# Tear Sheet Generator

**One-sentence summary**:  
A Python tool that scrapes financial data from the internet and generates a print-ready Excel tear sheet for any publicly traded company.

**Author**: Landon Memmott  
**Contact**: landon.memmott@pm.me  
**GitHub**: https://github.com/lmemm/tear_sheet_generator  
**Project started**: April 2026  
**Status**: 🟢 Active

---

## Quick Start

```bash
git clone https://github.com/lmemm/tear_sheet_generator.git
cd tear_sheet_generator
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # or: pip install -e .
```

Verify everything works:
```bash
pytest                             # run tests
python scripts/main.py             # generate a tear sheet
```

---

## Folder Structure

```
tear_sheet_generator/
├── src/
│   └── tear_sheet/
│       ├── __init__.py            → Package root
│       ├── scraper.py             → Data fetching from yfinance
│       ├── financials.py          → Financial calculations and ratios
│       ├── charts.py              → Matplotlib chart generation
│       ├── excel_builder.py       → Excel formatting and assembly
│       ├── config.py              → Settings, constants
│       └── utils.py               → Shared helper functions
├── tests/
│   ├── __init__.py
│   └── ...                        → Tests mirror src/ structure
├── scripts/
│   └── main.py                    → CLI entry point
├── notebooks/
│   └── tear_sheet.ipynb           → Jupyter notebook (class deliverable)
├── data/
│   ├── raw/                       → Original class files (read-only)
│   └── processed/                 → Intermediate data
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CHANGELOG.md
│   ├── DECISIONS.md
│   └── PROJECT_LOG.md
├── outputs/                       → Generated tear sheet Excel files
├── scratch/                       → Local only (gitignored)
├── .gitignore
├── CLAUDE.md
├── BACKLOG.md
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Usage

```bash
# Generate a tear sheet for Apple
python scripts/main.py AAPL

# Or use the Jupyter notebook interactively
jupyter notebook notebooks/tear_sheet.ipynb
```

Output is saved to `outputs/AAPL_tear_sheet.xlsx`.

---

## Dependencies & Tools

- **Python**: 3.11+
- **Key packages**: yfinance, openpyxl, pandas, matplotlib
- **Dev tools**: pytest, ruff (linting)
- **Dependency file**: `pyproject.toml` is the source of truth; `requirements.txt` is a pinned snapshot.

---

## Project Conventions

- **Branching**: `main` is stable. Work in feature branches, merge via PR.
- **Naming**: snake_case for files and functions. Classes are PascalCase.
- **Commits**: Short imperative subject line ("Add CSV parser", not "Added CSV parser").
- **Linting**: Run `ruff check .` before committing.
- **Data**: Raw data is never modified. All generated output goes to `outputs/`.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

*Last updated: 2026-04-09 by Landon Memmott*
