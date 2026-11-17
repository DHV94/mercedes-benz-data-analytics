# mercedes-benz-data-analytics

**ES** — Proyecto final de la formación de Ingeniero de Datos (Cívica): plataforma de datos para analizar la evolución de ventas por tipo de carrocería y propulsión, y las campañas de revisión (software/electrónica frente a mecánica) de Mercedes-Benz. Stack: **Snowflake + dbt Cloud + Power BI**.

**EN** — Final project of the Data Engineering programme (Cívica): a data platform to analyse sales evolution by body type and powertrain, and recall campaigns (software/electronics vs. mechanical) for Mercedes-Benz. Stack: **Snowflake + dbt Cloud + Power BI**.

> ⚠️ Sales data is **simulated** (no public transaction-level data exists). Recalls come from NHTSA public data. / Las ventas son **simuladas**; las revisiones proceden de datos públicos de la NHTSA.

## Architecture / Arquitectura
```
Source files → Snowflake stage → BRONZE (COPY INTO) → dbt: staging → silver → gold (star schema) → Power BI
```

## Repository layout / Estructura
| Path | Content |
|---|---|
| `snowflake/` | Setup scripts (roles, warehouse, databases) |
| `data_generator/` | Simulated source systems (EU, US, CN, JP) |
| `dbt_project/` | dbt models, seeds, tests, macros |
| `powerbi/` | Power BI report |
| `docs/es`, `docs/en` | Documentation |
| `logs/token_log.csv` | Automatic AI token usage log |

See [CONTRIBUTING.md](CONTRIBUTING.md) for conventions.

## Status / Estado
🚧 In progress — delivery 2026-11-24.
