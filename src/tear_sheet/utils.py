"""Shared helper functions."""


def format_market_cap(value: float | None) -> str:
    """Format market cap with T/B/M suffix."""
    if value is None:
        return "N/A"
    if value >= 1e12:
        return f"${value / 1e12:.2f}T"
    if value >= 1e9:
        return f"${value / 1e9:.2f}B"
    if value >= 1e6:
        return f"${value / 1e6:.2f}M"
    return f"${value:,.0f}"


def format_percentage(value: float | None) -> str:
    """Format a decimal as a percentage string (e.g. 0.156 → '15.6%')."""
    if value is None:
        return "N/A"
    return f"{value * 100:.1f}%"


def format_currency(value: float | None) -> str:
    """Format a number as USD currency."""
    if value is None:
        return "N/A"
    return f"${value:,.2f}"
