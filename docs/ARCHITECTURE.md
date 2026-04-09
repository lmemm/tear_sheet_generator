# Architecture

This document is the knowledge base for this project. It tells Claude (and future-you) how the system is designed so that any session can start productively without re-explaining context.

**Update this document** whenever you make a significant architectural decision, add a major component, or change how things connect.

---

## Overview

Tear Sheet Generator is a Python tool that scrapes financial data from the internet (primarily via yfinance) and assembles it into a formatted, print-ready Excel tear sheet. It generates a single-page company summary including overview info, financial data with growth metrics, stock performance charts and returns, and valuation metrics with analyst data. Built for a Python for Finance class assignment but designed as a lasting personal investing/research tool.

---

## Tech Stack

| Layer | Technology | Notes |
|:------|:-----------|:------|
| Language | Python 3.11+ | |
| Data source (Phase 1) | yfinance | Stock data, financials, analyst data. No API key needed. |
| Data source (Phase 2) | EDGAR | SEC filings, insider activity. API key needed. |
| Data source (Phase 2) | FRED | Macroeconomic indicators. API key needed. |
| Data source (Phase 3) | Alpaca API | Real-time pricing, paper trading. User has account. |
| Excel output | openpyxl | Creates .xlsx without Excel installed (headless-compatible) |
| Data manipulation | pandas | DataFrames for financial data |
| Charting | matplotlib | Stock price/revenue charts, uses Agg backend for headless |
| Graph viz (Phase 3) | pyvis + networkx | Interactive HTML graph view |
| Testing | pytest | Real data, no mocks |
| Linting | ruff | |

---

## System Components

### Component: Config
- **Location:** `src/tear_sheet/config.py`
- **Responsibility:** Central configuration — paths, yfinance field mappings, chart sizes, Excel layout constants, formatting specs
- **Key exports:** `PROJECT_ROOT`, `OUTPUT_DIR`, `YFINANCE_INFO_FIELDS`, `RETURN_PERIODS`, chart size/DPI constants, Excel formatting constants

### Component: Scraper
- **Location:** `src/tear_sheet/scraper.py`
- **Responsibility:** Fetch all raw data from yfinance — single point of contact with the API
- **Depends on:** yfinance, config (for field mappings)
- **Key functions:**
  - `get_company_data(ticker: str) -> dict` — returns info, income_stmt, balance_sheet, history, recommendations, analyst_targets, calendar

### Component: Financials
- **Location:** `src/tear_sheet/financials.py`
- **Responsibility:** Calculate derived financial metrics from raw data
- **Depends on:** pandas
- **Key functions:**
  - `calculate_growth_metrics(income_stmt)` — YoY revenue/net income growth + indexed revenue series
  - `calculate_return_percentages(history)` — 1Y/3Y/5Y stock returns
  - `calculate_ratios(data)` — current ratio, quick ratio, debt-to-equity
  - `calculate_analyst_upside(data)` — % upside to mean analyst target

### Component: Charts
- **Location:** `src/tear_sheet/charts.py`
- **Responsibility:** Generate matplotlib charts as in-memory PNG images (BytesIO)
- **Depends on:** matplotlib (Agg backend), config (for chart sizes)
- **Key functions:**
  - `create_price_chart(history, ticker) -> BytesIO` — 5yr stock price line chart
  - `create_revenue_chart(income_stmt, ticker) -> BytesIO` — indexed revenue growth chart

### Component: Utils
- **Location:** `src/tear_sheet/utils.py`
- **Responsibility:** Shared formatting helpers
- **Key functions:**
  - `format_market_cap(value)` — "$1.23T" / "$456B" / "$12M"
  - `format_percentage(value)` — "15.6%" or "N/A"
  - `format_currency(value)` — "$123.45" or "N/A"

### Component: Excel Builder
- **Location:** `src/tear_sheet/excel_builder.py`
- **Responsibility:** Assemble all data and charts into a formatted, print-ready Excel tear sheet
- **Depends on:** openpyxl, config (for layout constants), utils (for formatting)
- **Key functions:**
  - `build_tear_sheet(data, financials, charts, output_path) -> Path`
  - `_write_section_header()`, `_write_label_value()`, `_apply_page_setup()`

### Component: Orchestrator
- **Location:** `src/tear_sheet/__init__.py`
- **Responsibility:** Wire together the full pipeline (scraper → financials → charts → builder)
- **Key functions:**
  - `generate_tear_sheet(ticker, output_dir=None) -> Path` — the public API, used by both CLI and notebook

### Component: CLI
- **Location:** `scripts/main.py`
- **Responsibility:** Command-line entry point with argparse
- **Usage:** `python scripts/main.py CAT` or `python scripts/main.py CAT -o /custom/path`

---

## Data Flow

```
User Input (ticker string)
        │
        ▼
   Scraper (yfinance API)
        │
        ▼
   Raw Data Dict ─────────────────────────────────────────┐
        │                                                  │
        ├──► Financials Module                             │
        │     ├── calculate_growth_metrics()               │
        │     ├── calculate_return_percentages()           │
        │     ├── calculate_ratios()                       │
        │     └── calculate_analyst_upside()               │
        │              │                                   │
        ├──► Charts Module                                 │
        │     ├── create_price_chart() → BytesIO PNG       │
        │     └── create_revenue_chart() → BytesIO PNG     │
        │              │                                   │
        └──────────────┼───────────────────────────────────┘
                       │
                       ▼
              Excel Builder (openpyxl)
                       │
                       ▼
            outputs/{TICKER}_tear_sheet.xlsx
```

---

## Tear Sheet Layout (4 Sections, Single Page)

```
┌─────────────────────────────────────────────────────────────┐
│  COMPANY NAME                                    TICKER     │
├─────────────────────────────────────────────────────────────┤
│  COMPANY OVERVIEW                                           │
│  Industry | Sector | Location | Employees                   │
│  Business description...                                    │
├──────────────────────────────┬──────────────────────────────┤
│  FINANCIAL DATA              │  STOCK PERFORMANCE           │
│  [Revenue Growth Chart]      │  [Price Chart]               │
│  Revenue YoY growth values   │  1Y / 3Y / 5Y Returns       │
│  Net Income YoY growth       │  Beta                        │
│  Current / Quick Ratio       │  Dividend Yield / Payout     │
│  Debt-to-Equity              │                              │
├──────────────────────────────┴──────────────────────────────┤
│  VALUATION                                                  │
│  Forward P/E | Trailing P/E | 52-Wk High/Low | Market Cap  │
│  EPS (Trailing/Forward) | Analyst Rec + Target + Upside %   │
│  Next Earnings Date                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Configuration

| Variable | Purpose | Required | Default |
|:---------|:--------|:--------:|:--------|
| _(none for Phase 1)_ | yfinance needs no API key | — | — |
| `EDGAR_API_KEY` | SEC EDGAR access (Phase 2) | Phase 2 | — |
| `FRED_API_KEY` | FRED data access (Phase 2) | Phase 2 | — |
| `SMTP_EMAIL` | Bot email for sending reports (Phase 2) | Phase 2 | — |
| `SMTP_PASSWORD` | Bot email app password (Phase 2) | Phase 2 | — |
| `ALPACA_API_KEY` | Alpaca market data (Phase 3) | Phase 3 | — |

---

## Constraints & Boundaries

- yfinance is an unofficial API — data availability varies by ticker, some fields may be None
- Excel output must be print-ready on a single page (landscape, letter, fit-to-one-page)
- `matplotlib.use("Agg")` must be set before importing pyplot — required for headless environments
- Charts are BytesIO PNGs in memory — no temp files on disk
- All functions must handle None/missing data gracefully — display "N/A", never crash
- The Jupyter notebook is a class deliverable — must be clean and pre-run with CAT data
- Original class files in `data/raw/` are read-only references
- No mock data in tests — use real yfinance API calls

---

## Known Limitations & Tech Debt

- yfinance can be rate-limited or return incomplete data for some tickers
- Analyst data (recommendations, price targets) is not available for all tickers
- Calendar/earnings dates may be empty for some companies
- The original class script at `data/raw/Stock_Report_Sheet_Generator_original.py` had bugs (typo `flt.figure` instead of `plt.figure`, `figsize - (4,2)` instead of `figsize=(4,2)`, unquoted cell reference `A11.left`) — these are fixed in the new implementation
