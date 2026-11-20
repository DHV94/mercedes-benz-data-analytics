# SESSION_NOTES — hand-off between sessions (Claude / ChatGPT)

> **Rule: whoever works on the project (Claude, ChatGPT or the user) updates this file before the last commit of every work session.** It must always reflect the real state of the repo, so any session can resume from it alone.
> Read order for a new session: `CLAUDE.md` → this file → `docs/PROJECT_CONTEXT.md` → `docs/es/decisions_log.md` → (when relevant) `docs/es/source_design.md`.

- **Last updated:** 2026-11-20, later (by Claude, Sonnet 5.5)
- **Copy-paste prompt to start any new session:** `docs/HANDOFF_PROMPT.md`
- **Branch of reference:** `develop`. All files up to 2026-11-20 are committed in `develop`; branch `pre` created from `develop`. Feature branches are used when useful to simulate the team workflow (see `CONTRIBUTING.md`).
- Slide notes: `docs/es/slides_notes.md` (script, evidence checklist, questions for the teachers).

## 1. Real state of the repo (audit 2026-11-20)

| Area | State |
|---|---|
| Repo, branches (`main`, `develop`), README, CONTRIBUTING, `.gitignore` | ✅ Done |
| Token log (`scripts/log_tokens.py` + hook in `.claude/settings.json`) | ✅ Working; `logs/token_log.csv` is committed |
| Context, decision log (D-001…D-025), source design | ✅ Written (source design is a **draft**, see §3) |
| `snowflake/01_setup_environment.sql` | ✍️ Written and committed. **Confirmed by the user: NOT run yet.** Nothing exists in Snowflake. No data generated, dbt not used yet. |
| `docs/es/exercise_dimensional_model.md` | ✍️ Written: modelling exercise (course-style statement, no solution). **The user designs the model first**; Claude reviews. |
| Stages / file formats / bronze tables (`02_…`, `03_…`) | ❌ Not started |
| Data generator (`data_generator/`) | ❌ Not started (folder only has `.gitkeep`) |
| dbt Cloud project (`dbt_project/`) | ❌ Not started. New dbt Cloud account exists. |
| `docs/es/business_context.md`, English docs (`docs/en/`) | ❌ Not started |
| Power BI (`powerbi/`) | ❌ Not started |

Japan and Korea are **only designed on paper**, nothing is implemented for them.

## 2. Scope as of 2026-11-20 (see `docs/PROJECT_CONTEXT.md` §3c and decisions D-019…D-025)

- **Five use cases:** UC1 sales by model family · UC2 by body type · UC3 by powertrain (**UC1–UC3 all over 2021–2025**) · UC4 top-3 families by region in 2025 · UC5 recalls software/electronics vs mechanical by model and year.
- **Time window (open):** 5 years (2021–2025) justified as the basis to plan the next 5, e.g. a strategic review at the end of 2026 (or a meeting held in H1 2026). Still to define; in Power BI decide whether each view is one year or the whole window (year selector).
- UC1–UC4: commercial section with an interactive map. UC5: separate section, no map (NHTSA = US only).
- Dropped for now: bottom-3 models, sales forecasting, and any **ratio of real recalls over simulated sales**.
- Data: simulated sales (Python) + real NHTSA recalls + seeds. Core sources: **Europe, US, China**; Japan/Korea optional and only after one source works end-to-end.
- Teachers' priorities: grain of every table · incremental strategy from ingestion to Gold (not forced on every table) · reproducible batches · run twice without duplicates · second batch with new/changed data · SQL counts before/after · **SCD2 snapshot (dealers)** · dbt tests + alerts · macros only where useful · documentation.

## 3. Open points
1. Define the time-window narrative (see §2). **Decided:** generate data for 2021–2025 only (no 2020). Create branch `pre` from `develop` (user does it) — flow is `feature/*` → `develop` → `pre` → `main`.
2. **User is solving `docs/es/exercise_dimensional_model.md`** (conceptual/logical/physical silver + gold star schema). Claude reviews it afterwards; do NOT give the solution beforehand. Family vs variant must be distinguished.
3. ~~`replacement` / leasing / renting~~ — **dropped** (D-018): the project only records sales.
4. UC5: which real public data besides NHTSA? (user is exploring with ChatGPT). Bring: source, license, format, grain, coverage, join key.
5. Delivery channel for repo + slides: **not confirmed, ask the teachers**.
6. `source_design.md` still lists 5 regions and 24 dirt types: trim to the core scope once the model is closed.

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
5. Idempotency demo (run twice) and second batch; SQL counts.
6. Power BI; documentation; slides.

## 6. Session log (append one line per session)
- 2026-11-17/19 (Claude): scope, repo, hook, docs, Snowflake script, decision log.
- 2026-11-20 (Claude): audit of the repo, scope revision after teacher/ChatGPT review, this file created.
- 2026-11-20 end (Claude): added VIN section to slide notes, slides as free-form blocks, git prompts only when worthwhile. User continues the modelling exercise in class and will send the result. Next session: review the user's model (grain, keys, relationships) — do not give the solution first.
- 2026-11-20 later (Claude): modelling exercise written (user is solving it in draw.io and will send results), leasing/renting/replacement dropped, data 2021–2025 only, branch flow with `pre`, commit-explanation and git-action-warning rules, slide notes file.
