from ..base import Indicator
import pandas as pd
import numpy as np
from .gamma_peak_strike import GammaPeakStrike


class DistToGammaPeak(Indicator):
    NAME = "dist_to_gamma_peak"
    CATEGORY = "options_structure"
    SUBCATEGORY = "gamma_peaks"

    def __init__(self, underlying: str = 'SPY', spot_col: str = 'close'):
        self.underlying = underlying
        self.spot_col = spot_col

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.spot_col not in df.columns:
            out['dist_to_gamma_peak'] = float('nan')
            return out
        spot = pd.to_numeric(df[self.spot_col], errors='coerce').astype(float)
        peak = GammaPeakStrike(self.underlying).calculate(df)['gamma_peak_strike']
        out['dist_to_gamma_peak'] = (spot - peak).astype(float)
        return out

