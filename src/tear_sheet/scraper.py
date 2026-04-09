"""Data fetching from yfinance."""

from datetime import date

import pandas as pd
import yfinance as yf

from tear_sheet.config import HISTORY_PERIOD, YFINANCE_INFO_FIELDS


def get_company_data(ticker: str) -> dict:
    """Fetch all raw data from yfinance for a given ticker.

    Returns a dict with keys: info, income_stmt, balance_sheet, history,
    recommendations, analyst_targets, calendar, ticker, fetch_date.

    Raises ValueError if the ticker is invalid.
    """
    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker)

    # -- Validate ticker --------------------------------------------------
    raw_info = stock.info or {}
    if not raw_info.get("shortName"):
        raise ValueError(f"Invalid ticker: {ticker}")

    # -- Company info (filtered to configured fields) ---------------------
    info = {
        name: raw_info.get(yf_key)
        for name, yf_key in YFINANCE_INFO_FIELDS.items()
    }

    # -- Income statement -------------------------------------------------
    income_stmt = _safe_fetch(lambda: stock.income_stmt)
    if income_stmt is not None and not income_stmt.empty:
        income_stmt = _clean_income_stmt(income_stmt)
    else:
        income_stmt = None

    # -- Balance sheet ----------------------------------------------------
    balance_sheet = _safe_fetch(lambda: stock.balance_sheet)
    if balance_sheet is not None and balance_sheet.empty:
        balance_sheet = None

    # -- Historical prices ------------------------------------------------
    history = _safe_fetch(lambda: stock.history(period=HISTORY_PERIOD))
    if history is not None and history.empty:
        history = None

    # -- Recommendations --------------------------------------------------
    recommendations = _safe_fetch(lambda: stock.recommendations)
    if recommendations is not None and recommendations.empty:
        recommendations = None

    # -- Analyst price targets --------------------------------------------
    analyst_targets = _safe_fetch(lambda: _parse_analyst_targets(stock))

    # -- Calendar (earnings dates, etc.) ----------------------------------
    calendar = _safe_fetch(lambda: stock.calendar)
    if isinstance(calendar, dict) and not calendar:
        calendar = None

    return {
        "info": info,
        "income_stmt": income_stmt,
        "balance_sheet": balance_sheet,
        "history": history,
        "recommendations": recommendations,
        "analyst_targets": analyst_targets,
        "calendar": calendar,
        "ticker": ticker,
        "fetch_date": date.today().isoformat(),
    }


def _clean_income_stmt(df: pd.DataFrame) -> pd.DataFrame:
    """Sort columns chronologically and drop trailing NaN column."""
    col_names = df.columns.tolist()
    # Drop last column if Total Revenue is NaN (known yfinance quirk)
    if "Total Revenue" in df.index and pd.isnull(
        df.loc["Total Revenue", col_names[-1]]
    ):
        df = df.drop(df.columns[-1], axis=1)

    # Sort columns chronologically (oldest → newest)
    df = df.reindex(columns=sorted(df.columns))
    return df


def _parse_analyst_targets(stock: yf.Ticker) -> dict | None:
    """Extract analyst price targets into a plain dict."""
    targets = stock.analyst_price_targets
    if targets is None:
        return None
    # May be a dict or pandas Series depending on yfinance version
    if isinstance(targets, pd.Series):
        targets = targets.to_dict()
    if isinstance(targets, dict) and targets:
        return targets
    return None


def _safe_fetch(fn):
    """Call fn and return its result; return None on any exception."""
    try:
        return fn()
    except Exception:
        return None
