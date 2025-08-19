from ..base import Indicator
import pandas as pd
from ...data.sources.polygon import get_polygon_daily_bars

class DailyRet(Indicator):
    CATEGORY = "daily_momentum"
    SUBCATEGORY = "returns"
    """Daily returns over N days, shifted 1 day to avoid leakage.

    Params: underlying: str='SPY', window: int=1
    Output: ret_{window}d_d
    """
    def __init__(self, underlying: str = 'SPY', window: int = 1):
        self.underlying = underlying
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out[f"ret_{self.window}d_d"] = 0.0
            return out
        dates = pd.to_datetime(df['date'])
        start = dates.min().date().strftime('%Y-%m-%d')
        end = dates.max().date().strftime('%Y-%m-%d')
        daily = get_polygon_daily_bars(self.underlying, start, end)
        if daily.empty:
            out[f"ret_{self.window}d_d"] = 0.0
            return out
        daily['date'] = pd.to_datetime(daily['date']).dt.date
        ret = daily['close'].astype(float).pct_change(self.window).shift(1).fillna(0.0)
        daily[f"ret_{self.window}d_d"] = ret
        m = pd.Series(pd.to_datetime(df['date']).dt.date).map(daily.set_index('date')[f"ret_{self.window}d_d"]).astype(float).fillna(0.0)
        out[f"ret_{self.window}d_d"] = m.values
        return out
