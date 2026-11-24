# mercedes-benz-data-analytics

**ES** — Proyecto final de la formación de Ingeniero de Datos (Cívica): plataforma de datos para analizar la evolución de ventas por tipo de carrocería y propulsión, y las campañas de revisión (defectos) de Mercedes-Benz. Stack: **Snowflake + dbt Cloud + Power BI**.

**EN** — Final project of the Data Engineering programme (Cívica): a data platform to analyse sales evolution by body type and powertrain, and recall campaigns for Mercedes-Benz. Stack: **Snowflake + dbt Cloud + Power BI**.

> ⚠️ Sales data is **simulated** (no public transaction-level data exists). Recalls are **real** public data from NHTSA (Mercedes-Benz vehicles, model years 2021-2025). / Las ventas son **simuladas**; las campañas de defectos son datos **reales** públicos de NHTSA.

## Architecture / Arquitectura
```
Source files → Snowflake stage → BRONZE (COPY INTO, raw text) → dbt: staging → silver → gold (star schema) → Power BI
```
| Layer | What it holds | In dbt |
|---|---|---|
| Bronze | Raw text exactly as received + load metadata (`_source_file`, `_loaded_at`) | `source()` only, loaded by Snowflake |
| Staging | Same rows, right types and clean text | views |
| Silver | One clean row per business key (deduplicated, translated) | tables; `silver_sales` is **incremental** (`merge`) |
| Snapshot | History of dealers (SCD type 2) | `snap_dealers` |
| Gold | Star schema for reporting | `fct_sales`, `fct_campaign_line`, `dim_date`, `dim_model`, `dim_family`, `dim_dealer`, `dim_tax`, `dim_component` |

## Environments and jobs / Entornos y jobs
Three environments with the **same code**; only the variable `DBT_ENV_NAME` (dbt Cloud) changes which databases and roles are used (macros `generate_database_name` and `generate_schema_name`).

| Environment | Git branch | Databases | Role |
|---|---|---|---|
| DEV | feature branch (dbt Cloud IDE) | `DEV_MB_SILVER_DB`, `DEV_MB_GOLD_DB` (personal schema prefix) | `DEV_MB_TRANSFORM_ROLE` |
| PRE | `pre` | `PRE_MB_SILVER_DB`, `PRE_MB_GOLD_DB` | `PRE_MB_TRANSFORM_ROLE` |
| PRO | `main` | `PRO_MB_SILVER_DB`, `PRO_MB_GOLD_DB` | `PRO_MB_TRANSFORM_ROLE` |

Flow: `feature-*` → pull request → `develop` → `pre` → `main`. Jobs: `PRE · build`, `PRO · build` (manual) and `PRO · semanal` (every Monday 06:00 UTC). Bronze is single (`DEV_MB_BRONZE_DB`) and read by every environment. Power BI reads PRO gold with the read-only role `MB_REPORTING_ROLE`.

## How the data is loaded / Cómo se cargan los datos
Manual by design (a weekly automatic load is the planned evolution): upload the file to the stage, `COPY INTO` bronze, run dbt. Scripts in `snowflake/`; step-by-step scripts in `docs/es/demo_jueves.md` and `docs/es/demo_reset.md`.

## Repository layout / Estructura
| Path | Content |
|---|---|
| `snowflake/` | Setup scripts: roles, databases, bronze tables, PRE, reporting grants, recalls |
| `data/data_generator/` | Simulated Europe source system (reproducible batches and deltas) |
| `data/nhtsa/` | Real NHTSA recalls and the script that filters them |
| `dbt_project/` | dbt models (`staging`, `silver`, `gold`), seeds, snapshot, macros and tests |
| `powerbi/` | Power BI report |
| `docs/es`, `docs/en` | Documentation, decision log (`decisions_log.md`), demo and Power BI guides |
| `docs/evidence/` | Numbered screenshots (index in `docs/evidence/README.md`) |
| `docs/diagrams/` | Conceptual, logical and dimensional models |

## Where to start reading / Por dónde empezar
1. `docs/PROJECT_CONTEXT.md` — scope and architecture.
2. `docs/es/decisions_log.md` — every decision with the options discarded.
3. `docs/es/data_dictionary.md` and the YAML files in `dbt_project/models/` — columns and tests.
4. `docs/es/demo_jueves.md` — the live demo.

See [CONTRIBUTING.md](CONTRIBUTING.md) for conventions.

## Status / Estado
✅ Europe sales end to end (bronze → gold → Power BI), real NHTSA recalls, three environments with jobs, macros, tests and alerts. Planned: more regions (US, CN, JP, KR), automatic weekly ingestion, users and SSO per role.
