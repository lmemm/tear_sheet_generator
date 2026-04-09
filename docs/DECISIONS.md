# Decisions

Key architectural and design decisions, recorded so Future-You knows *why*.

## [2026-04-09] — openpyxl over xlwings for Excel output

**Context:** The original class script used xlwings to write to Excel. Need to choose an Excel library for the new implementation.

**Decision:** Use openpyxl instead of xlwings.

**Why:** openpyxl creates .xlsx files directly without needing Excel installed. This means the code works on Claude Code Web, CI environments, and any machine. xlwings requires a running Excel application, which limits portability. openpyxl also has strong formatting support for creating print-ready layouts.

**Alternatives considered:**
- xlwings — rejected because it requires Excel to be installed and running; doesn't work in headless environments like Claude Code Web
- XlsxWriter — viable alternative but openpyxl has better read/write support if we need to use templates later

## [2026-04-09] — yfinance as primary data source

**Context:** Need a source for stock/financial data.

**Decision:** Use yfinance.

**Why:** Already proven in class work, free, no API key needed, provides all required data (company info, financials, historical prices, analyst recommendations). Good enough for an academic project.

**Alternatives considered:**
- Alpha Vantage — requires API key, rate limits on free tier
- Financial Modeling Prep — requires API key
- Web scraping Yahoo Finance directly — fragile, breaks when HTML changes
