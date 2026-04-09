"""Tear Sheet Generator — scrapes financial data and builds print-ready Excel tear sheets."""

from pathlib import Path

from tear_sheet.charts import create_price_chart, create_revenue_chart
from tear_sheet.config import OUTPUT_DIR
from tear_sheet.excel_builder import build_tear_sheet
from tear_sheet.financials import (
    calculate_analyst_upside,
    calculate_growth_metrics,
    calculate_ratios,
    calculate_return_percentages,
)
from tear_sheet.scraper import get_company_data


def generate_tear_sheet(ticker: str, output_dir: Path | None = None) -> Path:
    """Generate a complete tear sheet for a given ticker.

    Returns the path to the saved .xlsx file.
    """
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
    financials = {
        "growth": growth,
        "returns": returns,
        "ratios": ratios,
        "analyst_upside": analyst_upside,
    }

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
