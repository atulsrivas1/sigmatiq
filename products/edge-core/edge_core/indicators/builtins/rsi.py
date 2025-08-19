from ..base import Indicator
import pandas as pd

class RSI(Indicator):
    CATEGORY = "oscillator"
    SUBCATEGORY = "rsi"
    """Wilder RSI over a column (default: close).
    Params: column: str = 'close', period: int = 14
    Output: rsi_{period}
    """
    def __init__(self, column: str = "close", period: int = 14):
        self.column = column
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"rsi_{self.period}"] = 0.0
            return out
        series = df[self.column].astype(float)
        delta = series.diff()
        gain = delta.clip(lower=0.0)
        loss = -delta.clip(upper=0.0)
        # Wilder's smoothing via EMA with alpha = 1/period
        avg_gain = gain.ewm(alpha=1.0/self.period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1.0/self.period, adjust=False).mean()
        rs = avg_gain / (avg_loss + 1e-12)
        rsi = 100.0 - (100.0 / (1.0 + rs))
        out[f"rsi_{self.period}"] = rsi.fillna(0.0)
        return out
