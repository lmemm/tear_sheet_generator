"""Tests for financials module."""

import pandas as pd
import numpy as np

from tear_sheet.financials import (
    calculate_analyst_upside,
    calculate_growth_metrics,
    calculate_ratios,
    calculate_return_percentages,
)


def _make_income_stmt():
    """Create a sample income statement DataFrame (columns = dates, oldest→newest)."""
    dates = pd.to_datetime(["2021-12-31", "2022-12-31", "2023-12-31", "2024-12-31"])
    data = {
        "Total Revenue": [50e9, 55e9, 60e9, 63e9],
        "Net Income": [5e9, 6e9, 5.5e9, 7e9],
    }
    df = pd.DataFrame(data, index=dates).T
    return df


def _make_history(years=5):
    """Create sample daily stock price history."""
    end = pd.Timestamp.now().normalize()
    start = end - pd.DateOffset(years=years)
    dates = pd.bdate_range(start, end)
    np.random.seed(42)
    prices = 100 + np.cumsum(np.random.randn(len(dates)) * 0.5)
    prices = np.maximum(prices, 10)  # keep positive
    return pd.DataFrame({"Close": prices}, index=dates)


class TestCalculateGrowthMetrics:
    def test_with_data(self):
        df = _make_income_stmt()
        result = calculate_growth_metrics(df)

        assert "revenue_yoy" in result
        assert "revenue_indexed" in result
        assert "net_income_yoy" in result

        # 4 years → 3 YoY periods
        assert len(result["revenue_yoy"]) == 3
        assert len(result["net_income_yoy"]) == 3

        # First revenue growth: (55-50)/50 = 0.1
        first_key = list(result["revenue_yoy"].keys())[0]
        assert abs(result["revenue_yoy"][first_key] - 0.1) < 0.001

        # Indexed revenue starts at 1.0
        assert result["revenue_indexed"].iloc[0] == 1.0

    def test_none_input(self):
        result = calculate_growth_metrics(None)
        assert result["revenue_yoy"] == {}
        assert result["revenue_indexed"] is None
        assert result["net_income_yoy"] == {}

    def test_empty_dataframe(self):
        result = calculate_growth_metrics(pd.DataFrame())
        assert result["revenue_yoy"] == {}


class TestCalculateReturnPercentages:
    def test_with_data(self):
        history = _make_history(years=5)
        result = calculate_return_percentages(history)

        assert "1Y" in result
        assert "3Y" in result
        assert "5Y" in result
        # All should be numeric (not None) since we have 5 years of data
        assert all(isinstance(v, float) for v in result.values())

    def test_short_history(self):
        # Only 6 months of data
        end = pd.Timestamp.now().normalize()
        start = end - pd.DateOffset(months=6)
        dates = pd.bdate_range(start, end)
        prices = [100 + i * 0.1 for i in range(len(dates))]
        history = pd.DataFrame({"Close": prices}, index=dates)

        result = calculate_return_percentages(history)
        assert result["1Y"] is None
        assert result["3Y"] is None
        assert result["5Y"] is None

    def test_none_input(self):
        result = calculate_return_percentages(None)
        assert result == {"1Y": None, "3Y": None, "5Y": None}


class TestCalculateRatios:
    def test_with_data(self):
        data = {"info": {"current_ratio": 1.5, "quick_ratio": 1.2, "debt_to_equity": 0.8}}
        result = calculate_ratios(data)
        assert result["current_ratio"] == 1.5
        assert result["quick_ratio"] == 1.2
        assert result["debt_to_equity"] == 0.8

    def test_missing_data(self):
        result = calculate_ratios({"info": {}})
        assert result["current_ratio"] is None


class TestCalculateAnalystUpside:
    def test_with_data(self):
        data = {
            "info": {"current_price": 100},
            "analyst_targets": {"mean": 120, "low": 90, "high": 150},
        }
        result = calculate_analyst_upside(data)
        assert abs(result - 0.2) < 0.001

    def test_no_targets(self):
        data = {"info": {"current_price": 100}, "analyst_targets": None}
        assert calculate_analyst_upside(data) is None

    def test_no_price(self):
        data = {"info": {"current_price": None}, "analyst_targets": {"mean": 120}}
        assert calculate_analyst_upside(data) is None
