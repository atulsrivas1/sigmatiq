from ..base import Indicator
import pandas as pd
import numpy as np


class RSILastHour(Indicator):
    NAME = "rsi_last_hour"
    CATEGORY = "intraday"
    SUBCATEGORY = "session_window"

    def __init__(self, period: int = 7):
        self.period = int(period)

    def _rsi(self, s: pd.Series, period: int) -> pd.Series:
        delta = s.diff()
        gain = (delta.clip(lower=0)).ewm(alpha=1/period, adjust=False).mean()
        loss = (-delta.clip(upper=0)).ewm(alpha=1/period, adjust=False).mean()
        rs = gain / (loss.replace(0.0, np.nan))
        return 100 - (100 / (1 + rs))

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'close' not in df.columns or 'date' not in df.columns:
            out[f"rsi_last_hour_{self.period}"] = float('nan')
            return out
        # Compute RSI on close across entire series, but expose only last-hour rows (hour_et == 15) if available
        s = pd.to_numeric(df['close'], errors='coerce').astype(float)
        rsi = self._rsi(s, self.period)
        col = f"rsi_last_hour_{self.period}"
        out[col] = pd.Series(np.nan, index=df.index)
        if 'hour_et' in df.columns:
            mask = (pd.to_numeric(df['hour_et'], errors='coerce') == 15)
            out.loc[mask, col] = rsi[mask]
        else:
            out[col] = rsi  # fallback: provide for all rows
        return out

