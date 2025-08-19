from ..base import Indicator
import pandas as pd
import numpy as np


class KeltnerChannels(Indicator):
    NAME = "keltner"
    CATEGORY = "price"
    SUBCATEGORY = "channels"

    def __init__(self, window: int = 20, multiplier: float = 2.0):
        self.window = int(window)
        self.multiplier = float(multiplier)

    def _ema(self, s: pd.Series, span: int) -> pd.Series:
        return s.ewm(span=span, adjust=False).mean()

    def _atr(self, h: pd.Series, l: pd.Series, c: pd.Series, period: int) -> pd.Series:
        prev_c = c.shift(1)
        tr1 = h - l
        tr2 = (h - prev_c).abs()
        tr3 = (l - prev_c).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(period, min_periods=max(1, period//2)).mean()

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        req = {'high','low','close'}
        if not req.issubset(df.columns):
            out[f"keltner_mid_{self.window}"] = float('nan')
            out[f"keltner_upper_{self.window}"] = float('nan')
            out[f"keltner_lower_{self.window}"] = float('nan')
            return out
        h = pd.to_numeric(df['high'], errors='coerce').astype(float)
        l = pd.to_numeric(df['low'], errors='coerce').astype(float)
        c = pd.to_numeric(df['close'], errors='coerce').astype(float)
        mid = self._ema(c, self.window)
        rng = self._atr(h, l, c, self.window)
        up = mid + self.multiplier * rng
        lo = mid - self.multiplier * rng
        out[f"keltner_mid_{self.window}"] = mid
        out[f"keltner_upper_{self.window}"] = up
        out[f"keltner_lower_{self.window}"] = lo
        return out

