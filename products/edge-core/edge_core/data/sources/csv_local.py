"""CSV-local data source (skeleton stub)."""

from pathlib import Path
import pandas as pd

def load_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)

