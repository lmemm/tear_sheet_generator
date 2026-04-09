"""CLI entry point for generating tear sheets."""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from tear_sheet import generate_tear_sheet  # noqa: E402


def main():
    parser = argparse.ArgumentParser(
        description="Generate a print-ready Excel tear sheet for a publicly traded company."
    )
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., CAT, AAPL)")
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="Output directory (default: outputs/)"
    )

    args = parser.parse_args()

    try:
        generate_tear_sheet(args.ticker, args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
