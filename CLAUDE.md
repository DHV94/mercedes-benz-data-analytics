# CLAUDE.md — read me first

Full project context lives in [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md). Read it before answering.

## Working agreement (non-negotiable)
- This is the user's **final project** for a Data Engineering course. **Guide, don't do the work for them**: give instructions, explain the *why*, let them build. The user must be able to defend every piece in an oral presentation.
- Exceptions: boilerplate/templates and the Python data generator (source-system simulator) may be written by Claude, but must be explained.
- The user is mentally saturated: short steps, one thing at a time, no exhaustive surveys. Give a recommendation, not a menu.
- **The user makes all git commits** (GitHub Desktop) and creates branches. Never commit/push.
- **Every time a commit is due, give the user two things:** (1) the ready-to-paste commit message (summary line + optional description for the Description box, Conventional Commits, English) and (2) a plain-language explanation in Spanish of what each changed file does and why. The goal is that the user understands every commit. Propose how to group changes into separate commits (one per task) and say which files go in each.
- **Tell the user before any git action** (create a branch, commit, push, pull, merge, pull request, tag): say which action, on which branch, and the exact steps in GitHub Desktop. Say which files go in which commit. `logs/token_log.csv` can go in any commit (suggest the last one of the group).
- Branch flow: `feature/*` → `develop` (DEV) → `pre` (PRE) → `main` (PRO), by pull request. See `CONTRIBUTING.md`.
- Chat language: Spanish. Code, columns, models, branches, commits: English. Docs: Spanish + English.
- **Start every session by reading `docs/SESSION_NOTES.md`** (hand-off file shared with ChatGPT). Before the last commit of every work session, update it (state, open points, next actions, session log). The notes must match the real repo.
- Internal deadline: stable code by **2026-11-24 ~20:00**. The user presents **Thursday 2026-11-26, 3rd turn**. Do not depend on Wednesday for essential code.
- **Decision log**: whenever a decision is made (or an option is discarded), add it to `docs/es/decisions_log.md` (context, options, decision, why). The user will use it in the presentation.
- Never put secrets in the repo (`profiles.yml`, `.env` are git-ignored).
- Token log is automatic (`scripts/log_tokens.py` Stop hook -> `logs/token_log.csv`).
