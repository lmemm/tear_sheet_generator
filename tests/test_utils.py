"""Tests for utils module."""

from tear_sheet.utils import format_currency, format_market_cap, format_percentage


class TestFormatMarketCap:
    def test_trillion(self):
        assert format_market_cap(1.5e12) == "$1.50T"

    def test_billion(self):
        assert format_market_cap(42.3e9) == "$42.30B"

    def test_million(self):
        assert format_market_cap(750e6) == "$750.00M"

    def test_small(self):
        assert format_market_cap(500_000) == "$500,000"

    def test_none(self):
        assert format_market_cap(None) == "N/A"


class TestFormatPercentage:
    def test_positive(self):
        assert format_percentage(0.156) == "15.6%"

    def test_negative(self):
        assert format_percentage(-0.05) == "-5.0%"

    def test_zero(self):
        assert format_percentage(0.0) == "0.0%"

    def test_none(self):
        assert format_percentage(None) == "N/A"


class TestFormatCurrency:
    def test_normal(self):
        assert format_currency(1234.56) == "$1,234.56"

    def test_large(self):
        assert format_currency(1_000_000) == "$1,000,000.00"

    def test_none(self):
        assert format_currency(None) == "N/A"
