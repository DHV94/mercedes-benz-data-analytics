# CLAUDE.md — read me first

Full project context lives in [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md). Read it before answering.

## Working agreement (non-negotiable)
- This is the user's **final project** for a Data Engineering course. **Guide, don't do the work for them**: give instructions, explain the *why*, let them build. The user must be able to defend every piece in an oral presentation.
- Exceptions: boilerplate/templates and the Python data generator (source-system simulator) may be written by Claude, but must be explained.
- Since 2026-11-24 the user also asked Claude to write specific parts (gold models, NHTSA recalls, tests, the UC5 classification). See `docs/es/ai_collaboration_log.md`; the user must review and be able to explain them.
- Short steps, one thing at a time, no exhaustive surveys. Give a recommendation, not a menu.
- **Git (updated 2026-11-22, user's explicit decision in chat):** Claude may create **local commits** to save time, but only after explaining to the user in Spanish what the commit contains and why. The user does **push, pull, PRs and merges** and creates/renames branches. Claude never pushes, never opens PRs, never merges. Never add a Claude `Co-Authored-By` line or any Claude attribution to commit messages.
- **Every time a commit is due, give the user two things:** (1) the ready-to-paste commit message (summary line + optional description for the Description box, Conventional Commits, English) and (2) a plain-language explanation in Spanish of what each changed file does and why. The goal is that the user understands every commit. Propose how to group changes into separate commits (one per task) and say which files go in each.
- **Git actions: only when they are worth it** (a finished task, a working milestone, or before switching context). Do not prompt for a commit/PR after every small edit and do not over-control: batch small changes. When one is due, say which action, on which branch, the exact GitHub Desktop steps and which files go in which commit. `logs/token_log.csv` can go in any commit (suggest the last one of the group).  One `feature-<topic>` branch per task (D-038).
- Branch flow (D-038, updated by D-067): `feature-*` → `develop` (DEV) → `pre` (PRE) → `main` (PRO), by pull request. No `pro` branch (`main` is PRO, also in dbt Cloud). See `CONTRIBUTING.md`.
- **Time watch (user request, 2026-11-20):** at the start and end of each session check the calendar in `docs/SESSION_NOTES.md` §4 and the checkpoints below, and say clearly when to speed up, cut scope or force a step. The user has authorised forcing when needed, but still wants to understand each part (go step by step, cut scope before skipping understanding).
  - Checkpoints: end Sat 21 → logical + dimensional models closed (if not, gold = sales only, recalls out); end Sun 22 → Snowflake set up, Europe loaded in bronze, dbt Cloud connected; end Mon 23 → Europe silver + gold working with incremental and dealer snapshot; Tue 24 20:00 → stable code, repeatable demo (batch 1, batch 2, counts).
- Chat language: Spanish. Code, columns, models, branches, commits: English. Docs: Spanish + English.
- **Start every session by reading `docs/SESSION_NOTES.md`** (hand-off file shared with ChatGPT). Before the last commit of every work session, update it (state, open points, next actions, session log). The notes must match the real repo.
- Internal deadline: stable code by **2026-11-24 ~20:00**. The user presents **Thursday 2026-11-26, 3rd turn**. Do not depend on Wednesday for essential code.
- **Decision log**: whenever a decision is made (or an option is discarded), add it to `docs/es/decisions_log.md` (context, options, decision, why). The user will use it in the presentation.
- Never put secrets in the repo (`profiles.yml`, `.env` are git-ignored).
- Token log is automatic (`scripts/log_tokens.py` Stop hook -> `logs/token_log.csv`).
