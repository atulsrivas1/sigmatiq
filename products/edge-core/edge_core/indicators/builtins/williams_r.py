from ..base import Indicator
import pandas as pd

class WilliamsR(Indicator):
    CATEGORY = "oscillator"
    SUBCATEGORY = "williams_r"

    def __init__(self, period: int = 14):
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        required = {"high", "low", "close"}
        if not required.issubset(df.columns):
            out[f"williams_r_{self.period}"] = 0.0
            return out
        high = pd.to_numeric(df['high'], errors='coerce').astype(float)
        low = pd.to_numeric(df['low'], errors='coerce').astype(float)
        close = pd.to_numeric(df['close'], errors='coerce').astype(float)
        hh = high.rolling(self.period).max()
        ll = low.rolling(self.period).min()
        wr = -100.0 * (hh - close) / (hh - ll + 1e-12)
        out[f"williams_r_{self.period}"] = wr.fillna(0.0)
        return out

