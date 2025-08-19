from ..base import Indicator
import pandas as pd

class BollingerBands(Indicator):
    CATEGORY = "band"
    SUBCATEGORY = "bollinger"

    def __init__(self, column: str = "close", window: int = 20, num_std: float = 2.0):
        self.column = column
        self.window = int(window)
        self.num_std = float(num_std)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"bb_mid_{self.window}"] = 0.0
            out[f"bb_upper_{self.window}"] = 0.0
            out[f"bb_lower_{self.window}"] = 0.0
            return out
        x = pd.to_numeric(df[self.column], errors='coerce').astype(float)
        mid = x.rolling(self.window).mean()
        std = x.rolling(self.window).std()
        upper = mid + self.num_std * std
        lower = mid - self.num_std * std
        out[f"bb_mid_{self.window}"] = mid.fillna(0.0)
        out[f"bb_upper_{self.window}"] = upper.fillna(0.0)
        out[f"bb_lower_{self.window}"] = lower.fillna(0.0)
        return out

