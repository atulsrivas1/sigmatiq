from ..base import Indicator
import pandas as pd

class ATR(Indicator):
    CATEGORY = "volatility"
    SUBCATEGORY = "atr"

    def __init__(self, period: int = 14):
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        required = {"high", "low", "close"}
        if not required.issubset(df.columns):
            out[f"atr_{self.period}"] = 0.0
            return out
        high = pd.to_numeric(df["high"], errors='coerce').astype(float)
        low = pd.to_numeric(df["low"], errors='coerce').astype(float)
        close = pd.to_numeric(df["close"], errors='coerce').astype(float)
        prev_close = close.shift(1)
        tr = pd.concat([
            (high - low).abs(),
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ], axis=1).max(axis=1)
        alpha = 1.0 / float(self.period)
        atr = tr.ewm(alpha=alpha, adjust=False).mean()
        out[f"atr_{self.period}"] = atr.fillna(0.0)
        return out

