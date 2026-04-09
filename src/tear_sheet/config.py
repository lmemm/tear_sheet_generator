"""Central configuration for the tear sheet generator."""

from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"
DATA_DIR = PROJECT_ROOT / "data"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# yfinance field mappings  (human-readable name → stock.info key)
# ---------------------------------------------------------------------------
YFINANCE_INFO_FIELDS = {
    # Company overview
    "company_name": "shortName",
    "ticker": "symbol",
    "sector": "sector",
    "industry": "industry",
    "description": "longBusinessSummary",
    "city": "city",
    "state": "state",
    "employees": "fullTimeEmployees",
    # Valuation
    "forward_pe": "forwardPE",
    "trailing_pe": "trailingPE",
    "market_cap": "marketCap",
    "fifty_two_week_high": "fiftyTwoWeekHigh",
    "fifty_two_week_low": "fiftyTwoWeekLow",
    # Ratios
    "current_ratio": "currentRatio",
    "quick_ratio": "quickRatio",
    "debt_to_equity": "debtToEquity",
    # Risk / return
    "beta": "beta",
    "dividend_yield": "dividendYield",
    "payout_ratio": "payoutRatio",
    # Earnings
    "trailing_eps": "trailingEps",
    "forward_eps": "forwardEps",
    # Analyst
    "recommendation_key": "recommendationKey",
    "current_price": "currentPrice",
}

# ---------------------------------------------------------------------------
# History & return periods
# ---------------------------------------------------------------------------
HISTORY_PERIOD = "5y"
RETURN_PERIODS = {"1Y": 252, "3Y": 756, "5Y": 1260}  # trading days

# ---------------------------------------------------------------------------
# Chart settings
# ---------------------------------------------------------------------------
PRICE_CHART_SIZE = (7, 3)
REVENUE_CHART_SIZE = (5, 2.5)
CHART_DPI = 150

# ---------------------------------------------------------------------------
# Excel layout — section starting rows
# Spacing accounts for chart heights so nothing overlaps.
# ---------------------------------------------------------------------------
SECTION_ROWS = {
    "company_overview": 3,
    "financial_data": 12,
    "stock_performance": 28,
    "valuation": 45,
    "sources": 54,
}

# Row heights (in points) for rows that need extra space
DESCRIPTION_ROW_HEIGHT = 60  # each description row gets this height

# Column widths  (column letter → width in Excel units)
COLUMN_WIDTHS = {
    "A": 3,
    "B": 14,
    "C": 12,
    "D": 12,
    "E": 12,
    "F": 12,
    "G": 12,
    "H": 12,
    "I": 12,
    "J": 12,
    "K": 12,
    "L": 12,
    "M": 12,
    "N": 12,
    "O": 12,
    "P": 12,
    "Q": 12,
    "R": 14,
}

# Last data column letter
LAST_COL = "R"
LAST_COL_NUM = 18  # openpyxl column number for R

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
PAGE_ORIENTATION = "landscape"
PAGE_PAPER_SIZE = 1  # PAPERSIZE_LETTER
PAGE_MARGINS = {
    "left": 0.5,
    "right": 0.5,
    "top": 0.5,
    "bottom": 0.5,
}

# ---------------------------------------------------------------------------
# Font / color constants
# ---------------------------------------------------------------------------
HEADER_BG_COLOR = "4472C4"
HEADER_FONT_COLOR = "FFFFFF"
HEADER_FONT_SIZE = 12
TITLE_FONT_SIZE = 16
LABEL_FONT_SIZE = 10
VALUE_FONT_SIZE = 10
FONT_NAME = "Calibri"
