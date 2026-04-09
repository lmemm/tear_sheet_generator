# Architecture

This document is the knowledge base for this project. It tells Claude (and future-you) how the system is designed so that any session can start productively without re-explaining context.

**Update this document** whenever you make a significant architectural decision, add a major component, or change how things connect.

---

## Overview

Tear Sheet Generator is a Python tool for a Python for Finance class that scrapes financial data from the internet (primarily via yfinance) and assembles it into a formatted, print-ready Excel tear sheet. The program generates a single-page company summary including overview info, financial data, stock performance charts, and valuation metrics. Deliverables are a Jupyter Notebook and the generated Excel file.

---

## Tech Stack

| Layer | Technology | Notes |
|:------|:-----------|:------|
| Language | Python 3.11+ | |
| Data source | yfinance | Primary data provider for stock/financial data |
| Excel output | openpyxl | Excel file creation and formatting |
| Data manipulation | pandas | DataFrames for financial data |
| Charting | matplotlib | Stock price charts embedded in Excel |
| Testing | pytest | |
| Linting | ruff | |

---

## System Components

### Component: Scraper
- **Location:** `src/tear_sheet/scraper.py`
- **Responsibility:** Fetch all raw data from yfinance (company info, financials, historical prices)
- **Depends on:** yfinance
- **Key functions/classes:**
  - `get_company_data(ticker)` — fetches and returns all data needed for the tear sheet

### Component: Financials
- **Location:** `src/tear_sheet/financials.py`
- **Responsibility:** Calculate financial metrics — revenue growth, net income growth, ratios
- **Depends on:** pandas
- **Key functions/classes:**
  - `calculate_growth_metrics(financials_df)` — computes growth rates
  - `calculate_return_percentages(history_df)` — computes 1yr/3yr/5yr returns

### Component: Charts
- **Location:** `src/tear_sheet/charts.py`
- **Responsibility:** Generate matplotlib charts (stock price, revenue growth, etc.)
- **Depends on:** matplotlib, pandas
- **Key functions/classes:**
  - `create_price_chart(history_df, ticker)` — stock price line chart
  - `create_revenue_chart(financials_df, ticker)` — revenue growth chart

### Component: Excel Builder
- **Location:** `src/tear_sheet/excel_builder.py`
- **Responsibility:** Assemble all data and charts into a formatted Excel tear sheet
- **Depends on:** openpyxl, Charts component
- **Key functions/classes:**
  - `build_tear_sheet(data, ticker, output_path)` — main assembly function

### Component: Config
- **Location:** `src/tear_sheet/config.py`
- **Responsibility:** Central configuration — cell positions, formatting constants, output paths

---

## Data Flow

```
User Input (ticker) → Scraper (yfinance API) → Raw Data Dict
                                                    │
                            ┌───────────────────────┼───────────────────────┐
                            ▼                       ▼                       ▼
                      Financials              Charts                  Company Info
                    (growth, ratios)    (price, revenue plots)     (name, sector, etc.)
                            │                       │                       │
                            └───────────────────────┼───────────────────────┘
                                                    ▼
                                            Excel Builder
                                                    │
                                                    ▼
                                        outputs/{TICKER}_tear_sheet.xlsx
```

---

## Tear Sheet Sections (Assignment Requirements)

1. **Company Overview** — name, ticker, industry, description, location, employees
2. **Financial Data** — revenue growth, net income growth, current ratio, quick ratio
3. **Stock Performance** — price chart, 1yr/3yr/5yr return percentages
4. **Valuation Data** — P/E ratio, 52-week high/low, market cap, analyst recommendations

---

## Configuration

| Variable | Purpose | Required | Default |
|:---------|:--------|:--------:|:--------|
| _(none currently)_ | yfinance doesn't require API keys | — | — |

---

## Constraints & Boundaries

- yfinance is an unofficial API — data availability varies by ticker
- Excel output must be print-ready on a single page (tear sheet format)
- The Jupyter notebook is a class deliverable — it should be clean and presentable
- Original class files in `data/raw/` are read-only references

---

## Known Limitations & Tech Debt

- yfinance can be rate-limited or return incomplete data for some tickers
- The original class script had bugs (typos in matplotlib calls) — these are fixed in the new implementation
