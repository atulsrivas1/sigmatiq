from ..base import Indicator
import pandas as pd
import numpy as np


class Ichimoku(Indicator):
    NAME = "ichimoku"
    CATEGORY = "price"
    SUBCATEGORY = "trend"

    def __init__(self, tenkan: int = 9, kijun: int = 26, senkou: int = 52, shift_ahead: bool = False):
        self.tenkan = int(tenkan)
        self.kijun = int(kijun)
        self.senkou = int(senkou)
        self.shift_ahead = bool(shift_ahead)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        req = {'high','low','close'}
        if not req.issubset(df.columns):
            out['ichimoku_tenkan'] = float('nan')
            out['ichimoku_kijun'] = float('nan')
            out['ichimoku_span_a'] = float('nan')
            out['ichimoku_span_b'] = float('nan')
            out['ichimoku_chikou'] = float('nan')
            return out
        h = pd.to_numeric(df['high'], errors='coerce').astype(float)
        l = pd.to_numeric(df['low'], errors='coerce').astype(float)
        c = pd.to_numeric(df['close'], errors='coerce').astype(float)

        conv = (h.rolling(self.tenkan).max() + l.rolling(self.tenkan).min()) / 2.0
        base = (h.rolling(self.kijun).max() + l.rolling(self.kijun).min()) / 2.0
        span_a = (conv + base) / 2.0
        span_b = (h.rolling(self.senkou).max() + l.rolling(self.senkou).min()) / 2.0
        chikou = c.shift(-self.kijun)  # lagging line (shift back K periods); negative shift moves forward in index
        if self.shift_ahead:
            # Project spans ahead by kijun periods (may produce NaNs at tail)
            span_a = span_a.shift(self.kijun)
            span_b = span_b.shift(self.kijun)
        out['ichimoku_tenkan'] = conv
        out['ichimoku_kijun'] = base
        out['ichimoku_span_a'] = span_a
        out['ichimoku_span_b'] = span_b
        out['ichimoku_chikou'] = chikou
        return out

