# Project context / Contexto del proyecto

> Living document. Update it whenever a decision changes. Purpose: recover full context if the AI assistant session is lost.
> Última actualización: 2026-11-18.

## 1. Goal
Final project, Data Engineering programme (Cívica). Simulate working for **Mercedes-Benz**: build the full data platform (ingestion, cleaning, modelling, testing, BI) with **Snowflake + dbt Cloud + Power BI**, simulating a multi-person international team.

## 2. Constraints
- Individual project; deadline **2026-11-24 ~20:00**; presentations 25–26 Nov; **user presents Thu 26 Nov, 3rd turn** (updated 2026-11-20). Internal goal: stable code by Tue 24 ~20:00.
- Snowflake trial: ~382 $ credits, ~19 days left on 2026-11-17 (expires ~2026-12-06). Warehouse XS, auto-suspend 60 s.
- dbt Cloud: use **"Latest" (v1.x)**, not v2/Fusion. New account planned (Gmail `+dbt` alias) because the free Developer plan allows 1 project and the practice project uses it.
- Course material (read-only reference): `C:\Users\dhv94\Documents\GitHub\Curso-Data-Engineer`. Do NOT copy it into this repo (slides may not be redistributable).

## 3. Business questions
**Core (must):** sales evolution over recent years by (a) **body type** (coupé, sedan, SUV…) and (b) **powertrain** (ICE, hybrid, plug-in hybrid, electric…).
**Also:**
- (c) Recall campaigns over model years, comparing **software/electronics** failures vs **mechanical** ones, with "recalls per 1,000 units sold" by model.
- (d) "Do pentests/security certifications make cars safer?" is reframed as the evolution of recalls due to software/electronic faults (no causal claim).
- NHTSA covers the US only: sales-vs-recalls comparisons use US sales only. State it in the presentation.

**Stretch (only if time):** forecast for a future model by region (Europe, China, Japan, US) — out of scope for data engineering; mention as future work, at most Power BI's built-in forecast, flagged as indicative.

## 3b. (SUPERSEDED on 2026-11-20 by 3c — kept for history)
Design principle: few, simple, visual; scalable later. Cases 1–4 go in a Power BI **map** report (country level, region as roll-up).

| # | Use case | Notes |
|---|---|---|
| UC1 | Sales evolution by **body type** by region, last 5 years (2021–2025) | (superseded by 3c) |
| UC2 | Sales evolution by **powertrain** by region, last 5 years | Same |
| UC3 | **Top 3 best-selling models** by region, 2025 | Model = model **family** (e.g. GLC), not variant |
| UC4 | **Top 3 worst-selling models** by region, 2025 | Only models on sale all year; define a minimum-availability rule so new/discontinued models don't distort it |
| UC5 | **Recalls: software vs mechanical components**, recent years | **Open**: to explore with ChatGPT (other public data found by the user). Baseline: NHTSA recalls + `nhtsa_component_map` seed |

Metric definition (to be formalised in `docs/es/business_context.md`): a *unit sold* = delivered vehicle with status `sold`; `returned`, `cancelled` and `replacement` are excluded.
Acquisition type, net price in EUR and data-quality reporting stay as attributes/filters/technical work, not use cases.

## 3c. Definitive use cases and scope (2026-11-20) — current
| # | Use case | Notes |
|---|---|---|
| UC1 | Sales evolution by **model family**, 2021–2025 | Family (e.g. GLC) ≠ variant (e.g. GLC 300 e). Define the grain explicitly |
| UC2 | Sales evolution by **body type**, 2021–2025 | |
| UC3 | Sales evolution by **powertrain**, 2021–2025 | Time-window narrative still open (D-026) |
| UC4 | **Top 3 families by region**, 2025 | |
| UC5 | **Recall campaigns, software/electronics vs mechanical**, by model and year | Separate report section, no map (NHTSA = US). Extra public data to be evaluated |

- UC1–UC4: commercial section with interactive map, region/country filters and navigation between charts.
- Dropped for now: bottom-3 models, forecasting, and any ratio of real recalls over simulated sales (misleading: real vs simulated data).
- Optional if time: pictures of model families as a catalogue attribute.
- Sources: Europe, US and China are the core; Japan and Korea (only designed on paper) are optional, after one source works end-to-end.
- Teachers' priorities: grain per table; incremental from ingestion to Gold (only where it makes sense); reproducible batches; run twice without duplicates; second batch with new/changed data; SQL before/after counts; SCD2 snapshot on dealers; dbt tests + alerts; macros only where useful; documentation.
- Calendar and presentation: see `docs/SESSION_NOTES.md` §4 (**user presents Thursday 2026-11-26, 3rd turn**; supersedes the dates in §2 and §7).
- Day-to-day state and next actions: `docs/SESSION_NOTES.md`.

## 4. Data strategy (hybrid)
No public transaction-level Mercedes sales exist, so:
1. **Simulated sales** (Python generator, acts as the "source system"), **2021–2025** (decided 2026-11-20, D-026), **~100k rows sample** (justified as a demo sample for performance), calibrated to public Mercedes figures. Delivered per region, in different formats, in several batches (incremental loads).
2. **Seeds**: `model_catalog` (model, body type, powertrain, production years), `region_country`, `nhtsa_component_map` (NHTSA component -> software/electronics | mechanical | other), `fx_rates` (EUR conversion).
3. **Real NHTSA recalls** for Mercedes-Benz (public).
4. Calendar and region tables.

Be explicit in the presentation that sales are simulated.

### Region delivery formats
| Region | Format |
|---|---|
| Europe | CSV `;`, decimal comma, dates `dd/mm/yyyy` |
| US | CSV `,`, dates `mm/dd/yyyy` |
| China | JSON |
| Japan | CSV, different encoding and/or different column names (decided: yes, add more differences) |

### Decided details
- **Price kept in local currency** (EUR, USD, CNY, JPY) in bronze/silver; converted in the pipeline with an FX-rate seed/table. Main reporting currency EUR; goal: conversion to all currencies if feasible.
- **Deliberate dirt (as realistic as possible):** duplicates, nulls in key fields, malformed dates, inconsistent model names (`"C 300"`, `"c300"`, `"C-Class 300"`), prices with symbols/text, plus Japan-specific quirks (different column names/encoding). Add more realistic ones when designing the generator.

## 5. Architecture and conventions
```
Source files -> Snowflake stage -> BRONZE (COPY INTO) -> dbt: staging (stg_) -> silver (slv_) -> gold (int_/dim_/fct_/agg_) -> Power BI
```
- Follows the course's medallion convention. Snowflake DBs: `{ENV}_MB_BRONZE_DB / _SILVER_DB / _GOLD_DB` for DEV/PRE/PRO; roles `{ENV}_MB_TRANSFORM_ROLE` + a reporting role; warehouse `WH_MB`. Prefix `MB` avoids clashing with the practice objects already in the trial account (`DEV_BRONZE_DB`, `WH_CURSO`…).
- dbt: bronze = `source()` only; staging = rename/cast 1:1; silver = dedupe/clean (tables); gold: `intermediate`, `core` (dim/fct), `agg_`. Seeds and snapshots in silver. File naming `stg_<source>__<table>.sql`, `_<source>__models.yml`.
- Reference course examples: `Curso-Data-Engineer/Apuntes y archivos/4- dbt/` (`dbt_project.yml` of day 5, `01_crear_entorno.sql`, `docs/architecture.md` of day 2).

### Draft dimensional model (to close together)
- `fct_sales`: one row per vehicle sold.
- `fct_recalls`: one row per recall campaign × model × model year.
- Dimensions: `dim_model` (includes body type + powertrain, **shared by both facts**), `dim_dealer`, `dim_region`, `dim_date`, `dim_component`.

## 6. Git / team simulation
- Branches (updated 2026-11-20): `feature/*`/`fix/*` → `develop` (DEV) → `pre` (PRE) → `main` (PRO, deliverable only), by PR/merge. Each branch maps to a dbt/Snowflake environment.
- Commits: Conventional Commits in English, **no date prefix** (git stores it): `feat(ingestion): add stage and file formats`.
- Tags (SemVer): `v0.1.0-alpha` raw ingestion · `v0.2.0-alpha` staging/silver + tests · `v0.3.0-beta` star schema · `v0.4.0-beta` Power BI · `v1.0.0` final.
- See `CONTRIBUTING.md`.

## 7. Schedule
| Day | Goal |
|---|---|
| 17–18 | Source design + dimensional model, repo, Snowflake setup, data generator, backlog |
| 19 | Bronze ingestion + dbt sources |
| 20 | Staging: cleaning + tests |
| 21 | Intermediate + marts (star schema), snapshot/incremental |
| 22 | Power BI |
| 23 | Docs, CI, security hardening, polish |
| 24 | Presentation + rehearsal + buffer |

Strategy: first a small end-to-end version that works, then extend.

## 8. Cybersecurity / DevSecOps angle (user request — do near the end, day 23)
Candidate free measures (to evaluate and pick realistically):
- **Secrets**: `gitleaks` pre-commit hook + CI step; GitHub secret scanning; no credentials in repo.
- **Snowflake**: key-pair authentication for the dbt service user, least-privilege roles per environment, network policy, **masking policies / row access policies** (e.g. dealer-level data), separate service user for jobs, read-only `REPORTING_ROLE`.
- **CI/CD (DevSecOps)**: dbt Cloud CI job or GitHub Actions on PRs: `sqlfluff` lint, `dbt build --select state:modified+`, `bandit` on the Python generator, Dependabot, branch protection on `main`/`develop`.
- **Data governance**: model contracts, `meta` owners, PII-free by design (documented).

Narrative: security is part of the pipeline, not an afterthought.

## 9. Working agreement
See `CLAUDE.md`. Model in use: Sonnet 5.5 (medium); switch to Opus only for hard design decisions. Token usage: `logs/token_log.csv`.

## 10. Status log
- 2026-11-17: scope, data strategy, conventions agreed. Repo `mercedes-benz-data-analytics` created (private), base files + token hook done, branch `develop` created. First commit pending (user does it).
- 2026-11-18: decisions on volume (~100k), local-currency prices + FX conversion, dirt list, DevSecOps angle. This context document created.

- 2026-11-18 (later): new dbt Cloud account created. Source design v0.1 drafted (`docs/es/source_design.md`). Decisions: Reiwa dates + schema drift included; Europe = EUR/GBP/CHF; net prices in reports (gross kept, `tax_rates` seed); leasing/renting added as `acquisition_type`; weekly consumption on Tuesday mornings (scheduled job + source freshness); Japan only (Korea/India = future work).

- 2026-11-18 (end): Korea added (S4b, CP949, price in 10k KRW). Market weights reviewed with public 2025 data (Mercedes cars: China 551.9k units ~31%, Europe 634.6k, US ~285k, Germany 213.2k, Korea ~68.5k). `replacement` acquisition type added (interpretation to confirm). Wrote `snowflake/01_setup_environment.sql`. User has NOT committed yet.

## 11. Open items / next steps (resume here)
1. **User**: commit everything on `develop` (suggested: `docs: add source design and project context`, `feat(snowflake): add environment setup script`) and publish the branch.
2. **User**: replace `<YOUR_USER>` in `snowflake/01_setup_environment.sql`, run it in Snowsight, report the output of the final `show databases`.
3. Confirm the meaning of `replacement` (see `docs/es/source_design.md`, note after D24).
4. Next scripts: `02_stages_and_file_formats.sql` (internal stage + 5 file formats: EU `;`, US `,`, JP Shift-JIS, KR tab CP949, JSON), then `03_bronze_tables.sql`.
5. Write the data generator (`data/data_generator/`) — Claude writes it, explains it; user reviews.
6. Create dbt Cloud project (new account already created): connection to Snowflake (DEV_MB_TRANSFORM_ROLE, WH_MB), repo connection, `dbt_project.yml` with env vars `DBT_SILVER_DB` / `DBT_GOLD_DB` like the course.
7. Close the dimensional model; backlog (GitHub Projects).
8. Pending info from user: required deliverables/format of the presentation when known.
