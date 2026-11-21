# SESSION_NOTES — hand-off between sessions (Claude / ChatGPT)

> **Rule: whoever works on the project (Claude, ChatGPT or the user) updates this file before the last commit of every work session.** It must always reflect the real state of the repo, so any session can resume from it alone.
> Read order for a new session: `CLAUDE.md` → this file → `docs/PROJECT_CONTEXT.md` → `docs/es/decisions_log.md` → (when relevant) `docs/es/source_design.md`.

- **Last updated:** 2026-11-20, work PC (by Claude, Sonnet 5.5)
- **Copy-paste prompt to start any new session:** `docs/HANDOFF_PROMPT.md`
- **Branch of reference:** `develop`. Flow `feature/*` → `develop` → `main` (D-038). No `pre` and no `pro` branch (`main` is PRO, also in dbt Cloud). `origin/pre` exists on GitHub but is unused (see `CONTRIBUTING.md`).
- Slide notes: `docs/es/slides_notes.md` (script, evidence checklist, questions for the teachers).

## 1. Real state of the repo (audit 2026-11-20)

| Area | State |
|---|---|
| Repo, branches (`main`, `develop`), README, CONTRIBUTING, `.gitignore` | ✅ Done |
| Token log (`scripts/log_tokens.py` + hook in `.claude/settings.json`) | ✅ Working; `logs/token_log.csv` is committed |
| Context, decision log (D-001…D-031), source design | ✅ Written (source design is a **draft**, see §3) |
| `snowflake/01_setup_environment.sql` | ✍️ Written and committed. **Confirmed by the user: NOT run yet.** Nothing exists in Snowflake. No data generated, dbt not used yet. |
| `docs/es/exercise_dimensional_model.md` | ✍️ Written: modelling exercise (course-style statement, no solution). **The user designs the model first**; Claude reviews. |
| Stages / file formats / bronze tables (`02_…`, `03_…`) | ❌ Not started |
| Data generator (`data/data_generator/`) | ✅ **Europe only, written and tested (2026-11-21, by Claude, not yet explained to the user)**: `generate_europe.py`, `config/model_catalog.csv`, `README.md`. Reproducible (same seed ⇒ identical SHA-256), batch 1 (history to 2025-10-31) + batch 2 (new + corrected + re-sent rows, dealer renames/closures). US and China not done. |
| dbt Cloud project (`dbt_project/`) | ❌ Not started. New dbt Cloud account exists. |
| `docs/es/business_context.md`, English docs (`docs/en/`) | ❌ Not started |
| Power BI (`powerbi/`) | ❌ Not started |

Japan and Korea are **only designed on paper**, nothing is implemented for them.

## 2. Scope as of 2026-11-20 (see `docs/PROJECT_CONTEXT.md` §3c and decisions D-019…D-025)

- **Five use cases:** UC1 sales by model family · UC2 by body type · UC3 by powertrain (**UC1–UC3 all over 2021–2025**) · UC4 top-3 families by region in 2025 · UC5 recalls (US only, shown next to US sales, no ratio; D-039) software/electronics vs mechanical by model and year; powertrain breakdown optional.
- **Time window (open):** 5 years (2021–2025) justified as the basis to plan the next 5, e.g. a strategic review at the end of 2026 (or a meeting held in H1 2026). Still to define; in Power BI decide whether each view is one year or the whole window (year selector).
- UC1–UC4: commercial section with an interactive map. UC5: separate section, no map (NHTSA = US only).
- Dropped for now: bottom-3 models, sales forecasting, and any **ratio of real recalls over simulated sales**.
- Data: simulated sales (Python) + real NHTSA recalls + seeds. Core sources: **Europe, US, China**; Japan/Korea optional and only after one source works end-to-end.
- Teachers' priorities: grain of every table · incremental strategy from ingestion to Gold (not forced on every table) · reproducible batches · run twice without duplicates · second batch with new/changed data · SQL counts before/after · **SCD2 snapshot (dealers)** · dbt tests + alerts · macros only where useful · documentation.

## 3. Open points
1. Define the time-window narrative (see §2). **Decided:** generate data for 2021–2025 only (no 2020). Branch `pre` is **no longer used** — flow is `feature/*` → `develop` → `main` (D-038).
2. **User is solving `docs/es/exercise_dimensional_model.md`** (conceptual/logical/physical silver + gold star schema). Claude reviews it afterwards; do NOT give the solution beforehand. Family vs variant must be distinguished.
3. ~~`replacement` / leasing / renting~~ — **dropped** (D-018): the project only records sales.
4. UC5: which real public data besides NHTSA? (user is exploring with ChatGPT). Bring: source, license, format, grain, coverage, join key.
5. Delivery channel for repo + slides: **not confirmed, ask the teachers**.
6. `source_design.md` still lists 5 regions and 24 dirt types: trim to the core scope once the model is closed.
7. **Live demo (D-031):** ~3 min. Batch 1 and batch 2 (new + changed rows), incremental run, SQL counts before/after, automation with a Snowflake Task or a scheduled dbt Cloud job (to confirm). **Plan B:** screenshots or a recorded video in case the live run fails.
8. **Questions for the teachers** (bring to the work sessions): (a) delivery channel for the repo and the slides; (b) is one Snowflake Task or one dbt Cloud job enough as "automation"?; (c) what do they expect from the demo and from the 2021–2025 window?
9. **NHTSA recalls = checkpoint (D-036).** Real file downloaded to `data/nhtsa/raw/` (zip + `RCL.txt` committed; unzipped 314 MB ignored). Included in the modelling for now; review every session and **drop UC5 if it costs too much time** (if the sales flow is not stable end-to-end by Tue 24). Bronze keeps the full file, filter (MB cars, report date 2021–2025) in silver (D-035). Snowflake cannot read `.zip`: gzip the txt before loading. Exercise 2.6 was updated with the real fields.

## 4. Calendar (replaces the old one)
- Fri 20: class in the afternoon → close dimensional model.
- Sat 21: light work in the morning.
- Sun 22: development day.
- Mon 23: class 16:00–20:00 (teachers available) → technical doubts.
- Tue 24: last class afternoon → **stable working code by ~20:00**.
- Wed 25: classmates present; documentation, delivery, rehearsal. Do not depend on it for essential code.
- **Thu 26: user presents, 3rd turn** (10–15 min). Needs repo + slides submitted before presenting. Extras: dog meme (if natural), miniature Mercedes car.

## 5. Next actions (in order)
1. Dimensional model closed and understood by the user (grain, facts, dimensions, keys).
2. Run/verify Snowflake setup; stage + file format + bronze table for **one** source (suggested: Europe).
3. Small generator with reproducible batches for that source.
4. dbt Cloud project: sources → staging → silver (incremental) → gold; tests; snapshot on dealers.
5. Idempotency demo (run twice) and second batch; SQL counts. **This is the base of the live demo** (D-031, open point 7).
6. Power BI; documentation; slides.

## 6. Session log (append one line per session)
- 2026-11-17/19 (Claude): scope, repo, hook, docs, Snowflake script, decision log.
- 2026-11-20 (Claude): audit of the repo, scope revision after teacher/ChatGPT review, this file created.
- 2026-11-20 end (Claude): added VIN section to slide notes, slides as free-form blocks, git prompts only when worthwhile. User continues the modelling exercise in class and will send the result. Next session: review the user's model (grain, keys, relationships) — do not give the solution first.
- 2026-11-20 later (Claude): modelling exercise written (user is solving it in draw.io and will send results), leasing/renting/replacement dropped, data 2021–2025 only, branch flow with `pre`, commit-explanation and git-action-warning rules, slide notes file.
- 2026-11-20 work PC (Claude): applied D-030 (work only in `develop`) to CLAUDE.md and CONTRIBUTING.md, D-029 marked as partially superseded, D-030/D-031 recorded, open points 7 (live demo) and 8 (teacher questions) added, read-only repo checks done. Next: review the user's dimensional model (do not give the solution first).
- 2026-11-20 work PC (Claude, later): D-030 replaced by D-038 (`feature/*` → `develop` → `main`, no `pre`, no `pro`; `main` is PRO in dbt Cloud). Added D-032…D-037 (NHTSA scope and storage, passenger cars only). Exercise 2.6 rewritten with real NHTSA fields. D-039: UC5 limited to the US, shown next to US sales (no ratio). User now solves the modelling exercise in draw.io; next session: review it (grain, keys, family vs variant, relationships) without giving the solution. Worked at the work PC.
- 2026-11-20 home (Claude, Sonnet 5.5): reviewed the user's **conceptual** model (`docs/diagrams/mercedes-benz-data-analytics_modelado_conceptual.png`; readable in dark mode). D-040: no physical model, 3NF not mandatory. Feedback given: 3 inverted cardinalities (family, body type, powertrain vs model), currency/tax into country, FX as separate table linked to currency, recalls should link at family level (D-039), N:M to resolve in the logical model. Logical model (= silver) is next: the user sends it; then dimensional (= gold). Nothing committed in this session.
- 2026-11-20 home (Claude, later): reviewed conceptual v2 (cardinalities fixed, recalls now linked to family, tax as separate table). Analysed the real NHTSA file to answer campaign↔component: N:M confirmed; component depends on campaign+model+year; 43,484 rows → 2,973 distinct (campaign, model, year, component). D-041 recorded. Open: tax history (validity dates vs snapshot), FX rate per month?, then logical model (user).
- 2026-11-20 home (Claude, later): conceptual **v3 reviewed and approved** (`docs/diagrams/..._conceptual_v3.png`): Country 1—M Tax (versions), Currency 1—M FX rate, recalls linked to family, N:M recall↔component. Conceptual model closed. Next: the user writes the logical model (silver).
- 2026-11-21 home (Claude, later): logical v1 reviewed (`docs/diagrams/mercedes-benz-data-analytics_logical_v1.png`). To fix in v2: resolve both N:M recalls relations with ONE intermediate table (campaign × family × model year × component; `potential_units` stays in campaigns), move the tax FK to `taxes.country_id`, add an exchange-rate table (currency × month), invert Models–Sales cardinality (1 model : M sales), dealers with `dealer_code` + validity columns, sales with `source_system` + `source_sale_id`, English snake_case names. D-042 (dealer history, point-in-time join as future improvement) and D-043 (sale key) recorded. Next: logical v2, then the dimensional model (gold).
- 2026-11-21 12:27 (Claude): logical **v3** reviewed (`..._logical_v3.png`). Direction is right (one table with campaign + family + component keys) but to fix in v4: (1) split `campaigns` (campaign_id, report_date, potential_units) from the intermediate table (campaign_id, family_id, **model_year**, component_id; surrogate id + unique natural key) — model_year was missing; (2) remove `campaign_id` from `components`; (3) split `currencies` (code, name) from `exchange_rates` (currency_id, month, rate); (4) taxes still need `country_id` (or decide to keep only `countries.tax_id`, not both); (5) sales still need `source_system`/`source_sale_id`. [Update: logical **v4** reviewed — sales got `source_system`/`source_sale_id`; campaigns now split into campaign + campaign line. Still to fix in v5: campaign→lines and families→campaigns cardinalities inverted; remove the `campaign lines` column and `campaign_id` from `components`; family + `model_year` belong in the line (D-045: ~35% of real campaigns affect several families; the file has no status); `currencies` still mixes currency and rate by date; with tax only in countries (D-046) the Countries–Taxes cardinality must be M countries : 1 tax. Geography decided in D-047. Later the same day (D-050) taxes go back to a table WITH validity dates per country (`taxes.country_id`, rate, valid_from, valid_to) and `sales` stores the applied tax (FK, computed in silver); `countries.tax_id` is removed; US row has rate 0. D-048: model has first/last model year; D-049 (net revenue as secondary measure) awaits the user's confirmation.] [2026-11-21 13:38: logical **v5** reviewed — nearly closed. Fixes for v6: (a) move the Families relationship from `campaigns` to `campaign_lines` (1 family : M lines); (b) add `sales.tax_id` and reverse Sales–Taxes (1 tax : M sales); (c) remove `exchange_rate_id` from `currencies`, add `currency_code`, mark `exchange_rates.currency_id` as FK; (d) remove the `campaign lines` column from campaigns and add `potential_units`; (e) add `model_year` to `sales`. Dealers keep `dealer_id` in sales for now (caveat: snapshot dates are "detected on", so a point-in-time join would miss early history; reports will use the current version, D-042). **Hard stop agreed in advice:** dimensional model closed by Sunday 22 at ~12:00, otherwise gold = sales only.] [2026-11-21 afternoon: logical **v6** reviewed — logical model effectively CLOSED. Applied: tax_id and model_year in sales, campaigns (potential_units), campaign line (family + model_year), exchange_rates. Two small leftovers for v7 (do not block the dimensional model): (1) Families–Campaign line cardinality reversed (should be 1 family : M lines); (2) `currencies` still has `exchange_rate_id` (remove), lacks `currency_code`, and `exchange_rates.currency_id` is not marked FK. Typos to fix: Contries, Campaings, Campaing line, componentes. NEXT: the dimensional model (gold), sales first (UC1–UC4).] [**Logical model v7 reviewed and CLOSED** (`..._logical_v7.png`): all v6 leftovers fixed; only cosmetic typos remain (`campaing_id`, `date_of_campaing`, `Campaing line`). Next for the user: write the grain of each silver table ("one row is…"), then the dimensional model (exercise part 2, question 1 first).] [**Logical v8 = FINAL** (typos fixed). LOGICAL MODEL CLOSED on 2026-11-21 13:5x. Opening of the presentation drafted in `docs/es/slides_notes.md` §2b.] Time: noon checkpoint missed for the logical model; plan = close the SALES side now, start the dimensional model for UC1–UC4 first, recalls fact only if time (D-036).
- 2026-11-21 00:57 (Claude): user made corrections in `docs/diagrams/mercedes-benz-data-analytics_logical_v2.png` (NOT reviewed yet). Pending in v2: the single intermediate table for recalls (campaign × family × model year × component). Open design point: the user wants to keep `countries.tax_id` (current tax) AND add `taxes.country_id`; Claude's advice: keep only `taxes.country_id` and derive the current rate from validity dates (two links can disagree); if kept, document it as a "current tax" shortcut and add a consistency test. **Time status:** Saturday 21 checkpoint (logical + dimensional closed) still ahead; Sat afternoon is family time, so only the morning is available. If not closed by ~noon, cut: gold = sales only, recalls out (D-036). Sunday must carry Snowflake + generator + bronze + dbt connection.
- 2026-11-21 early morning (Claude): at the user's request, wrote and tested the Europe data generator (D-044) to save Sunday time. Output not committed to Git (`data/data_generator/output/` is ignored; regenerate with `python data/data_generator/generate_europe.py --output data/data_generator/output`). The user has NOT reviewed it yet: **explain it to the user** before using it in the pipeline. Next: logical v2 + dimensional (Saturday morning), then Snowflake scripts 02/03 (stage, file format, bronze table for Europe) guided step by step.
