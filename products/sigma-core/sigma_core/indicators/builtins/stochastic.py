from ..base import Indicator
import pandas as pd

class Stochastic(Indicator):
    CATEGORY = "oscillator"
    SUBCATEGORY = "stochastic"

    def __init__(self, period_k: int = 14, period_d: int = 3):
        self.period_k = int(period_k)
        self.period_d = int(period_d)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        required = {"high", "low", "close"}
        if not required.issubset(df.columns):
            out['stoch_k'] = 0.0
            out['stoch_d'] = 0.0
            return out
        high = pd.to_numeric(df['high'], errors='coerce').astype(float)
        low = pd.to_numeric(df['low'], errors='coerce').astype(float)
        close = pd.to_numeric(df['close'], errors='coerce').astype(float)
        ll = low.rolling(self.period_k).min()
        hh = high.rolling(self.period_k).max()
        k = 100.0 * (close - ll) / (hh - ll + 1e-12)
        d = k.rolling(self.period_d).mean()
        out['stoch_k'] = k.fillna(0.0)
        out['stoch_d'] = d.fillna(0.0)
        return out

