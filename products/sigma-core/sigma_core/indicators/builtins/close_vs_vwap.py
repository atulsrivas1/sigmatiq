from ..base import Indicator
import pandas as pd
import numpy as np


class CloseVsVWAP(Indicator):
    NAME = "close_vs_vwap"
    CATEGORY = "intraday"
    SUBCATEGORY = "vwap"

    def __init__(self, kind: str = 'intraday'):
        # kind: 'intraday' uses intraday_vwap column if present; 'daily' uses daily_vwap
        self.kind = kind

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'close' not in df.columns:
            out['close_vs_vwap'] = float('nan')
            return out
        close = pd.to_numeric(df['close'], errors='coerce').astype(float)
        vwap = None
        if self.kind == 'daily' and 'vwap_d' in df.columns:
            vwap = pd.to_numeric(df['vwap_d'], errors='coerce').astype(float)
        elif 'vwap_intraday' in df.columns:
            vwap = pd.to_numeric(df['vwap_intraday'], errors='coerce').astype(float)
        elif 'vwap' in df.columns:
            vwap = pd.to_numeric(df['vwap'], errors='coerce').astype(float)
        else:
            out['close_vs_vwap'] = float('nan')
            return out
        out['close_vs_vwap'] = (close - vwap) / (vwap.replace(0.0, np.nan))
        return out

