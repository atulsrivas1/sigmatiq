from ..base import Indicator
import pandas as pd

class ElderRay(Indicator):
    CATEGORY = "trend_strength"
    SUBCATEGORY = "elder_ray"

    def __init__(self, period: int = 13):
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        required = {"high", "low", "close"}
        if not required.issubset(df.columns):
            out['bull_power'] = 0.0
            out['bear_power'] = 0.0
            return out
        close = pd.to_numeric(df['close'], errors='coerce').astype(float)
        high = pd.to_numeric(df['high'], errors='coerce').astype(float)
        low = pd.to_numeric(df['low'], errors='coerce').astype(float)
        ema = close.ewm(span=self.period, adjust=False).mean()
        bull = high - ema
        bear = low - ema
        out['bull_power'] = bull.fillna(0.0)
        out['bear_power'] = bear.fillna(0.0)
        return out

