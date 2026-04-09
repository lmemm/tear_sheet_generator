# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/).

## [2026-04-09]

### Added
- Initial project setup with full directory structure
- CLAUDE.md, BACKLOG.md, and all docs templates
- Reference files from original class work in data/raw/
- Detailed implementation tickets T-001 through T-010 in BACKLOG.md
- Full system design in ARCHITECTURE.md (data flow, Excel layout, component specs)
- Decision log entries for openpyxl, yfinance, and testing approach

## [2026-04-09] — Phase 1 Implementation

### Added
- `config.py` — all constants: yfinance field mappings, chart sizes, Excel layout, fonts/colors
- `scraper.py` — `get_company_data()` fetches info, income_stmt, balance_sheet, history, recommendations, analyst targets, calendar with graceful error handling
- `financials.py` — growth metrics (YoY revenue/net income, indexed revenue), return percentages (1Y/3Y/5Y), ratios, analyst upside calculation
- `charts.py` — price chart and revenue growth chart generation (Agg backend, BytesIO output)
- `utils.py` — formatting helpers for market cap (T/B/M), percentages, and currency
- `excel_builder.py` — full tear sheet assembly with 4 sections, embedded charts, styled headers, print-ready page setup
- `__init__.py` — `generate_tear_sheet()` orchestrator wiring all modules together
- `scripts/main.py` — CLI entry point with argparse
- `notebooks/tear_sheet.ipynb` — 14-cell class deliverable notebook
- 27 unit tests across utils, financials, charts, and excel_builder

### Fixed
- `pyproject.toml` build backend (`setuptools.backends._legacy:_Backend` → `setuptools.build_meta`)
- Excluded `data/raw/` from ruff linting (original class script has intentional bugs)
