# Contributing / Guía de contribución

## Language / Idioma
- **EN**: code, column names, models, branches and commit messages.
- **ES + EN**: documentation (`docs/es/`, `docs/en/`, dbt `description:`).

## Branches / Ramas
| Branch | Purpose |
|---|---|
| `main` | Production (**PRO**). Deliverable-ready only. Tagged releases. |
| `develop` | Integration (**DEV**). A feature lands here when it works. |
| `feature/<topic>` | One task each, e.g. `feature/snowflake-setup`. Created from `develop`. |

Flow (decision D-038): `feature/*` → `develop` → `main`, by **pull request** (or merge from GitHub Desktop). A feature goes to `develop` when it works; `develop` goes to `main` only after it has been checked there. There is **no `pre` branch** and **no `pro` branch**: `main` is production (PRO). In dbt Cloud the Development environment uses the feature branches, a deployment environment follows `develop` (DEV) and the Production environment follows `main` (PRO).

Every commit must be explained by the assistant before the user makes it (message + plain-language explanation).

## Commits (Conventional Commits)
```
<type>(<scope>): <short description in English, imperative>
```
- **type**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- **scope**: `ingestion`, `staging`, `silver`, `gold`, `bi`, `snowflake`, `generator`, `ci`
- Example: `feat(ingestion): add stage and file formats for EU sales`

## Versions (tags, SemVer)
`v0.1.0-alpha` raw ingestion · `v0.2.0-alpha` staging/silver + tests · `v0.3.0-beta` star schema · `v0.4.0-beta` Power BI · `v1.0.0` final delivery.

## Naming conventions
- Snowflake: `{ENV}_MB_{LAYER}_DB` (`DEV_MB_BRONZE_DB`, `DEV_MB_SILVER_DB`, `DEV_MB_GOLD_DB`); roles `{ENV}_MB_TRANSFORM_ROLE`.
- dbt models: `stg_<source>__<table>`, `slv_<source>__<table>`, `int_<topic>__<verb>`, `dim_<entity>`, `fct_<event>`, `agg_<topic>`.
- YAML files: `_<source>__models.yml`, `_<source>__sources.yml`.
- Columns: `snake_case`, English, with units/zone in the name (`price_eur`, `sale_date_utc`).

## Secrets
Never commit credentials. `profiles.yml` and `.env` are git-ignored.

## Token log
`logs/token_log.csv` is filled automatically by a Claude Code hook (`scripts/log_tokens.py`, configured in `.claude/settings.json`).
