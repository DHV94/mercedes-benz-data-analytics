# Contributing / Guía de contribución

## Language / Idioma
- **EN**: code, column names, models, branches and commit messages.
- **ES + EN**: documentation (`docs/es/`, `docs/en/`, dbt `description:`).

## Branches / Ramas
| Branch | Purpose |
|---|---|
| `main` | Production (**PRO**). Deliverable-ready only. |
| `develop` | Integration (**DEV**). A feature lands here when it works. |
| `pre` | Pre-production (**PRE**). Checked here before `main`. |
| `feature-<topic>` | One task each, e.g. `feature-snowflake-setup`. Created from `develop`. Written with a hyphen because GitHub Desktop does not accept `feature/` here (a branch named `feature` already exists locally). |

Flow (D-038, updated by D-067): `feature-*` → `develop` → `pre` → `main`, by **pull request**. In dbt Cloud the Development environment uses the feature branches, the PRE deployment environment follows `pre` and the Production environment follows `main` (PRO). There is no `pro` branch.

Every commit must be explained by the assistant before the user makes it (message + plain-language explanation).

## Commits (Conventional Commits)
```
<type>(<scope>): <short description in English, imperative>
```
- **type**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- **scope**: `ingestion`, `staging`, `silver`, `gold`, `recalls`, `powerbi`, `bi`, `snowflake`, `generator`, `ci`
- Example: `feat(ingestion): add stage and file formats for EU sales`

## Versions (tags, SemVer) — planned, not applied yet
`v0.1.0-alpha` raw ingestion · `v0.2.0-alpha` staging/silver + tests · `v0.3.0-beta` star schema · `v0.4.0-beta` Power BI · `v1.0.0` final delivery.

## Naming conventions
- Snowflake: `{ENV}_MB_{LAYER}_DB` (`DEV_MB_SILVER_DB`, `PRO_MB_GOLD_DB`); a single bronze, `DEV_MB_BRONZE_DB`. Roles: `MB_INGEST_ROLE`, `{ENV}_MB_TRANSFORM_ROLE`, `MB_REPORTING_ROLE`.
- dbt models: `stg_<name>`, `silver_<name>`, `snap_<name>`, `dim_<entity>`, `fct_<event>`.
- YAML files: `_sources.yml`, `_<layer>.yml`.
- Columns: `snake_case`, English, with the unit or currency in the name when it matters (`price_net_eur`).

## Secrets
Never commit credentials. `profiles.yml` and `.env` are git-ignored.

## Token log
`logs/token_log.csv` is filled automatically by a Claude Code hook (`scripts/log_tokens.py`, configured in `.claude/settings.json`).
