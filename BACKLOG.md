# Backlog

This is the project's ticketing system. Each ticket is a unit of work that Claude can pick up and execute independently.

**Rules:**
- Tickets are worked in priority order (top = highest priority) unless the PM specifies otherwise.
- Only one ticket should be in `🔵 In Progress` at a time.
- When you pick up a ticket, change its status to `🔵 In Progress`.
- When you finish a ticket, change its status to `✅ Done` and add a completion note.
- If a ticket is blocked or needs PM input, change its status to `🟡 Blocked` and explain why.
- Never delete tickets — mark them `❌ Won't Do` with a reason if they're cancelled.

**Statuses:** `⬚ Open` → `🔵 In Progress` → `✅ Done` | `🟡 Blocked` | `❌ Won't Do`

---

## Active Tickets

### T-001: Scraper + Config
- **Status:** ⬚ Open
- **Priority:** P1
- **Type:** Feature
- **Description:** Build the config module with all constants and the scraper module that fetches all raw data from yfinance. This is the foundation — every other module depends on it.
- **Files:** `src/tear_sheet/config.py`, `src/tear_sheet/scraper.py`

**config.py — populate with:**
- `PROJECT_ROOT`, `OUTPUT_DIR`, `DATA_DIR` (already stubbed)
- `YFINANCE_INFO_FIELDS` dict mapping human-readable names to yfinance `stock.info` keys:
  - `company_name` → `shortName`, `ticker` → `symbol`, `sector` → `sector`, `industry` → `industry`, `description` → `longBusinessSummary`, `city` → `city`, `state` → `state`, `employees` → `fullTimeEmployees`
  - `forward_pe` → `forwardPE`, `trailing_pe` → `trailingPE`, `market_cap` → `marketCap`
  - `fifty_two_week_high` → `fiftyTwoWeekHigh`, `fifty_two_week_low` → `fiftyTwoWeekLow`
  - `current_ratio` → `currentRatio`, `quick_ratio` → `quickRatio`, `debt_to_equity` → `debtToEquity`
  - `beta` → `beta`, `dividend_yield` → `dividendYield`, `payout_ratio` → `payoutRatio`
  - `trailing_eps` → `trailingEps`, `forward_eps` → `forwardEps`
  - `recommendation_key` → `recommendationKey`, `current_price` → `currentPrice`
- `HISTORY_PERIOD = "5y"`
- `RETURN_PERIODS = {"1Y": 252, "3Y": 756, "5Y": 1260}` (trading days)
- Chart config: `PRICE_CHART_SIZE = (7, 3)`, `REVENUE_CHART_SIZE = (5, 2.5)`, `CHART_DPI = 150`
- Excel section row positions (starting rows for each of the 4 sections)
- Column width dict
- Page setup constants (landscape, letter, fit-to-one-page)
- Font/color constants for section headers (dark blue bg, white text), labels, values

**scraper.py — `get_company_data(ticker: str) -> dict`:**
- Create `yf.Ticker(ticker)` and fetch:
  - `stock.info` — filter to only the fields in `YFINANCE_INFO_FIELDS`. Use `.get()` for each key so missing fields return `None` instead of KeyError.
  - `stock.income_stmt` — the annual income statement DataFrame. Known quirk: the last column may have all NaN values (the original class script checks `if pd.isnull(df.loc["Total Revenue", col_names[-1]])` and drops it). Sort columns chronologically (oldest → newest).
  - `stock.balance_sheet` — annual balance sheet DataFrame
  - `stock.history(period="5y")` — daily OHLCV DataFrame with DatetimeIndex
  - `stock.recommendations` — analyst recommendation DataFrame (may be empty/None for some tickers)
  - `stock.analyst_price_targets` — dict/Series with `current`, `low`, `mean`, `median`, `high` (wrap in try/except, may not exist for all tickers)
  - `stock.calendar` — earnings dates (wrap in try/except)
- Return structure:
  ```python
  {
      "info": { ... },              # filtered dict, missing fields = None
      "income_stmt": pd.DataFrame,  # or None if unavailable
      "balance_sheet": pd.DataFrame,# or None if unavailable
      "history": pd.DataFrame,      # 5yr OHLCV
      "recommendations": ...,       # DataFrame or None
      "analyst_targets": ...,       # dict or None
      "calendar": ...,              # dict or None
      "ticker": str,                # normalized to uppercase
      "fetch_date": str,            # today's date ISO format
  }
  ```
- If ticker is invalid (stock.info is empty or has no `shortName`), raise `ValueError(f"Invalid ticker: {ticker}")`
- Handle individual data source failures gracefully — if income_stmt fails, set to `None` and continue

- **Acceptance criteria:**
  - [ ] `config.py` exports all constants listed above
  - [ ] `get_company_data("CAT")` returns a dict with all expected keys
  - [ ] `get_company_data("CAT")["info"]` contains all fields from YFINANCE_INFO_FIELDS (or None for missing)
  - [ ] Income statement columns are sorted chronologically (oldest → newest)
  - [ ] NaN trailing column on income_stmt is dropped if present
  - [ ] `get_company_data("INVALIDTICKER123")` raises ValueError
  - [ ] Individual data source failures don't crash the whole fetch
  - [ ] `ruff check .` passes
- **Notes:** Reference the original class script at `data/raw/Stock_Report_Sheet_Generator_original.py` for the field mappings and the income_stmt NaN fix pattern.
- **Completion note:**

---

### T-002: Financials + Charts + Utils
- **Status:** ⬚ Open
- **Priority:** P1
- **Type:** Feature
- **Description:** Build the financial calculations module, chart generation module, and shared utility functions. These take raw data from the scraper and produce computed metrics and chart images ready for the Excel builder.
- **Files:** `src/tear_sheet/financials.py`, `src/tear_sheet/charts.py`, `src/tear_sheet/utils.py`

**financials.py:**

`calculate_growth_metrics(income_stmt: pd.DataFrame | None) -> dict`:
- If income_stmt is None, return `{"revenue_yoy": {}, "revenue_indexed": None, "net_income_yoy": {}}`
- Revenue YoY growth: for each consecutive pair of years, `(new - old) / abs(old)`. Return dict of `{year_label: pct_change}` (e.g., `{"2022→2023": 0.15, "2023→2024": 0.08}`)
- Revenue indexed: normalize all Total Revenue values so first year = 1.0. Return as a pandas Series. This is what gets plotted in the revenue chart (same approach as original class script: `df['Total Revenue']/df.loc[df.index[0], 'Total Revenue']`)
- Net Income YoY growth: same calculation as revenue but for Net Income row

`calculate_return_percentages(history: pd.DataFrame | None) -> dict`:
- If history is None or empty, return `{"1Y": None, "3Y": None, "5Y": None}`
- For each period (1Y, 3Y, 5Y): find the Close price at the start and end of the period
- Use calendar dates with `pd.DateOffset(years=N)` to find the target date, then use `.iloc` with nearest index lookup
- If history doesn't go back far enough for a period, return None for that period
- Return: `{"1Y": 0.156, "3Y": 0.432, "5Y": 0.891}` (as decimals, formatted later)

`calculate_ratios(data: dict) -> dict`:
- Pull from `data["info"]`: current_ratio, quick_ratio, debt_to_equity
- Return: `{"current_ratio": value, "quick_ratio": value, "debt_to_equity": value}` (None for missing)

`calculate_analyst_upside(data: dict) -> float | None`:
- If `data["analyst_targets"]` is None or `data["info"]["current_price"]` is None, return None
- `(mean_target - current_price) / current_price` → e.g., 0.12 means 12% upside

**charts.py:**

IMPORTANT: At the top of the file, before any other matplotlib import:
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
```
This is required for headless environments (Claude Code Web). Non-negotiable.

`create_price_chart(history: pd.DataFrame, ticker: str) -> BytesIO`:
- Plot `Close` column over time as a line chart
- Use `PRICE_CHART_SIZE` from config for figsize
- Title: `f"{ticker} Stock Price (5Y)"`
- Clean styling: remove top/right spines, light grid, reasonable fonts
- Save to `BytesIO()`: `fig.savefig(buf, format="png", dpi=CHART_DPI, bbox_inches="tight")`
- `buf.seek(0)` then return buf
- `plt.close(fig)` to prevent memory leaks

`create_revenue_chart(income_stmt: pd.DataFrame, ticker: str) -> BytesIO`:
- Plot indexed revenue (revenue / first year's revenue) — this matches the original class script approach
- Use `REVENUE_CHART_SIZE` from config
- Title: `f"{ticker} Revenue Growth"`
- X-tick rotation: 35 degrees
- Same BytesIO/Agg/close pattern as price chart

**utils.py:**

`format_market_cap(value: float | None) -> str`:
- Use numeric thresholds (NOT string length like the original class script — that approach is fragile):
  - `>= 1e12` → `f"${value/1e12:.2f}T"`
  - `>= 1e9` → `f"${value/1e9:.2f}B"`
  - `>= 1e6` → `f"${value/1e6:.2f}M"`
- If None → `"N/A"`

`format_percentage(value: float | None) -> str`:
- `f"{value * 100:.1f}%"` or `"N/A"` if None

`format_currency(value: float | None) -> str`:
- `f"${value:,.2f}"` or `"N/A"` if None

- **Acceptance criteria:**
  - [ ] `calculate_growth_metrics` returns YoY revenue and net income growth dicts + indexed revenue Series
  - [ ] `calculate_return_percentages` returns 1Y/3Y/5Y returns as decimals (or None if insufficient data)
  - [ ] `calculate_ratios` returns current ratio, quick ratio, debt-to-equity
  - [ ] `calculate_analyst_upside` returns upside % or None
  - [ ] `create_price_chart` returns a BytesIO containing valid PNG data (starts with `b'\x89PNG'`)
  - [ ] `create_revenue_chart` returns a BytesIO containing valid PNG data
  - [ ] Charts use Agg backend (no GUI dependency)
  - [ ] `plt.close(fig)` called after every chart save
  - [ ] `format_market_cap` correctly handles T/B/M tiers and None
  - [ ] All functions handle None/empty inputs without crashing
  - [ ] `ruff check .` passes
  - [ ] Verify by running: fetch CAT data with scraper, pass to these functions, confirm outputs
- **Notes:** The indexed revenue approach is from the original class script at `data/raw/Stock_Report_Sheet_Generator_original.py` line 44.
- **Completion note:**

---

### T-003: Excel Builder + CLI
- **Status:** ⬚ Open
- **Priority:** P1
- **Type:** Feature
- **Description:** Build the Excel assembly module that formats all data and charts into a print-ready tear sheet, the orchestration function in `__init__.py`, and the CLI entry point. This is the largest ticket — it wires everything together.
- **Files:** `src/tear_sheet/excel_builder.py`, `src/tear_sheet/__init__.py`, `scripts/main.py`

**excel_builder.py — `build_tear_sheet(data, financials, charts, output_path) -> Path`:**

Parameters:
- `data` — raw data dict from scraper
- `financials` — dict with keys: `growth` (from calculate_growth_metrics), `returns` (from calculate_return_percentages), `ratios` (from calculate_ratios), `analyst_upside` (from calculate_analyst_upside)
- `charts` — dict with keys: `price_chart` (BytesIO), `revenue_chart` (BytesIO)
- `output_path` — Path where to save .xlsx

Create a single worksheet with 4 sections. Use openpyxl throughout.

**Section 1: Company Overview (rows ~1-9)**
- Row 1: Company name in A1 (merge across ~A1:P1, large bold font 16pt), Ticker symbol right-aligned in column R (bold)
- Row 3: Section header "COMPANY OVERVIEW" — full-width colored bar (dark blue background `4472C4`, white bold text)
- Row 4: `Industry:` label + value | `Sector:` label + value
- Row 5: `Location:` label + city, state value | `Employees:` label + value (formatted with commas)
- Rows 6-9: `Description:` label + business description (merge across multiple columns, `Alignment(wrap_text=True, vertical="top")`)

**Section 2: Financial Data (rows ~10-22)**
- Row 10: Section header "FINANCIAL DATA" (same colored bar style)
- Rows 11-16: Revenue growth chart image — embed using `openpyxl.drawing.image.Image(charts["revenue_chart"])`, set width/height in pixels, place with `ws.add_image(img, "A11")`
- Row 17: Revenue Growth (YoY) label + values for each available year (e.g., "2021→2022: 15.3%  2022→2023: 8.1%")
- Row 18: Net Income Growth (YoY) label + values
- Row 19: `Current Ratio:` + value | `Quick Ratio:` + value
- Row 20: `Debt-to-Equity:` + value

**Section 3: Stock Performance (rows ~23-36)**
- Row 23: Section header "STOCK PERFORMANCE" (colored bar)
- Rows 24-30: Price chart image (same embed approach, larger image)
- Row 31: `1-Year Return:` + formatted % | `3-Year Return:` + formatted % | `5-Year Return:` + formatted %
- Row 32: `Beta:` + value
- Row 33: `Dividend Yield:` + formatted % | `Payout Ratio:` + formatted %

**Section 4: Valuation Data (rows ~37-44)**
- Row 37: Section header "VALUATION" (colored bar)
- Row 38: `Forward P/E:` + value | `Trailing P/E:` + value
- Row 39: `52-Week High:` + formatted $ | `52-Week Low:` + formatted $
- Row 40: `Market Cap:` + formatted (T/B/M)
- Row 41: `Trailing EPS:` + formatted $ | `Forward EPS:` + formatted $
- Row 42: `Analyst Recommendation:` + value (e.g., "Buy") | `Mean Price Target:` + formatted $
- Row 43: `Upside/Downside:` + formatted % (color green if positive, red if negative)
- Row 44: `Next Earnings Date:` + date string

**Formatting details:**
- Section headers: `Font(name="Calibri", size=12, bold=True, color="FFFFFF")`, `PatternFill(start_color="4472C4", fill_type="solid")`, merge across full width
- Labels: `Font(name="Calibri", size=10, bold=True)`
- Values: `Font(name="Calibri", size=10)`
- Column widths: set A-R to reasonable widths (A=3, B=12, C-R=10-12 each, adjust as needed)
- All label cells right-aligned, value cells left-aligned
- Missing data: display "N/A" — never leave cells empty or crash

**Page setup (critical for "print-ready" requirement):**
```python
ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 1
ws.sheet_properties.pageSetUpPr = PrintPageSetup()
ws.sheet_properties.pageSetUpPr.fitToPage = True
```

**Helper functions within module:**
- `_write_section_header(ws, row, title, end_col)` — merges, styles, writes header
- `_write_label_value(ws, row, label_col, label, value_col, value)` — writes label in one cell, value in adjacent
- `_apply_page_setup(ws)` — sets orientation, paper, fit-to-page, margins

Save with `wb.save(output_path)`, return the path.

**`src/tear_sheet/__init__.py` — `generate_tear_sheet(ticker, output_dir=None) -> Path`:**
```python
def generate_tear_sheet(ticker: str, output_dir: Path | None = None) -> Path:
    ticker = ticker.upper().strip()
    output_dir = output_dir or OUTPUT_DIR
    output_path = output_dir / f"{ticker}_tear_sheet.xlsx"

    print(f"Fetching data for {ticker}...")
    data = get_company_data(ticker)

    print("Calculating financial metrics...")
    growth = calculate_growth_metrics(data["income_stmt"])
    returns = calculate_return_percentages(data["history"])
    ratios = calculate_ratios(data)
    analyst_upside = calculate_analyst_upside(data)
    financials = {"growth": growth, "returns": returns, "ratios": ratios, "analyst_upside": analyst_upside}

    print("Generating charts...")
    charts_dict = {}
    if data["income_stmt"] is not None:
        charts_dict["revenue_chart"] = create_revenue_chart(data["income_stmt"], ticker)
    if data["history"] is not None:
        charts_dict["price_chart"] = create_price_chart(data["history"], ticker)

    print("Building Excel tear sheet...")
    result_path = build_tear_sheet(data, financials, charts_dict, output_path)

    print(f"Tear sheet saved to: {result_path}")
    return result_path
```

**`scripts/main.py` — CLI:**
- `sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))` at top for import resolution
- argparse: positional `ticker` arg, optional `-o`/`--output` for output dir
- Call `generate_tear_sheet(ticker, output_dir)`
- Wrap in try/except: catch ValueError for invalid tickers, print user-friendly message

- **Acceptance criteria:**
  - [ ] `python scripts/main.py CAT` produces `outputs/CAT_tear_sheet.xlsx`
  - [ ] `python scripts/main.py AAPL` produces `outputs/AAPL_tear_sheet.xlsx`
  - [ ] Excel file has all 4 sections with data populated
  - [ ] Charts are visible as embedded images in the Excel file
  - [ ] Section headers have colored backgrounds and white bold text
  - [ ] Page setup is landscape, letter, fit-to-one-page
  - [ ] Opening the file in Excel/Numbers and doing Print Preview shows it fits on one page
  - [ ] Missing data shows "N/A" — never empty cells or crashes
  - [ ] Invalid ticker prints a clear error (not a stack trace)
  - [ ] `ruff check .` passes
- **Notes:** The Excel layout is the most subjective part. Get it working first, then fine-tune spacing and column widths visually. The row numbers above are approximate — adjust as needed so everything fits on one page.
- **Completion note:**

---

### T-004: Jupyter Notebook Deliverable
- **Status:** ⬚ Open
- **Priority:** P1
- **Type:** Feature
- **Description:** Create a clean, presentable Jupyter notebook that serves as the class deliverable. It should walk through the process step by step, show code working with real data, display inline charts, and produce the Excel output. Demo company: CAT (Caterpillar).
- **Files:** `notebooks/tear_sheet.ipynb`

**Notebook cell structure:**

Cell 1 — Markdown title:
```markdown
# Tear Sheet Generator
**Author:** Landon Memmott
**Date:** April 2026
**Course:** Python for Finance

A program that scrapes financial data from the internet and generates a print-ready Excel tear sheet for any publicly traded company.
```

Cell 2 — Code (setup):
```python
import sys
sys.path.insert(0, "../src")

from tear_sheet import generate_tear_sheet
from tear_sheet.scraper import get_company_data
from tear_sheet.financials import (
    calculate_growth_metrics,
    calculate_return_percentages,
    calculate_ratios,
    calculate_analyst_upside,
)
from tear_sheet.charts import create_price_chart, create_revenue_chart
from tear_sheet.utils import format_market_cap, format_percentage, format_currency

import pandas as pd
%matplotlib inline
```

Cell 3 — Markdown:
```markdown
## 1. Data Collection
We use the `yfinance` library to fetch company information, financial statements, historical stock prices, and analyst data.
```

Cell 4 — Code:
```python
ticker = "CAT"
data = get_company_data(ticker)
print(f"Company: {data['info']['company_name']}")
print(f"Sector: {data['info']['sector']}")
print(f"Industry: {data['info']['industry']}")
print(f"Employees: {data['info']['employees']:,}")
print(f"\nDescription: {data['info']['description'][:200]}...")
```

Cell 5 — Code:
```python
# Display recent income statement
data["income_stmt"].head()
```

Cell 6 — Markdown:
```markdown
## 2. Financial Analysis
We calculate key financial metrics including revenue growth, stock returns, and financial ratios.
```

Cell 7 — Code:
```python
growth = calculate_growth_metrics(data["income_stmt"])
returns = calculate_return_percentages(data["history"])
ratios = calculate_ratios(data)
upside = calculate_analyst_upside(data)

print("Revenue Growth (YoY):")
for period, pct in growth["revenue_yoy"].items():
    print(f"  {period}: {format_percentage(pct)}")

print(f"\nStock Returns:")
for period, ret in returns.items():
    print(f"  {period}: {format_percentage(ret)}")

print(f"\nFinancial Ratios:")
print(f"  Current Ratio: {ratios['current_ratio']}")
print(f"  Quick Ratio: {ratios['quick_ratio']}")
print(f"  Debt-to-Equity: {ratios['debt_to_equity']}")

print(f"\nAnalyst Upside: {format_percentage(upside)}")
```

Cell 8 — Markdown:
```markdown
## 3. Visualization
Stock price history and revenue growth charts.
```

Cell 9 — Code:
```python
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image as PILImage

# Price chart
buf = create_price_chart(data["history"], ticker)
img = PILImage.open(buf)
plt.figure(figsize=(8, 3.5))
plt.imshow(img)
plt.axis("off")
plt.show()
```

Cell 10 — Code:
```python
# Revenue chart
buf = create_revenue_chart(data["income_stmt"], ticker)
img = PILImage.open(buf)
plt.figure(figsize=(6, 3))
plt.imshow(img)
plt.axis("off")
plt.show()
```

Cell 11 — Markdown:
```markdown
## 4. Generate Tear Sheet
Assemble all data and charts into a formatted Excel tear sheet.
```

Cell 12 — Code:
```python
output_path = generate_tear_sheet(ticker)
print(f"\nTear sheet saved to: {output_path}")
```

Cell 13 — Markdown:
```markdown
## 5. Try Another Company
Change the ticker below to generate a tear sheet for any publicly traded company.
```

Cell 14 — Code:
```python
another_ticker = "AAPL"  # Change this to any ticker
output_path = generate_tear_sheet(another_ticker)
print(f"Tear sheet saved to: {output_path}")
```

**Important:**
- The notebook must be pre-run with output cells populated (the professor sees the rendered output)
- Use `%matplotlib inline` for in-notebook chart display
- No raw error outputs or stack traces should be visible
- Keep markdown cells well-written — this is being graded
- Add `Pillow` to requirements.txt if needed for displaying chart BytesIO in notebook (or display charts differently by calling matplotlib directly instead of going through the BytesIO → PIL path)

- **Acceptance criteria:**
  - [ ] Notebook exists at `notebooks/tear_sheet.ipynb`
  - [ ] Notebook runs end-to-end without errors
  - [ ] All sections have explanatory markdown cells
  - [ ] Charts display inline in the notebook
  - [ ] Final cells produce .xlsx files in `outputs/`
  - [ ] Notebook is clean and presentable (no debug output, no stack traces)
  - [ ] Author and course info in the header
  - [ ] `ruff check .` passes
- **Notes:** For the inline chart display, an alternative to the PIL approach is to just call matplotlib directly in the notebook (e.g., call the same plotting code but use `plt.show()` instead of saving to BytesIO). Choose whichever approach is cleaner. The BytesIO path proves the same images going into Excel, but the direct matplotlib path is simpler.
- **Completion note:**

---

## Future Tickets (Phase 2+)

_These will be broken into detailed tickets after Phase 1 is complete._

### T-005: Email Delivery
- **Status:** ⬚ Open
- **Priority:** P2
- **Type:** Feature
- **Description:** Add email delivery using user's existing Python bot email account. New module `src/tear_sheet/emailer.py` with stdlib smtplib. Credentials in `.env`. CLI flag: `--email`.

### T-006: EDGAR Integration — Insider Activity + Filings
- **Status:** ⬚ Open
- **Priority:** P2
- **Type:** Feature
- **Description:** Pull insider buy/sell transactions and links to recent 10-K/10-Q filings from SEC EDGAR. Add as a new section on the tear sheet. API key setup required.

### T-007: FRED Macro Context
- **Status:** ⬚ Open
- **Priority:** P2
- **Type:** Feature
- **Description:** Add macroeconomic context section to tear sheet. Pull relevant indicators from FRED (construction spending, interest rates, industrial production for infrastructure companies). API key setup required.

### T-008: Company Registry + Graph View
- **Status:** ⬚ Open
- **Priority:** P3
- **Type:** Feature
- **Description:** Auto-populate a company registry (`data/processed/company_registry.json`) every time a tear sheet is generated. Build an interactive Obsidian-style graph view using NetworkX + Pyvis showing sector clusters and company relationships. Support manual relationship tagging via CLI.

### T-009: Peer Comparison Mode
- **Status:** ⬚ Open
- **Priority:** P3
- **Type:** Feature
- **Description:** Add `--peers DE URI VMC` flag to generate a comparison sheet alongside the main tear sheet. Side-by-side metrics for the target company and its peers.

### T-010: Watchlist + Batch Mode
- **Status:** ⬚ Open
- **Priority:** P3
- **Type:** Feature
- **Description:** Define a watchlist of tickers (JSON or CLI args) and batch-generate tear sheets for all of them in one command.

---

## Completed Tickets

_(Move completed tickets here to keep the Active section clean)_

---

## Ticket Template

Copy this when creating new tickets:

```markdown
### T-XXX: [Title]
- **Status:** ⬚ Open
- **Priority:** P1 / P2 / P3
- **Type:** Feature / Bug / Refactor / Chore
- **Description:**
- **Acceptance criteria:**
  - [ ]
  - [ ] Tests pass
- **Files likely involved:**
- **Notes:**
- **Completion note:**
```
