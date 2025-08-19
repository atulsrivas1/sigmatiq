from ..base import Indicator
import pandas as pd

class StochRSI(Indicator):
    CATEGORY = "oscillator"
    SUBCATEGORY = "stoch_rsi"

    def __init__(self, column: str = 'close', rsi_period: int = 14, stoch_period: int = 14, smooth_k: int = 3, smooth_d: int = 3):
        self.column = column
        self.rsi_period = int(rsi_period)
        self.stoch_period = int(stoch_period)
        self.smooth_k = int(smooth_k)
        self.smooth_d = int(smooth_d)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out['stochrsi_k'] = 0.0
            out['stochrsi_d'] = 0.0
            return out
        x = pd.to_numeric(df[self.column], errors='coerce').astype(float)
        delta = x.diff()
        gain = delta.clip(lower=0.0)
        loss = -delta.clip(upper=0.0)
        rsi = 100.0 - (100.0 / (1.0 + gain.ewm(alpha=1.0/self.rsi_period, adjust=False).mean() / (loss.ewm(alpha=1.0/self.rsi_period, adjust=False).mean() + 1e-12)))
        rsi_min = rsi.rolling(self.stoch_period).min()
        rsi_max = rsi.rolling(self.stoch_period).max()
        stoch_rsi = (rsi - rsi_min) / (rsi_max - rsi_min + 1e-12)
        k = stoch_rsi.rolling(self.smooth_k).mean() * 100.0
        d = k.rolling(self.smooth_d).mean()
        out['stochrsi_k'] = k.fillna(0.0)
        out['stochrsi_d'] = d.fillna(0.0)
        return out

