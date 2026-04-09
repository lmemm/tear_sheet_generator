# CLAUDE.md — Instructions for Claude

This file tells Claude (and Claude Code) how to work in this project. Read this file completely before starting any work.

---

## Critical Rules

- **NEVER commit directly to main.** Always create a feature branch first.
- **NEVER disable safety constraints** unless the PM explicitly tells you to.
- **NEVER proceed based on assumptions** about project state — verify first (check files, run commands, test connections).

---

## Before You Start

1. Read this file completely.
2. Read `docs/ARCHITECTURE.md` to understand the system.
3. Read `BACKLOG.md` to see current tickets and priorities.
4. Read `docs/DECISIONS.md` for past architectural choices.
5. Check `docs/CHANGELOG.md` for recent changes.

---

## General Behavior

- When the user asks you to run a command (e.g., `python scripts/main.py`), execute it immediately — don't treat it as a suggestion or discussion point.
- If a request is ambiguous, ask whether the user wants you to implement it or walk them through it before starting.
- When verifying setup or credentials, actually test the connection (e.g., make a real API call) — don't just check that environment variables exist.
- Do not explore, refactor, or build anything beyond what was asked.

---

## Environment

- **Platform:** Mac (local development), also used via Claude Code on the Web
- **Python environment:** Always use the project's virtual environment (`.venv`). Never install to system Python.
- **Secrets:** Load from `.env` files using `python-dotenv`. Never hardcode secrets.
- **Key libraries:** yfinance, openpyxl, pandas, matplotlib

---

## How to Work — Agent Workflow

### Picking Up a Ticket

- Open `BACKLOG.md` and find the highest-priority `⬚ Open` ticket.
- Change its status to `🔵 In Progress`.
- Create a feature branch: `feature/T-XXX-short-description`
- Read the ticket's description and acceptance criteria carefully before writing code.
- If anything is ambiguous, mark the ticket `🟡 Blocked` and explain what needs clarification.

### Implementing

- Work only on what the ticket describes — no scope creep.
- Follow the project conventions below.
- Write tests alongside the implementation, not after.
- Run `ruff check .` and `pytest` before considering the work done.
- Every acceptance criterion checkbox must be satisfiable. Check them off as you go.

### Completing a Ticket

When all acceptance criteria are met:
1. Run `ruff check .` — fix any issues.
2. Run `pytest` — all tests must pass.
3. Update the ticket status in `BACKLOG.md` to `✅ Done`.
4. Add a completion note on the ticket describing what was built.
5. Append an entry to `docs/CHANGELOG.md`.
6. Append an entry to `docs/PROJECT_LOG.md`.
7. If you made an architectural decision, document it in `docs/DECISIONS.md`.
8. If you added or changed a major component, update `docs/ARCHITECTURE.md`.
9. Commit with a message referencing the ticket: `T-XXX: Add CSV export endpoint`

### If Something Goes Wrong

- If a ticket turns out to be more complex than expected, note this in the ticket and continue.
- If you discover a bug unrelated to your current ticket, add a new ticket to `BACKLOG.md` with type `Bug` — do not fix it now unless it blocks your current work.
- If you need to make an architectural change, document the decision in `docs/DECISIONS.md` before implementing it.

---

## Periodic Review — Maintenance Mode

When the PM asks for a "review pass" or "maintenance check," go through the codebase and look for:

### Bug Scan
- Check for unhandled exceptions, edge cases, and missing error handling.
- Look for logic errors or off-by-one issues.
- Verify that error messages are helpful and accurate.

### Consolidation
- Are there duplicate functions or similar logic that could be merged?
- Are there utility functions that should be extracted to `utils.py`?
- Is there copy-pasted code that should be a shared function?

### Improvements
- Are there functions that are too long or doing too many things?
- Are there missing docstrings on public functions?
- Are there hardcoded values that should be in `config.py`?
- Can any logic be simplified?

### Dead Code & Cleanup
- Are there unused imports, functions, or variables?
- Are there commented-out blocks of code that should be removed?
- Are there stale TODO comments that have been resolved?
- Are there test files without meaningful tests?

For each finding, create a ticket in `BACKLOG.md` with the appropriate type (Bug, Refactor, or Chore). Group small related cleanups into a single ticket rather than creating dozens of tiny ones.

---

## Project Log

After every session, append an entry to `docs/PROJECT_LOG.md` with:
- What was done
- Decisions made and why
- Next steps

**Never delete entries from the project log — append only.**

---

## Changelog

After making any meaningful change (new feature, bug fix, refactor, config change), append an entry to `docs/CHANGELOG.md`.

**Format:**

```markdown
## [YYYY-MM-DD]

### Added / Changed / Fixed / Removed
- Brief description of what changed and why
```

- Group entries under the correct heading (Added, Changed, Fixed, Removed).
- Use the current date.
- Keep descriptions concise — one line per change.
- Don't log trivial formatting or whitespace-only changes.

---

## Project Conventions

- **Python version**: 3.11+
- **Naming**: `snake_case` for files and functions, `PascalCase` for classes.
- **Linting**: Run `ruff check .` before committing. Fix issues, don't suppress them.
- **Commits**: Short imperative subject line referencing ticket: `T-XXX: Add CSV parser`
- **Branching**: Work on feature branches: `feature/T-XXX-short-description`
- **Data safety**: Never modify files in `data/raw/`. All generated output goes to `outputs/`.
- **Tests**: Run `pytest` after any code change. Add tests for new logic.
- **Dependencies**: `pyproject.toml` is the source of truth. Update `requirements.txt` with `pip freeze > requirements.txt` after adding packages.
- **Documentation**: Update `docs/ARCHITECTURE.md` when adding or changing components.

---

## File Layout

| Directory | Purpose |
|:----------|:--------|
| `src/tear_sheet/` | All application code |
| `tests/` | Pytest tests |
| `scripts/` | Entry points (e.g., `main.py`) |
| `data/raw/` | Reference data (read-only) — includes original class files |
| `data/processed/` | Intermediate outputs |
| `outputs/` | Final tear sheet Excel files |
| `docs/` | Architecture, changelog, decisions, project log |
| `scratch/` | Local only (gitignored) — quick experiments |
| `notebooks/` | Jupyter notebooks — the main deliverable notebook lives here |
| `BACKLOG.md` | Ticketing system — all tasks and their status |

---

## When Editing Code

- Keep functions short and focused.
- Add docstrings to public functions.
- Use `config.py` for magic numbers and thresholds.
- All test helpers and sample data live in test files, not in source modules.

---

## Running & Testing

```bash
# Run the project (from project root)
python scripts/main.py

# Run via notebook
jupyter notebook notebooks/tear_sheet.ipynb

# Run tests
pytest

# Lint
ruff check .
```
