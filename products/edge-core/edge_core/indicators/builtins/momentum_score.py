from ..base import Indicator
import pandas as pd
import numpy as np

class MomentumScoreTotal(Indicator):
    CATEGORY = "composite"
    SUBCATEGORY = "momentum_score"
    """Composite momentum score combining hourly and daily signals.

    This implementation is intentionally simple and robust:
      score_hourly = zscore([close_mom_1, close_mom_3])
      score_daily  = (rsi_14_d - 50) / 50  # scaled to ~[-1, 1]
      momentum_score_total = w_hourly * score_hourly + w_daily * score_daily

    Params: w_hourly: float = 0.7, w_daily: float = 0.3
    Output: momentum_score_total
    """
    def __init__(self, w_hourly: float = 0.7, w_daily: float = 0.3):
        self.w_hourly = float(w_hourly)
        self.w_daily = float(w_daily)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        # Hourly z-score of close_mom_1 and close_mom_3 if present
        hourly_cols = [c for c in ['close_mom_1', 'close_mom_3'] if c in df.columns]
        if hourly_cols:
            h = df[hourly_cols].astype(float).copy()
            h = (h - h.mean()) / (h.std() + 1e-12)
            score_h = h.mean(axis=1)
        else:
            score_h = pd.Series(0.0, index=df.index)
        # Daily RSI scaled
        if 'rsi_14_d' in df.columns:
            score_d = (df['rsi_14_d'].astype(float) - 50.0) / 50.0
        else:
            score_d = pd.Series(0.0, index=df.index)
        out['momentum_score_total'] = self.w_hourly * score_h + self.w_daily * score_d
        return out
