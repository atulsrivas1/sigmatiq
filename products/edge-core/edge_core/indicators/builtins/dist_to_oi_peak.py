from ..base import Indicator
import pandas as pd
import numpy as np
from .oi_peak_strike import OIPeakStrike


class DistToOIPeak(Indicator):
    NAME = "dist_to_oi_peak"
    CATEGORY = "options_structure"
    SUBCATEGORY = "oi_peaks"

    def __init__(self, underlying: str = 'SPY', spot_col: str = 'close'):
        self.underlying = underlying
        self.spot_col = spot_col

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.spot_col not in df.columns:
            out['dist_to_oi_peak'] = float('nan')
            return out
        spot = pd.to_numeric(df[self.spot_col], errors='coerce').astype(float)
        peak = OIPeakStrike(self.underlying).calculate(df)['oi_peak_strike']
        out['dist_to_oi_peak'] = (spot - peak).astype(float)
        return out

