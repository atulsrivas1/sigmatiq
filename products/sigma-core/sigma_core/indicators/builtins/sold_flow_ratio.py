from ..base import Indicator
import pandas as pd

class SoldFlowRatio(Indicator):
    CATEGORY = "options_flow"
    SUBCATEGORY = "ratio"
    """Put/Call sold flow ratio with optional smoothing window.
    Params: window: int|None (rolling mean window); uses columns puts_sold_total, calls_sold_total.
    Output: sold_flow_ratio or sold_flow_ratio_{window}
    """
    def __init__(self, window: int | None = None):
        self.window = int(window) if window else None

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if not {"puts_sold_total", "calls_sold_total"}.issubset(df.columns):
            out["sold_flow_ratio" if not self.window else f"sold_flow_ratio_{self.window}"] = 0.0
            return out
        pc = (df["puts_sold_total"].astype(float) + 1e-6) / (df["calls_sold_total"].astype(float) + 1e-6)
        if self.window and self.window > 1:
            pc = pc.rolling(self.window).mean()
            col = f"sold_flow_ratio_{self.window}"
        else:
            col = "sold_flow_ratio"
        out[col] = pc.fillna(0.0)
        return out
