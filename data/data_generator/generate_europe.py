"""Simulated source system: Mercedes-Benz passenger car sales in Europe + dealer master.

What it produces (all files are reproducible: same --seed => identical files):

    output/
      batch_1/sales_eu_2021.csv ... sales_eu_2025.csv   history up to 2025-10-31, one file per year
      batch_1/dealer_master.csv                         dealer master as of batch 1
      batch_2/sales_eu_2025_delta.csv                   new sales (Nov-Dec 2025) + corrections + re-sent rows
      batch_2/dealer_master.csv                         dealer master with renamed and closed dealers
      reference/model_alias.csv                         every spelling of a model name -> variant code
      manifest.json                                     rows and SHA-256 of every file

European format (as designed in docs/es/source_design.md):
    CSV with ';', UTF-8, decimal comma, dates dd/mm/yyyy.

The data is deliberately dirty (see RATES). Nothing here is real Mercedes-Benz data.
Usage:
    python generate_europe.py --output <folder> [--seed 42] [--rows 45000]
"""
import argparse
import csv
import hashlib
import json
import random
from calendar import monthrange
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
CATALOG_PATH = HERE / "config" / "model_catalog.csv"

# --------------------------------------------------------------------------
# 1. Configuration
# --------------------------------------------------------------------------
# country: (currency, share of European sales, rough EUR -> local rate)
# The rates here only build plausible local prices; the real conversion in the
# pipeline uses the fx_rates seed.
COUNTRIES = {
    "DE": ("EUR", 0.33, 1.00),
    "GB": ("GBP", 0.20, 0.86),
    "FR": ("EUR", 0.13, 1.00),
    "IT": ("EUR", 0.12, 1.00),
    "ES": ("EUR", 0.10, 1.00),
    "CH": ("CHF", 0.06, 0.96),
}
CURRENCY_SYMBOL = {"EUR": "€", "GBP": "£", "CHF": "CHF"}
DEALERS_PER_COUNTRY = {"DE": 40, "GB": 25, "FR": 20, "IT": 20, "ES": 15, "CH": 8}
CITIES = {
    "DE": [("München", "Bayern"), ("Berlin", "Berlin"), ("Hamburg", "Hamburg"),
           ("Stuttgart", "Baden-Württemberg"), ("Köln", "Nordrhein-Westfalen"), ("Frankfurt", "Hessen")],
    "GB": [("London", "England"), ("Manchester", "England"), ("Leeds", "England"),
           ("Glasgow", "Scotland"), ("Cardiff", "Wales")],
    "FR": [("Paris", "Île-de-France"), ("Lyon", "Auvergne-Rhône-Alpes"),
           ("Marseille", "Provence-Alpes-Côte d'Azur"), ("Lille", "Hauts-de-France")],
    "IT": [("Milano", "Lombardia"), ("Roma", "Lazio"), ("Torino", "Piemonte"), ("Napoli", "Campania")],
    "ES": [("Madrid", "Madrid"), ("Barcelona", "Cataluña"), ("Valencia", "Comunidad Valenciana"),
           ("Sevilla", "Andalucía")],
    "CH": [("Zürich", "Zürich"), ("Genève", "Genève"), ("Basel", "Basel-Stadt")],
}
NAME_PREFIX = {"DE": "Autohaus", "GB": "Star Motors", "FR": "Garage Étoile",
               "IT": "Concessionaria Stella", "ES": "Concesionario Estrella", "CH": "Garage Stern"}

YEARS = [2021, 2022, 2023, 2024, 2025]
YEAR_WEIGHTS = [0.20, 0.19, 0.20, 0.21, 0.20]
MONTH_WEIGHTS = [0.9, 0.9, 1.3, 1.0, 1.0, 1.1, 0.9, 0.7, 1.3, 1.1, 1.0, 1.2]  # March and September peak
BATCH_1_END = date(2025, 10, 31)  # sales after this date arrive in batch 2

# Market trend: how much each powertrain / body type is "pushed" each year.
POWERTRAIN_FACTOR = {
    "ICE": {2021: 1.25, 2022: 1.15, 2023: 1.00, 2024: 0.90, 2025: 0.80},
    "PHEV": {2021: 1.00, 2022: 1.25, 2023: 1.35, 2024: 1.25, 2025: 1.15},
    "BEV": {2021: 0.60, 2022: 0.90, 2023: 1.20, 2024: 1.50, 2025: 1.90},
}


def body_factor(body_type, year):
    if body_type == "SUV":
        return 1 + 0.05 * (year - 2021)
    if body_type in ("Sedan", "Wagon"):
        return 1 - 0.035 * (year - 2021)
    return 1.0


STATUSES = ["sold", "returned", "cancelled"]
STATUS_WEIGHTS = [0.94, 0.03, 0.03]
CUSTOMER_TYPES = ["private", "company", "fleet"]
CUSTOMER_WEIGHTS = [0.70, 0.15, 0.15]

# Probability of each deliberate defect (docs/es/source_design.md, section 5).
RATES = {
    "duplicate_row": 0.015,     # D01 exact duplicate row inside a file
    "null_vin": 0.005,          # D03 empty VIN
    "bad_vin": 0.004,           # D04 VIN with wrong length or invalid letters (I, O, Q)
    "model_alias": 0.12,        # D05 model name written another way
    "bad_date": 0.006,          # D06 impossible date or another date format
    "delivery_before_sale": 0.004,  # D07
    "thousands_price": 0.15,    # D09 price with thousands separator "61.250,50"
    "symbol_price": 0.02,       # D09 price with currency symbol "61250,50 €"
    "bad_price": 0.003,         # D10 price zero or negative
    "currency_variant": 0.02,   # D12 "eur", "€"
    "whitespace_case": 0.03,    # D14 spaces and upper/lower case
    "null_customer": 0.04,      # D20 empty customer_type
    "unknown_dealer": 0.005,    # D15 dealer code not in the master
}
MODIFIED_SHARE = 0.015   # share of batch 1 sales corrected in batch 2 (same sale_id)
RESENT_SHARE = 0.005     # share of batch 1 rows sent again, identical, in batch 2

SALES_COLUMNS = ["sale_id", "vin", "model_name", "model_year", "sale_date", "delivery_date",
                 "dealer_code", "country", "sale_price", "currency", "sale_status", "customer_type"]
DEALER_COLUMNS = ["dealer_code", "dealer_name", "country_code", "city", "region",
                  "opening_date", "closing_date", "is_active"]

# VIN: positions 1-3 manufacturer, 4-8 descriptor, 9 check, 10 model year, 11 plant, 12-17 serial.
# Letters I, O and Q are never used in a real VIN.
VIN_CHARS = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ"
VIN_YEAR_CODES = "ABCDEFGHJKLMNPRSTVWXY"  # model years 2010..2030 (2021 = M, 2025 = S)


# --------------------------------------------------------------------------
# 2. Catalog and model name spellings
# --------------------------------------------------------------------------
def load_catalog():
    with open(CATALOG_PATH, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["available_from"] = int(r["available_from"])
        r["available_to"] = int(r["available_to"])
        r["base_price_eur"] = float(r["base_price_eur"])
        r["popularity"] = float(r["popularity"])
    return rows


def name_spellings(variant_name, family):
    """Every way the source systems may write a model name (the first one is the clean one)."""
    spellings = [variant_name,
                 variant_name.lower(),                       # "c 200"
                 variant_name.replace(" ", ""),              # "C200"
                 variant_name.replace(" ", "").lower(),      # "c200"
                 variant_name.upper(),                       # "C 200"
                 "Mercedes-Benz " + variant_name]
    if family.endswith("-Class") and variant_name.startswith(family[0] + " "):
        spellings.append(variant_name.replace(family[0] + " ", family + " ", 1))  # "C-Class 200"
    unique = []
    for s in spellings:
        if s not in unique:
            unique.append(s)
    return unique


def build_aliases(catalog):
    aliases = {}
    owner = {}
    for v in catalog:
        aliases[v["model_variant_code"]] = name_spellings(v["variant_name"], v["model_family"])
        for s in aliases[v["model_variant_code"]]:
            key = s.strip().lower()
            assert owner.setdefault(key, v["model_variant_code"]) == v["model_variant_code"], \
                f"spelling '{s}' belongs to two variants"
    return aliases


# --------------------------------------------------------------------------
# 3. Dealers
# --------------------------------------------------------------------------
def build_dealers(rng):
    dealers = []
    for cc, count in DEALERS_PER_COUNTRY.items():
        city_count = {}
        for number in sorted(rng.sample(range(1, 400), count)):
            city, region = rng.choice(CITIES[cc])
            city_count[city] = city_count.get(city, 0) + 1
            name = f"{NAME_PREFIX[cc]} {city}" + (f" {city_count[city]}" if city_count[city] > 1 else "")
            closing = None
            if rng.random() < 0.04:  # a few dealers closed before batch 1
                closing = date(rng.randint(2023, 2025), rng.randint(1, 10), rng.randint(1, 28))
                opening = date(rng.randint(2000, 2020), rng.randint(1, 12), rng.randint(1, 28))
            elif rng.random() < 0.10:  # a few dealers opened during the period
                opening = date(rng.randint(2022, 2024), rng.randint(1, 12), rng.randint(1, 28))
            else:
                opening = date(rng.randint(2000, 2020), rng.randint(1, 12), rng.randint(1, 28))
            dealers.append({"dealer_code": f"{cc}-{number:04d}", "dealer_name": name, "country_code": cc,
                            "city": city, "region": region, "opening_date": opening, "closing_date": closing})
    return dealers


def dealers_after_batch_2(dealers, rng):
    """Batch 2 master: some dealers are renamed, a few close in Nov-Dec 2025 (what the SCD2 snapshot will capture)."""
    result = []
    for d in dealers:
        d2 = dict(d)
        if d2["closing_date"] is None:
            r = rng.random()
            if r < 0.06:
                d2["dealer_name"] = d2["dealer_name"] + " Partner"
            elif r < 0.09:
                d2["closing_date"] = date(2025, rng.randint(11, 12), rng.randint(1, 28))
        result.append(d2)
    return result


def is_open(dealer, day):
    return dealer["opening_date"] <= day and (dealer["closing_date"] is None or day <= dealer["closing_date"])


# --------------------------------------------------------------------------
# 4. Clean sales records
# --------------------------------------------------------------------------
def make_vin(rng, body_type, model_year, serial):
    wmi = "W1N" if body_type == "SUV" else rng.choice(["WDD", "W1K"])
    descriptor = "".join(rng.choice(VIN_CHARS) for _ in range(5))
    check = rng.choice("0123456789X")
    year_code = VIN_YEAR_CODES[(model_year - 2010) % len(VIN_YEAR_CODES)]
    plant = rng.choice("FGKLN")
    return f"{wmi}{descriptor}{check}{year_code}{plant}{serial:06d}"


def generate_sales(rng, catalog, dealers_final, n_rows):
    by_country = {cc: [d for d in dealers_final if d["country_code"] == cc] for cc in COUNTRIES}
    countries = list(COUNTRIES)
    country_weights = [COUNTRIES[c][1] for c in countries]
    pool = {}
    for y in YEARS:
        variants = [v for v in catalog if v["available_from"] <= y <= v["available_to"]]
        weights = [v["popularity"] * POWERTRAIN_FACTOR[v["powertrain"]][y] * body_factor(v["body_type"], y)
                   for v in variants]
        pool[y] = (variants, weights)

    records = []
    for _ in range(n_rows):
        year = rng.choices(YEARS, YEAR_WEIGHTS)[0]
        month = rng.choices(range(1, 13), MONTH_WEIGHTS)[0]
        sale_date = date(year, month, rng.randint(1, monthrange(year, month)[1]))
        cc = rng.choices(countries, country_weights)[0]
        dealer = None
        for _ in range(30):
            candidate = rng.choice(by_country[cc])
            if is_open(candidate, sale_date):
                dealer = candidate
                break
        dealer = dealer or by_country[cc][0]
        variant = rng.choices(*pool[year])[0]
        model_year = min(max(year + rng.choices([-1, 0, 1], [0.2, 0.6, 0.2])[0], variant["available_from"]),
                         variant["available_to"])
        status = rng.choices(STATUSES, STATUS_WEIGHTS)[0]
        currency, _, fx = COUNTRIES[cc]
        price = round(variant["base_price_eur"] * (1.02 ** (year - 2021)) * rng.uniform(0.93, 1.07) * fx, 2)
        delivery = None if status == "cancelled" else sale_date + timedelta(days=rng.randint(5, 120))
        records.append({"sale_date": sale_date, "delivery_date": delivery, "dealer_code": dealer["dealer_code"],
                        "country": cc, "variant": variant, "model_year": model_year, "price": price,
                        "currency": currency, "status": status,
                        "customer_type": rng.choices(CUSTOMER_TYPES, CUSTOMER_WEIGHTS)[0]})

    records.sort(key=lambda r: r["sale_date"])
    per_year = Counter()
    for serial, r in enumerate(records, start=1):
        y = r["sale_date"].year
        per_year[y] += 1
        r["sale_id"] = f"EU-{y}-{per_year[y]:06d}"
        r["vin"] = make_vin(rng, r["variant"]["body_type"], r["model_year"], serial)
    return records


# --------------------------------------------------------------------------
# 5. From a clean record to a dirty raw row
# --------------------------------------------------------------------------
class Dirt:
    """Applies the deliberate defects and counts how many of each were applied."""

    def __init__(self, rng, aliases):
        self.rng = rng
        self.aliases = aliases
        self.stats = Counter()

    def hit(self, key):
        if self.rng.random() < RATES[key]:
            self.stats[key] += 1
            return True
        return False

    def corrupt_vin(self, vin):
        kind = self.rng.choice(["short", "long", "invalid_letter"])
        if kind == "short":
            return vin[:16]
        if kind == "long":
            return vin + self.rng.choice("0123456789")
        pos = self.rng.randrange(17)
        return vin[:pos] + self.rng.choice("IOQ") + vin[pos + 1:]

    def bad_date(self, d):
        return self.rng.choice([f"31/02/{d.year}", d.strftime("%Y-%m-%d"), d.strftime("%d.%m.%y")])

    def price(self, value, currency):
        if self.hit("bad_price"):
            value = self.rng.choice([0.0, -value])
        if self.hit("thousands_price"):
            text = f"{abs(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            text = f"{abs(value):.2f}".replace(".", ",")
        if self.hit("symbol_price"):
            text = f"{text} {CURRENCY_SYMBOL[currency]}"
        return ("-" if value < 0 else "") + text

    def mess_text(self, text):
        return self.rng.choice([text.upper(), text.lower(), " " + text, text + " ", text.title()])

    def to_raw(self, rec):
        r = self.rng
        vin = rec["vin"]
        if self.hit("null_vin"):
            vin = ""
        elif self.hit("bad_vin"):
            vin = self.corrupt_vin(vin)

        code = rec["variant"]["model_variant_code"]
        model_name = rec["variant"]["variant_name"]
        if self.hit("model_alias") and len(self.aliases[code]) > 1:
            model_name = r.choice(self.aliases[code][1:])

        sale_text = rec["sale_date"].strftime("%d/%m/%Y")
        if self.hit("bad_date"):
            sale_text = self.bad_date(rec["sale_date"])
        delivery = rec["delivery_date"]
        if delivery is not None and self.hit("delivery_before_sale"):
            delivery = rec["sale_date"] - timedelta(days=r.randint(1, 30))
        delivery_text = "" if delivery is None else delivery.strftime("%d/%m/%Y")

        dealer = rec["dealer_code"]
        if self.hit("unknown_dealer"):
            dealer = f"{rec['country']}-9999"

        currency = rec["currency"]
        if self.hit("currency_variant"):
            currency = r.choice([currency.lower(), CURRENCY_SYMBOL[currency]])

        customer = "" if self.hit("null_customer") else rec["customer_type"]
        fields = {"model_name": model_name, "dealer_code": dealer, "country": rec["country"],
                  "sale_status": rec["status"], "customer_type": customer}
        if self.hit("whitespace_case"):
            key = r.choice([k for k, v in fields.items() if v])
            fields[key] = self.mess_text(fields[key])

        return [rec["sale_id"], vin, fields["model_name"], str(rec["model_year"]), sale_text, delivery_text,
                fields["dealer_code"], fields["country"], self.price(rec["price"], rec["currency"]), currency,
                fields["sale_status"], fields["customer_type"]]


# --------------------------------------------------------------------------
# 6. Writing files
# --------------------------------------------------------------------------
def write_csv(path, header, rows, delimiter):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter=delimiter, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def dealer_rows(dealers):
    return [[d["dealer_code"], d["dealer_name"], d["country_code"], d["city"], d["region"],
             d["opening_date"].isoformat(), d["closing_date"].isoformat() if d["closing_date"] else "",
             "false" if d["closing_date"] else "true"] for d in dealers]


def add_duplicates(rows, rng, stats):
    """Insert exact copies of some rows at random positions (defect D01)."""
    for index in sorted(rng.sample(range(len(rows)), round(len(rows) * RATES["duplicate_row"]))):
        rows.insert(rng.randint(index + 1, len(rows)), list(rows[index]))
        stats["duplicate_row"] += 1
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", default=str(HERE / "output"), help="folder where files are written")
    parser.add_argument("--seed", type=int, default=42, help="same seed => identical files")
    parser.add_argument("--rows", type=int, default=45000, help="number of clean sales before defects")
    args = parser.parse_args()
    out = Path(args.output)

    catalog = load_catalog()
    aliases = build_aliases(catalog)

    dealers_b1 = build_dealers(random.Random(args.seed))
    dealers_b2 = dealers_after_batch_2(dealers_b1, random.Random(args.seed + 1))
    sales = generate_sales(random.Random(args.seed + 2), catalog, dealers_b2, args.rows)

    dirt = Dirt(random.Random(args.seed + 3), aliases)
    rng = random.Random(args.seed + 4)

    batch_1 = [r for r in sales if r["sale_date"] <= BATCH_1_END]
    batch_2_new = [r for r in sales if r["sale_date"] > BATCH_1_END]

    # ---- batch 1: one file per year
    first_raw = {}
    for year in YEARS:
        recs = [r for r in batch_1 if r["sale_date"].year == year]
        rows = [dirt.to_raw(r) for r in recs]
        for row in rows:
            first_raw.setdefault(row[0], row)
        rows = add_duplicates(rows, rng, dirt.stats)
        write_csv(out / "batch_1" / f"sales_eu_{year}.csv", SALES_COLUMNS, rows, ";")
    write_csv(out / "batch_1" / "dealer_master.csv", DEALER_COLUMNS, dealer_rows(dealers_b1), ",")

    # ---- batch 2: new sales + corrections of old sales (same sale_id) + identical re-sent rows
    delta = [dirt.to_raw(r) for r in batch_2_new]
    candidates = [r for r in batch_1 if r["status"] == "sold" and r["delivery_date"] is not None]
    for rec in rng.sample(candidates, round(len(batch_1) * MODIFIED_SHARE)):
        fixed = dict(rec)
        if rng.random() < 0.6:
            fixed["status"] = "returned"
        else:
            fixed["price"] = round(rec["price"] * rng.uniform(0.95, 1.05), 2)
        delta.append(dirt.to_raw(fixed))
    resent_ids = rng.sample(sorted(first_raw), round(len(first_raw) * RESENT_SHARE))
    delta.extend(list(first_raw[i]) for i in resent_ids)
    rng.shuffle(delta)
    write_csv(out / "batch_2" / "sales_eu_2025_delta.csv", SALES_COLUMNS, delta, ";")
    write_csv(out / "batch_2" / "dealer_master.csv", DEALER_COLUMNS, dealer_rows(dealers_b2), ",")

    # ---- reference: every spelling of every model name
    alias_rows = [[s, code] for code, names in aliases.items() for s in names]
    write_csv(out / "reference" / "model_alias.csv", ["raw_name", "model_variant_code"], alias_rows, ",")

    # ---- manifest
    manifest = {}
    for path in sorted(out.rglob("*.csv")):
        data = path.read_bytes()
        manifest[path.relative_to(out).as_posix()] = {
            "rows": data.count(b"\n") - 1, "sha256": hashlib.sha256(data).hexdigest()}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"seed={args.seed} clean sales={len(sales)} (batch 1: {len(batch_1)}, new in batch 2: {len(batch_2_new)})")
    for name, info in manifest.items():
        print(f"  {name:<40} {info['rows']:>7} rows")
    print("defects applied:", dict(sorted(dirt.stats.items())))


if __name__ == "__main__":
    main()
