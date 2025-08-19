from ..base import Indicator
import pandas as pd
import numpy as np


class PCRVolume(Indicator):
    NAME = "pcr_volume"
    CATEGORY = "options_flow"
    SUBCATEGORY = "ratios"

    def __init__(self):
        pass

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        # Prefer aggregated flow totals if present; otherwise try to infer from per-distance columns
        if {'calls_sold_total','puts_sold_total'}.issubset(df.columns):
            c = pd.to_numeric(df['calls_sold_total'], errors='coerce').astype(float)
            p = pd.to_numeric(df['puts_sold_total'], errors='coerce').astype(float)
            out['pcr_volume'] = (p + 1e-9) / (c + 1e-9)
            return out
        # fallback: sum per-distance columns if available
        calls_d = [c for c in df.columns if str(c).startswith('calls_sold_d')]
        puts_d = [c for c in df.columns if str(c).startswith('puts_sold_d')]
        if calls_d and puts_d:
            ctot = pd.DataFrame({k: pd.to_numeric(df[k], errors='coerce').astype(float) for k in calls_d}).sum(axis=1)
            ptot = pd.DataFrame({k: pd.to_numeric(df[k], errors='coerce').astype(float) for k in puts_d}).sum(axis=1)
            out['pcr_volume'] = (ptot + 1e-9) / (ctot + 1e-9)
            return out
        out['pcr_volume'] = float('nan')
        return out

