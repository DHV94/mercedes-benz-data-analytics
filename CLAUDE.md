# CLAUDE.md — read me first

Full project context lives in [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md). Read it before answering.

## Working agreement (non-negotiable)
- This is the user's **final project** for a Data Engineering course. **Guide, don't do the work for them**: give instructions, explain the *why*, let them build. The user must be able to defend every piece in an oral presentation.
- Exceptions: boilerplate/templates and the Python data generator (source-system simulator) may be written by Claude, but must be explained.
- The user is mentally saturated: short steps, one thing at a time, no exhaustive surveys. Give a recommendation, not a menu.
- **The user makes all git commits** (GitHub Desktop) and creates branches. Never commit/push.
- Chat language: Spanish. Code, columns, models, branches, commits: English. Docs: Spanish + English.
- Hard deadline: **2026-11-24 ~20:00**. Presentation 2026-11-25 (user is #11 of 29, first day). Do not count on work time after the deadline.
- **Decision log**: whenever a decision is made (or an option is discarded), add it to `docs/es/decisions_log.md` (context, options, decision, why). The user will use it in the presentation.
- Never put secrets in the repo (`profiles.yml`, `.env` are git-ignored).
- Token log is automatic (`scripts/log_tokens.py` Stop hook -> `logs/token_log.csv`).
