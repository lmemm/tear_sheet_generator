"""Tests for charts module."""

import pandas as pd
import numpy as np

from tear_sheet.charts import create_price_chart, create_revenue_chart


def _make_history():
    """Create sample daily stock price history."""
    dates = pd.bdate_range("2020-01-01", periods=1000)
    np.random.seed(42)
    prices = 100 + np.cumsum(np.random.randn(1000) * 0.5)
    return pd.DataFrame({"Close": prices}, index=dates)


def _make_income_stmt():
    """Create a sample income statement DataFrame."""
    dates = pd.to_datetime(["2021-12-31", "2022-12-31", "2023-12-31", "2024-12-31"])
    data = {"Total Revenue": [50e9, 55e9, 60e9, 63e9]}
    return pd.DataFrame(data, index=dates).T


class TestCreatePriceChart:
    def test_returns_png_bytesio(self):
        history = _make_history()
        buf = create_price_chart(history, "TEST")
        data = buf.read()
        assert data[:4] == b"\x89PNG"
        assert len(data) > 1000  # sanity check: not empty


class TestCreateRevenueChart:
    def test_returns_png_bytesio(self):
        df = _make_income_stmt()
        buf = create_revenue_chart(df, "TEST")
        data = buf.read()
        assert data[:4] == b"\x89PNG"
        assert len(data) > 1000
