"""Financial calculations and ratio computations."""

import pandas as pd


def calculate_growth_metrics(income_stmt: pd.DataFrame | None) -> dict:
    """Calculate revenue and net income growth from an income statement DataFrame.

    Returns dict with keys: revenue_yoy, revenue_indexed, net_income_yoy.
    """
    empty = {"revenue_yoy": {}, "revenue_indexed": None, "net_income_yoy": {}}
    if income_stmt is None or income_stmt.empty:
        return empty

    result = {}

    # Revenue YoY growth
    result["revenue_yoy"] = _yoy_growth(income_stmt, "Total Revenue")

    # Revenue indexed (first year = 1.0)
    result["revenue_indexed"] = _indexed_series(income_stmt, "Total Revenue")

    # Net Income YoY growth
    result["net_income_yoy"] = _yoy_growth(income_stmt, "Net Income")

    return result


def calculate_return_percentages(history: pd.DataFrame | None) -> dict:
    """Calculate 1Y, 3Y, 5Y stock returns from historical price data.

    Returns dict like {"1Y": 0.156, "3Y": 0.432, "5Y": 0.891} (decimals).
    """
    returns = {"1Y": None, "3Y": None, "5Y": None}
    if history is None or history.empty or "Close" not in history.columns:
        return returns

    end_price = history["Close"].iloc[-1]
    end_date = history.index[-1]

    for label, years in [("1Y", 1), ("3Y", 3), ("5Y", 5)]:
        target_date = end_date - pd.DateOffset(years=years)
        # Skip if history doesn't go back far enough
        if history.index[0] > target_date:
            continue
        # Find nearest available date at or after target
        mask = history.index >= target_date
        start_price = history.loc[mask, "Close"].iloc[0]
        if start_price and start_price != 0:
            returns[label] = (end_price - start_price) / start_price

    return returns


def calculate_ratios(data: dict) -> dict:
    """Extract financial ratios from scraped data."""
    info = data.get("info", {})
    return {
        "current_ratio": info.get("current_ratio"),
        "quick_ratio": info.get("quick_ratio"),
        "debt_to_equity": info.get("debt_to_equity"),
    }


def calculate_analyst_upside(data: dict) -> float | None:
    """Calculate analyst upside/downside percentage.

    Returns decimal (e.g. 0.12 = 12% upside), or None if data unavailable.
    """
    targets = data.get("analyst_targets")
    info = data.get("info", {})
    current_price = info.get("current_price")

    if targets is None or current_price is None or current_price == 0:
        return None

    mean_target = targets.get("mean") or targets.get("median")
    if mean_target is None:
        return None

    return (mean_target - current_price) / current_price


def _yoy_growth(df: pd.DataFrame, row_name: str) -> dict:
    """Calculate year-over-year growth for a row in the income statement."""
    if row_name not in df.index:
        return {}

    values = df.loc[row_name]
    growth = {}
    cols = df.columns.tolist()

    for i in range(len(cols) - 1):
        old_val = values[cols[i]]
        new_val = values[cols[i + 1]]
        if pd.notna(old_val) and pd.notna(new_val) and old_val != 0:
            old_year = cols[i].year if hasattr(cols[i], "year") else str(cols[i])
            new_year = cols[i + 1].year if hasattr(cols[i + 1], "year") else str(cols[i + 1])
            label = f"{old_year}\u2192{new_year}"
            growth[label] = (new_val - old_val) / abs(old_val)

    return growth


def _indexed_series(df: pd.DataFrame, row_name: str) -> pd.Series | None:
    """Normalize a row so the first value = 1.0."""
    if row_name not in df.index:
        return None

    values = df.loc[row_name].dropna()
    if values.empty or values.iloc[0] == 0:
        return None

    return values / values.iloc[0]
