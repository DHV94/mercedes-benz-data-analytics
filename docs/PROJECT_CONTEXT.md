# Project context / Contexto del proyecto

> Living document. Update it whenever a decision changes. Purpose: recover full context if the AI assistant session is lost.
> Última actualización: 2026-11-18.

## 1. Goal
Final project, Data Engineering programme (Cívica). Simulate working for **Mercedes-Benz**: build the full data platform (ingestion, cleaning, modelling, testing, BI) with **Snowflake + dbt Cloud + Power BI**, simulating a multi-person international team.

## 2. Constraints
- Individual project; deadline **2026-11-24 ~20:00**; presentations 25–26 Nov (user presents on the 25th). No margin assumed after the deadline.
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

## 4. Data strategy (hybrid)
No public transaction-level Mercedes sales exist, so:
1. **Simulated sales** (Python generator, acts as the "source system"), 2019–2025, **~100k rows sample** (justified as a demo sample for performance), calibrated to public Mercedes figures. Delivered per region, in different formats, in several batches (incremental loads).
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
- Branches: `main` (deliverable only), `develop`, `feature/*`, `fix/*`; PRs into `develop`.
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

## 11. Open items / next steps
1. User: create new dbt Cloud account (Gmail `+dbt` alias); first commit + publish `develop`.
2. Design of sources (columns per region, Japan differences, dirt catalogue) in `docs/`.
3. Snowflake setup scripts (`snowflake/`), then data generator.
4. Close the dimensional model; backlog (GitHub Projects).
5. Pending info from user: confirm required deliverables/format of the presentation when known.
