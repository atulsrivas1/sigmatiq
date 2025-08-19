from ..base import Indicator
import pandas as pd

class MACD(Indicator):
    NAME = "macd"
    CATEGORY = "oscillator"
    SUBCATEGORY = "macd"

    def __init__(self, column: str = "close", fast: int = 12, slow: int = 26, signal: int = 9):
        self.column = column
        self.fast = int(fast)
        self.slow = int(slow)
        self.signal = int(signal)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out["macd_line"] = 0.0
            out["macd_signal"] = 0.0
            out["macd_hist"] = 0.0
            return out
        x = pd.to_numeric(df[self.column], errors='coerce').astype(float)
        ema_fast = x.ewm(span=self.fast, adjust=False).mean()
        ema_slow = x.ewm(span=self.slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        macd_signal = macd_line.ewm(span=self.signal, adjust=False).mean()
        macd_hist = macd_line - macd_signal
        out["macd_line"] = macd_line.fillna(0.0)
        out["macd_signal"] = macd_signal.fillna(0.0)
        out["macd_hist"] = macd_hist.fillna(0.0)
        return out

