# Project Log

Running history of this project. **Append only — never delete entries.**

Each entry records what was done, decisions made, and why.

---

## [2026-04-09] — Project Scaffolding

**What was done:**
- Created full project structure following standard Python project template
- Copied original class files (Stock Report Sheet Generator.py, Tear Sheet Class.xlsx) to data/raw/ as reference
- Set up all docs, config files, and empty module structure
- Pushed to GitHub: https://github.com/lmemm/tear_sheet_generator

**Decisions made:**
- Using openpyxl instead of xlwings for Excel output (headless compatibility)
- Keeping yfinance as the data source (proven in class work)
- Structuring as a proper Python package in src/tear_sheet/ for reusability

**Next steps:**
- Plan the build — break work into backlog tickets

---

## [2026-04-09] — Build Planning Session

**What was done:**
- Researched yfinance data model — documented all available fields for company info, financials, stock history, analyst data
- Researched graph visualization options for future Obsidian-style graph view (Pyvis recommended)
- Designed 3-phase implementation plan:
  - Phase 1 (MVP): 4 tickets — Scraper+Config, Financials+Charts+Utils, Excel Builder+CLI, Jupyter Notebook
  - Phase 2: Email delivery, EDGAR integration (insider activity), FRED macro context
  - Phase 3: Graph view, peer comparison, watchlist mode, Alpaca integration
- Enriched tear sheet beyond assignment minimum: added debt-to-equity, beta, dividend yield, payout ratio, EPS, earnings dates, analyst upside %
- Wrote detailed tickets in BACKLOG.md with full implementation specs and acceptance criteria
- Updated ARCHITECTURE.md with complete system design including data flow and Excel layout

**Decisions made:**
- Demo ticker: CAT (Caterpillar) — aligns with user's infrastructure investing interest
- No mock data in tests — use real yfinance API calls for practical tool development
- BytesIO for chart images (no temp files, openpyxl accepts directly)
- matplotlib Agg backend is mandatory for headless compatibility
- generate_tear_sheet() lives in __init__.py as the single public API for CLI and notebook
- Layout driven by config constants — adjustable without touching builder logic
- Future data sources: EDGAR (insider activity, SEC filings), FRED (macro indicators), Alpaca (real-time data)

**Next steps:**
- Execute T-001 through T-004 (Phase 1 MVP)
- Assignment due soon — prioritize getting a working tool

---

## [2026-04-09] — Phase 1 Implementation (T-001 through T-004)

**What was done:**
- Implemented all 4 Phase 1 tickets: Scraper+Config, Financials+Charts+Utils, Excel Builder+CLI, Jupyter Notebook
- Fixed broken `pyproject.toml` build backend and set up virtual environment
- Wrote 27 unit tests covering utils, financials, charts, and excel builder (all passing)
- All code passes `ruff check .` lint
- Could not test live yfinance API calls — network access blocked in Claude Code Web environment

**Decisions made:**
- Used `PageSetupProperties` instead of `PrintPageSetup` for openpyxl's `pageSetUpPr` (ticket spec had wrong class)
- Return period calculation checks that history actually spans the period before computing return (prevents misleading partial-period returns)
- Excluded `data/raw/` from ruff config since original class script has intentional bugs we don't want to fix

**Next steps:**
- Run `python scripts/main.py CAT` locally to verify end-to-end with real data
- Run notebook with network access to populate output cells before class submission
- Fine-tune Excel layout spacing if needed after visual inspection
- Begin Phase 2 tickets (email delivery, EDGAR, FRED) when ready
