from ..base import Indicator
import pandas as pd

class CCI(Indicator):
    CATEGORY = "oscillator"
    SUBCATEGORY = "cci"

    def __init__(self, period: int = 20):
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        required = {"high", "low", "close"}
        if not required.issubset(df.columns):
            out[f"cci_{self.period}"] = 0.0
            return out
        high = pd.to_numeric(df['high'], errors='coerce').astype(float)
        low = pd.to_numeric(df['low'], errors='coerce').astype(float)
        close = pd.to_numeric(df['close'], errors='coerce').astype(float)
        tp = (high + low + close) / 3.0
        sma = tp.rolling(self.period).mean()
        md = (tp - sma).abs().rolling(self.period).mean()
        cci = (tp - sma) / (0.015 * (md + 1e-12))
        out[f"cci_{self.period}"] = cci.fillna(0.0)
        return out

