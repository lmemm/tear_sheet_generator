# Project Log

Running history of this project. **Append only — never delete entries.**

Each entry records what was done, decisions made, and why.

---

## [2026-04-09] — Project Scaffolding

**What was done:**
- Created full project structure following standard Python project template
- Copied original class files (Stock Report Sheet Generator.py, Tear Sheet Class.xlsx) to data/raw/ as reference
- Filled in ARCHITECTURE.md with system design based on assignment requirements
- Set up all docs, config files, and empty module structure

**Decisions made:**
- Using openpyxl instead of xlwings for Excel output — see docs/DECISIONS.md
- Keeping yfinance as the data source (proven in class work)
- Structuring as a proper Python package in src/tear_sheet/ for reusability

**Next steps:**
- Plan the build — break work into backlog tickets
- Implement data scraping module first
- Build up to full tear sheet assembly
