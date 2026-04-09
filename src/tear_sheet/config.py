"""Central configuration for the tear sheet generator."""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"
DATA_DIR = PROJECT_ROOT / "data"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
