"""Matplotlib chart generation for tear sheets."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from io import BytesIO

import pandas as pd

from tear_sheet.config import CHART_DPI, PRICE_CHART_SIZE, REVENUE_CHART_SIZE
from tear_sheet.financials import _indexed_series


def create_price_chart(history: pd.DataFrame, ticker: str) -> BytesIO:
    """Generate a 5-year stock price line chart and return as PNG BytesIO."""
    fig, ax = plt.subplots(figsize=PRICE_CHART_SIZE)

    ax.plot(history.index, history["Close"], color="#4472C4", linewidth=1.2)
    ax.set_title(f"{ticker} Stock Price (5Y)", fontsize=14, fontweight="bold")
    ax.set_ylabel("Price ($)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    fig.autofmt_xdate()

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=CHART_DPI, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf


def create_revenue_chart(income_stmt: pd.DataFrame, ticker: str) -> BytesIO:
    """Generate an indexed revenue growth chart and return as PNG BytesIO."""
    indexed = _indexed_series(income_stmt, "Total Revenue")

    fig, ax = plt.subplots(figsize=REVENUE_CHART_SIZE)

    if indexed is not None:
        labels = [
            c.year if hasattr(c, "year") else str(c) for c in indexed.index
        ]
        ax.plot(labels, indexed.values, color="#4472C4", linewidth=1.5, marker="o", markersize=4)

    ax.set_title(f"{ticker} Revenue Growth", fontsize=14, fontweight="bold")
    ax.set_ylabel("Revenue Growth")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=35)

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=CHART_DPI, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf
