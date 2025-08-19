from ..base import Indicator
import pandas as pd
import numpy as np

class ADX(Indicator):
    CATEGORY = "trend_strength"
    SUBCATEGORY = "dmi_adx"

    def __init__(self, period: int = 14):
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        required = {"high", "low", "close"}
        if not required.issubset(df.columns):
            out[f"plus_di_{self.period}"] = 0.0
            out[f"minus_di_{self.period}"] = 0.0
            out[f"adx_{self.period}"] = 0.0
            return out
        high = pd.to_numeric(df["high"], errors='coerce').astype(float)
        low = pd.to_numeric(df["low"], errors='coerce').astype(float)
        close = pd.to_numeric(df["close"], errors='coerce').astype(float)

        up_move = high.diff()
        down_move = -low.diff()
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

        prev_close = close.shift(1)
        tr1 = (high - low).abs()
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        alpha = 1.0 / float(self.period)
        tr_s = tr.ewm(alpha=alpha, adjust=False).mean()
        plus_dm_s = pd.Series(plus_dm, index=df.index).ewm(alpha=alpha, adjust=False).mean()
        minus_dm_s = pd.Series(minus_dm, index=df.index).ewm(alpha=alpha, adjust=False).mean()

        plus_di = 100.0 * (plus_dm_s / (tr_s + 1e-12))
        minus_di = 100.0 * (minus_dm_s / (tr_s + 1e-12))
        dx = 100.0 * (plus_di - minus_di).abs() / ((plus_di + minus_di) + 1e-12)
        adx = dx.ewm(alpha=alpha, adjust=False).mean()

        out[f"plus_di_{self.period}"] = plus_di.fillna(0.0)
        out[f"minus_di_{self.period}"] = minus_di.fillna(0.0)
        out[f"adx_{self.period}"] = adx.fillna(0.0)
        return out

