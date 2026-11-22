"""Simulated source system: Mercedes-Benz passenger car sales in Europe + dealer master.

What it produces (all files are reproducible: same --seed => identical files):

    output/
      batch_1/sales_eu_2021.csv ... sales_eu_2025.csv   history up to 2025-11-30, one file per year
      batch_1/dealer_master.csv                         dealer master as of batch 1
      delta_1/ ... delta_6/                             six small weekly deltas of December 2025 (see below)
        sales_eu_2025_delta_N.csv                       new sales (+ re-sent rows, corrections or alert rows)
        dealer_master.csv                               dealer master as of that delta (scripted scenario)
      reference/model_alias.csv                         every spelling of a model name -> variant code
      reference/tax_types.csv, taxes.csv                tax types and rates with validity (seed for dbt)
      reference/tax_regime_map.csv                      every spelling of tax_regime -> tax type code
      reference/delta_plan.csv                          rows and expected effect of every delta (demo script)
      reference/calibration_report.csv                  public market share vs generated share, per year
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
import shutil
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
BATCH_1_END = date(2025, 11, 30)  # sales after this date arrive in the December deltas
# Six small deltas (about 5 days of December 2025 each) used to test the incremental load at home, in class and live.
DELTA_WINDOWS = [(date(2025, 12, 1), date(2025, 12, 5)), (date(2025, 12, 6), date(2025, 12, 10)),
                 (date(2025, 12, 11), date(2025, 12, 15)), (date(2025, 12, 16), date(2025, 12, 20)),
                 (date(2025, 12, 21), date(2025, 12, 25)), (date(2025, 12, 26), date(2025, 12, 31))]
DELTA_RESENT_FROM_BATCH_1 = 5   # delta 2: identical rows sent again (from batch 1)
DELTA_RESENT_FROM_DELTA_1 = 3   # delta 2: identical rows sent again (from delta 1)
DELTA_CORRECTIONS = {"returned": 6, "price": 4}  # delta 3: corrections of old sales (same sale_id)

# Market calibration (D-053): the share of each powertrain and of SUVs in every year is taken from public
# data (config/market_mix.csv: ACEA for powertrain, JATO for body type) instead of invented trends.
MARKET_MIX_PATH = HERE / "config" / "market_mix.csv"
POWERTRAINS = ["BEV", "PHEV", "HEV", "PETROL", "DIESEL"]  # HEV = full and mild hybrids
# Mercedes-Benz Cars reached a 40% xEV (BEV + PHEV) share in Europe in 2025 (Mercedes-Benz Group sales release,
# 12 Jan 2026), while the whole EU market was at 26.8% (ACEA). That ratio is applied to every year: an assumption.
MERCEDES_XEV_SHARE_EU_2025 = 40.0


def load_market_mix():
    """market_mix.csv -> {year: {"powertrain": {group: pct}, "suv": pct}} for the whole market (not Mercedes)."""
    mix = {y: {"powertrain": {}, "suv": None} for y in YEARS}
    with open(MARKET_MIX_PATH, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            year, pct = int(r["year"]), float(r["market_share_pct"])
            if r["dimension"] == "powertrain":
                mix[year]["powertrain"][r["group"]] = pct
            elif r["dimension"] == "body_type" and r["group"] == "SUV":
                mix[year]["suv"] = pct
    for year, m in mix.items():
        pt = m["powertrain"]
        assert set(pt) == set(POWERTRAINS) | {"OTHER"} and m["suv"] is not None, f"incomplete mix for {year}"
        assert abs(sum(pt.values()) - 100) < 0.01, f"powertrain shares of {year} must add up to 100"
        # "OTHER" (LPG, CNG, flex-fuel) is not in the catalog: it is folded into petrol and diesel pro rata.
        other = pt.pop("OTHER")
        base = pt["PETROL"] + pt["DIESEL"]
        pt["PETROL"] += other * pt["PETROL"] / base
        pt["DIESEL"] += other * pt["DIESEL"] / base
    return mix


def mercedes_targets(mix):
    """Market mix -> Mercedes-Benz mix. xEV (BEV, PHEV) is scaled by the Mercedes/market ratio of 2025;
    the rest is split between HEV, petrol and diesel keeping the market proportion. SUV is left as the market."""
    market_xev_2025 = mix[2025]["powertrain"]["BEV"] + mix[2025]["powertrain"]["PHEV"]
    factor = MERCEDES_XEV_SHARE_EU_2025 / market_xev_2025
    targets = {}
    for year, m in mix.items():
        pt = m["powertrain"]
        bev, phev = pt["BEV"] * factor, pt["PHEV"] * factor
        rest = 100 - bev - phev
        combustion_and_hev = pt["HEV"] + pt["PETROL"] + pt["DIESEL"]
        target = {"BEV": bev, "PHEV": phev}
        for group in ("HEV", "PETROL", "DIESEL"):
            target[group] = rest * pt[group] / combustion_and_hev
        targets[year] = {"powertrain": target, "suv": m["suv"]}
    return targets, factor


def calibrated_weights(variants, target, iterations=200):
    """Starts from the catalog popularity and rescales the weights (iterative proportional fitting) until the
    share of every powertrain and of SUVs matches the target. Inside a group the catalog popularity is kept."""
    dimensions = [(lambda v: v["powertrain"], target["powertrain"]),
                  (lambda v: v["body_type"] == "SUV", {True: target["suv"], False: 100 - target["suv"]})]
    weights = [v["popularity"] for v in variants]
    for _ in range(iterations):
        for group_of, goals in dimensions:
            total = sum(weights)
            sums = Counter()
            for v, w in zip(variants, weights):
                sums[group_of(v)] += w
            assert all(g in sums for g in goals), "a group has no variant available in that year"
            weights = [w * goals[group_of(v)] / 100 * total / sums[group_of(v)] for v, w in zip(variants, weights)]
    return weights


# Taxes (D-060). One standard VAT per country plus a reduced regime in some countries (simulated, inspired by real
# special regimes such as VAT reductions for people with disabilities). Verify real rates before presenting them.
TAX_TYPES = {
    "VAT_STANDARD": ("VAT standard rate", "General value added tax applied to a car sale"),
    "VAT_REDUCED": ("VAT reduced rate", "Special regime with a reduced rate (simulated, e.g. buyers with disabilities)"),
}
REGIME_TO_TYPE = {"STD": "VAT_STANDARD", "RED": "VAT_REDUCED"}
REGIME_SPELLINGS = {"STD": ["STD", "std", "Standard", "STANDARD"], "RED": ["RED", "red", "Reduced", "REDUCED"]}
# (country, tax type, rate in %, valid from, valid to; None = still valid). Data covers 2021-2025 only.
TAXES = [
    ("DE", "VAT_STANDARD", 19.0, date(2021, 1, 1), None),
    ("GB", "VAT_STANDARD", 20.0, date(2021, 1, 1), None),
    ("FR", "VAT_STANDARD", 20.0, date(2021, 1, 1), None),
    ("IT", "VAT_STANDARD", 22.0, date(2021, 1, 1), None),
    ("ES", "VAT_STANDARD", 21.0, date(2021, 1, 1), None),
    ("CH", "VAT_STANDARD", 7.7, date(2021, 1, 1), date(2023, 12, 31)),
    ("CH", "VAT_STANDARD", 8.1, date(2024, 1, 1), None),
    ("ES", "VAT_REDUCED", 4.0, date(2021, 1, 1), None),
    ("IT", "VAT_REDUCED", 4.0, date(2021, 1, 1), None),
    ("GB", "VAT_REDUCED", 0.0, date(2021, 1, 1), None),
    ("FR", "VAT_REDUCED", 5.5, date(2021, 1, 1), None),
]
REDUCED_SHARE = {"ES": 0.02, "IT": 0.02, "GB": 0.015, "FR": 0.015}  # share of sales with the reduced regime


def tax_rate(country, tax_type, day):
    rates = [t[2] for t in TAXES if t[0] == country and t[1] == tax_type and t[3] <= day
             and (t[4] is None or day <= t[4])]
    assert len(rates) == 1, f"tax {tax_type} of {country} on {day}: {len(rates)} rates"
    return rates[0]


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
    "regime_spelling": 0.03,    # D24 tax_regime written another way ("std", "Reduced")
}

SALES_COLUMNS = ["sale_id", "vin", "model_name", "model_year", "sale_date", "delivery_date",
                 "dealer_code", "country", "sale_price", "currency", "sale_status", "customer_type", "tax_regime"]
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


def scripted_dealer_versions(dealers, rng):
    """Dealer scenario for the deltas. It is scripted, so it is the same in every run (what the SCD2 snapshot must capture):

        delta 1-3: no change in the dealer master
        delta 4  : three dealers (DE, FR, ES) are renamed (+ " Partner")
        delta 5  : two dealers (GB, IT) close on 2025-12-22; the renamed German dealer changes name again
                   (third version: " Group"); a new Swiss dealer CH-0999 opens on 2025-12-21
        delta 6  : no change in the dealer master (the snapshot must create no new version)

    Returns (versions, scenario) where versions[n] is the master sent with delta n (1..6)."""
    active = [d for d in dealers if d["closing_date"] is None and d["opening_date"] < date(2025, 1, 1)]

    def pick(cc):
        return rng.choice(sorted((d for d in active if d["country_code"] == cc), key=lambda d: d["dealer_code"]))

    renamed = {cc: pick(cc)["dealer_code"] for cc in ("DE", "FR", "ES")}
    closing = {cc: pick(cc)["dealer_code"] for cc in ("GB", "IT")}
    new_dealer = {"dealer_code": "CH-0999", "dealer_name": "Garage Stern Bern", "country_code": "CH", "city": "Bern",
                  "region": "Bern", "opening_date": date(2025, 12, 21), "closing_date": None}

    v3 = [dict(d) for d in dealers]
    v4 = [dict(d) for d in v3]
    for d in v4:
        if d["dealer_code"] in renamed.values():
            d["dealer_name"] += " Partner"
    v5 = [dict(d) for d in v4]
    for d in v5:
        if d["dealer_code"] in closing.values():
            d["closing_date"] = date(2025, 12, 22)
        if d["dealer_code"] == renamed["DE"]:
            d["dealer_name"] += " Group"
    v5.append(new_dealer)
    versions = {1: v3, 2: v3, 3: v3, 4: v4, 5: v5, 6: v5}
    scenario = {4: [f"{c} renamed (+ Partner)" for c in renamed.values()],
                5: [f"{c} closed on 2025-12-22" for c in closing.values()]
                   + [f"{renamed['DE']} renamed again (+ Group)", "CH-0999 opened on 2025-12-21"]}
    return versions, scenario


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


def generate_sales(rng, catalog, dealers_final, n_rows, targets):
    by_country = {cc: [d for d in dealers_final if d["country_code"] == cc] for cc in COUNTRIES}
    countries = list(COUNTRIES)
    country_weights = [COUNTRIES[c][1] for c in countries]
    pool = {}
    for y in YEARS:
        variants = [v for v in catalog if v["available_from"] <= y <= v["available_to"]]
        pool[y] = (variants, calibrated_weights(variants, targets[y]))

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
        regime = "RED" if rng.random() < REDUCED_SHARE.get(cc, 0) else "STD"
        if regime == "RED":  # same net price as the standard regime, so the gross price is lower
            price = round(price / (1 + tax_rate(cc, "VAT_STANDARD", sale_date) / 100)
                          * (1 + tax_rate(cc, "VAT_REDUCED", sale_date) / 100), 2)
        delivery = None if status == "cancelled" else sale_date + timedelta(days=rng.randint(5, 120))
        records.append({"sale_date": sale_date, "delivery_date": delivery, "dealer_code": dealer["dealer_code"],
                        "country": cc, "variant": variant, "model_year": model_year, "price": price,
                        "currency": currency, "status": status, "tax_regime": regime,
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

        regime = rec["tax_regime"]
        if self.hit("regime_spelling"):
            regime = r.choice(REGIME_SPELLINGS[regime][1:])
        customer = "" if self.hit("null_customer") else rec["customer_type"]
        fields = {"model_name": model_name, "dealer_code": dealer, "country": rec["country"],
                  "sale_status": rec["status"], "customer_type": customer}
        if self.hit("whitespace_case"):
            key = r.choice([k for k, v in fields.items() if v])
            fields[key] = self.mess_text(fields[key])

        return [rec["sale_id"], vin, fields["model_name"], str(rec["model_year"]), sale_text, delivery_text,
                fields["dealer_code"], fields["country"], self.price(rec["price"], rec["currency"]), currency,
                fields["sale_status"], fields["customer_type"], regime]


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


def clean_row(rec):
    """A raw row with no random defect (used for the alert rows of delta 6)."""
    price = f"{rec['price']:.2f}".replace(".", ",")
    delivery = "" if rec["delivery_date"] is None else rec["delivery_date"].strftime("%d/%m/%Y")
    return [rec["sale_id"], rec["vin"], rec["variant"]["variant_name"], str(rec["model_year"]),
            rec["sale_date"].strftime("%d/%m/%Y"), delivery, rec["dealer_code"], rec["country"], price,
            rec["currency"], rec["status"], rec["customer_type"], rec["tax_regime"]]


# Alert rows of delta 6: each one must be caught by a dbt test and trigger the alert (column, new value, why)
ALERT_ROWS = [
    ("tax_regime", "XXX", "tax_regime not in the equivalence seed"),
    ("tax_regime", "", "empty tax_regime"),
    ("tax_regime", "RED", "reduced regime in a country without reduced rate (DE or CH)"),
    ("sale_price", "0,00", "price zero"),
    ("sale_price", "-1500,00", "negative price"),
    ("sale_date", "15/03/2026", "sale date in the future"),
    ("sale_date", "20/04/2026", "sale date in the future"),
    ("dealer_code", "DE-9999", "dealer not in the master"),
    ("dealer_code", "FR-9999", "dealer not in the master"),
    ("sale_status", "unknown", "status outside the accepted values"),
]


def alert_rows(recs):
    """Builds the alert rows from clean December records, with new sale ids EU-2025-9000NN."""
    rows = []
    pool = list(recs)
    for n, (column, value, _) in enumerate(ALERT_ROWS, start=1):
        wanted = ("DE", "CH") if column == "tax_regime" and value == "RED" else None
        base = next(r for r in pool if wanted is None or r["country"] in wanted)
        pool.remove(base)  # every alert row uses another record
        row = dict(zip(SALES_COLUMNS, clean_row(dict(base, sale_id=f"EU-2025-9{n:05d}"))))
        row[column] = value
        rows.append([row[c] for c in SALES_COLUMNS])
    return rows


def calibration_rows(sales, mix, targets):
    """Compares, per year, the public market share, the Mercedes target and what was really generated."""
    rows = []
    for year in YEARS:
        recs = [r for r in sales if r["sale_date"].year == year]
        n = len(recs)
        for group in POWERTRAINS:
            got = 100 * sum(r["variant"]["powertrain"] == group for r in recs) / n
            rows.append([year, "powertrain", group, f"{mix[year]['powertrain'][group]:.1f}",
                         f"{targets[year]['powertrain'][group]:.1f}", f"{got:.1f}", n])
        got = 100 * sum(r["variant"]["body_type"] == "SUV" for r in recs) / n
        rows.append([year, "body_type", "SUV", f"{mix[year]['suv']:.1f}", f"{targets[year]['suv']:.1f}",
                     f"{got:.1f}", n])
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
    dealer_versions, dealer_scenario = scripted_dealer_versions(dealers_b1, random.Random(args.seed + 1))
    mix = load_market_mix()
    targets, xev_factor = mercedes_targets(mix)
    sales = generate_sales(random.Random(args.seed + 2), catalog, dealer_versions[5], args.rows, targets)

    dirt = Dirt(random.Random(args.seed + 3), aliases)
    rng = random.Random(args.seed + 4)

    for old in ["batch_1", "batch_2", "reference"] + [f"delta_{n}" for n in range(1, 10)]:  # stale files of old runs
        shutil.rmtree(out / old, ignore_errors=True)

    batch_1 = [r for r in sales if r["sale_date"] <= BATCH_1_END]
    batch_1_ids = {r["sale_id"] for r in batch_1}
    delta_sales = [[r for r in sales if lo <= r["sale_date"] <= hi] for lo, hi in DELTA_WINDOWS]

    # ---- batch 1: one file per year (history up to 2025-11-30)
    first_raw = {}
    for year in YEARS:
        recs = [r for r in batch_1 if r["sale_date"].year == year]
        rows = [dirt.to_raw(r) for r in recs]
        for row in rows:
            first_raw.setdefault(row[0], row)
        rows = add_duplicates(rows, rng, dirt.stats)
        write_csv(out / "batch_1" / f"sales_eu_{year}.csv", SALES_COLUMNS, rows, ";")
    write_csv(out / "batch_1" / "dealer_master.csv", DEALER_COLUMNS, dealer_rows(dealers_b1), ",")

    # ---- six deltas of December 2025
    tests = {1: "Normal incremental load: new sales only",
             2: "Idempotency: identical rows sent again must not create duplicates",
             3: "Corrections: same sale_id with new status or price must update, not duplicate",
             4: "Dealer snapshot: three dealers renamed -> new versions",
             5: "Dealer snapshot: two closures, a second rename and a new dealer",
             6: "Alerts: rows that must fail tests (reference/alert_rows.csv); no dealer change"}
    plan = []
    delta_ids = {}
    sent_before = list(batch_1)  # records already sent (candidates for corrections)
    for n, recs in enumerate(delta_sales, start=1):
        rows = [dirt.to_raw(r) for r in recs]
        for row in rows:
            first_raw.setdefault(row[0], row)
        delta_ids[n] = [row[0] for row in rows]
        resent = corrections = alerts = 0
        if n == 2:
            ids = rng.sample(sorted(batch_1_ids), DELTA_RESENT_FROM_BATCH_1)
            ids += rng.sample(delta_ids[1], DELTA_RESENT_FROM_DELTA_1)
            rows.extend(list(first_raw[i]) for i in ids)
            resent = len(ids)
        if n == 3:
            candidates = [r for r in sent_before if r["status"] == "sold" and r["delivery_date"] is not None]
            for kind, count in DELTA_CORRECTIONS.items():
                for rec in rng.sample(candidates, count):
                    candidates.remove(rec)
                    fixed = dict(rec)
                    if kind == "returned":
                        fixed["status"] = "returned"
                    else:
                        fixed["price"] = round(rec["price"] * rng.uniform(0.95, 1.05), 2)
                    rows.append(dirt.to_raw(fixed))
                    corrections += 1
        if n == 6:
            extra = alert_rows(list(recs))
            rows.extend(extra)
            alerts = len(extra)
        rng.shuffle(rows)
        sent_before.extend(recs)
        write_csv(out / f"delta_{n}" / f"sales_eu_2025_delta_{n}.csv", SALES_COLUMNS, rows, ";")
        write_csv(out / f"delta_{n}" / "dealer_master.csv", DEALER_COLUMNS, dealer_rows(dealer_versions[n]), ",")
        plan.append([n, f"delta_{n}/sales_eu_2025_delta_{n}.csv", len(rows), len(recs), corrections, resent, alerts,
                     "; ".join(dealer_scenario.get(n, [])) or "no change", tests[n]])
    write_csv(out / "reference" / "delta_plan.csv",
              ["delta", "file", "rows", "new_sales", "corrections", "resent_rows", "alert_rows", "dealer_changes",
               "what_it_tests"], plan, ",")
    write_csv(out / "reference" / "alert_rows.csv", ["sale_id", "column", "bad_value", "why_it_must_fail"],
              [[f"EU-2025-9{n:05d}", c, v, why] for n, (c, v, why) in enumerate(ALERT_ROWS, start=1)], ",")

    # ---- reference: every spelling of every model name, tax types, taxes and tax regime spellings
    alias_rows = [[s, code] for code, names in aliases.items() for s in names]
    write_csv(out / "reference" / "model_alias.csv", ["raw_name", "model_variant_code"], alias_rows, ",")
    write_csv(out / "reference" / "tax_types.csv", ["tax_type_code", "tax_type_name", "description"],
              [[code, name, desc] for code, (name, desc) in TAX_TYPES.items()], ",")
    write_csv(out / "reference" / "taxes.csv",
              ["country_code", "tax_type_code", "tax_value", "valid_from", "valid_to"],
              [[c, t, f"{v:.1f}", f.isoformat(), to.isoformat() if to else ""] for c, t, v, f, to in TAXES], ",")
    write_csv(out / "reference" / "tax_regime_map.csv", ["raw_regime", "regime_code", "tax_type_code"],
              [[sp, code, REGIME_TO_TYPE[code]] for code, sps in REGIME_SPELLINGS.items() for sp in sps], ",")

    # ---- calibration report (not a source file: documents how close the simulation is to public data)
    write_csv(out / "reference" / "calibration_report.csv",
              ["year", "dimension", "group", "market_pct", "mercedes_target_pct", "generated_pct", "rows"],
              calibration_rows(sales, mix, targets), ",")

    # ---- manifest
    manifest = {}
    for path in sorted(out.rglob("*.csv")):
        data = path.read_bytes()
        manifest[path.relative_to(out).as_posix()] = {
            "rows": data.count(b"\n") - 1, "sha256": hashlib.sha256(data).hexdigest()}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"seed={args.seed} clean sales={len(sales)} (batch 1: {len(batch_1)}, December deltas: "
          f"{sum(len(d) for d in delta_sales)})")
    for name, info in manifest.items():
        print(f"  {name:<40} {info['rows']:>7} rows")
    print(f"market calibration: Mercedes xEV factor = {xev_factor:.3f} (see reference/calibration_report.csv)")
    print("defects applied:", dict(sorted(dirt.stats.items())))
    print("\ndelta plan (rows = lines in the file without header):")
    for row in plan:
        print(f"  delta {row[0]}: {row[2]:>4} rows = {row[3]} new + {row[4]} corrections + {row[5]} re-sent + "
              f"{row[6]} alert | dealers: {row[7]}")


if __name__ == "__main__":
    main()
