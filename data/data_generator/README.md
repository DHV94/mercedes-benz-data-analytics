# Data generator / Generador de datos

**ES** — Simula el sistema origen de ventas de Europa (y su maestro de concesionarios). **No son datos reales de Mercedes-Benz.** Con la misma semilla genera siempre los mismos ficheros, lo que permite repetir la demo.

**EN** — Simulates the European sales source system (and its dealer master). **Not real Mercedes-Benz data.** The same seed always produces the same files, so the demo can be repeated.

## Usage / Uso

```bash
python data/data_generator/generate_europe.py --output data/data_generator/output
```

Options: `--seed 42` (reproducibility), `--rows 45000` (clean sales before defects).
`output/` is git-ignored; it can always be regenerated.

## What it creates / Qué crea

| File | Content |
|---|---|
| `batch_1/sales_eu_2021.csv` … `sales_eu_2025.csv` | Sales history up to 2025-11-30, one file per year. CSV `;`, UTF-8, decimal comma, `dd/mm/yyyy` |
| `batch_1/dealer_master.csv` | Dealer master (128 dealers, 6 countries). CSV `,`, ISO dates |
| `delta_1/` … `delta_6/` | Six small deltas of December 2025 (about 5 days each, 134–180 rows): `sales_eu_2025_delta_N.csv` + `dealer_master.csv`. Each delta tests one thing (new sales, identical re-sent rows, corrections, dealer renames, closures + new dealer, alert rows). See `docs/es/demo_scenarios.md` |
| `reference/delta_plan.csv`, `alert_rows.csv` | Exact rows and expected effect of every delta; the 10 deliberate alert rows of delta 6 |
| `reference/tax_types.csv`, `taxes.csv`, `tax_regime_map.csv` | Tax types, rates with validity and every spelling of `tax_regime` (feed the dbt seeds, D-060) |
| `reference/model_alias.csv` | Every spelling of every model name → `model_variant_code` (feeds the dbt seed) |
| `manifest.json` | Rows and SHA-256 per file (to prove two runs are identical) |

`config/model_catalog.csv` is the model catalog (51 variants, 5 powertrains: PETROL, DIESEL, HEV, PHEV, BEV; 7 body types) and will also be the source of the dbt seed `model_catalog`. Prices and availability are fictional approximations.

## How the data is built / Cómo se construye

1. A **trend** per year makes the data answer the use cases: electric and plug-in hybrids grow, SUVs gain share, sedans lose it.
2. Each sale gets a country (weights), an open dealer of that country, a model variant available that year, prices in local currency (EUR, GBP, CHF) **including VAT** (European source).
3. A deterministic `sale_id` (`EU-YYYY-NNNNNN`) and a VIN with real structure (manufacturer, model-year letter, serial).
4. **Defects** are applied afterwards to the raw text (see `RATES` in the script and section 5 of `docs/es/source_design.md`): duplicates, empty/invalid VIN, model-name spellings, bad dates, delivery before sale, prices with thousands separator or symbol, zero/negative prices, currency variants, whitespace/case, empty customer type, unknown dealers.

## Demo flow / Flujo de la demo

1. Load `batch_1` → run the pipeline → record row counts.
2. Run the pipeline **again** with no new data → counts must not change (idempotency).
3. Load `delta_1` … `delta_6` one by one (run the pipeline after each) → see `docs/es/demo_scenarios.md` for the expected counts of every step.
