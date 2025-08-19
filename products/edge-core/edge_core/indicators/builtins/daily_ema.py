from ..base import Indicator
import pandas as pd
from ...data.sources.polygon import get_polygon_daily_bars

class DailyEMA(Indicator):
    CATEGORY = "daily_moving_average"
    SUBCATEGORY = "ema"
    """Daily EMA shifted 1 day to avoid leakage.

    Params: underlying: str='SPY', window: int=20
    Output: ema_{window}_d
    """
    def __init__(self, underlying: str = 'SPY', window: int = 20):
        self.underlying = underlying
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out[f"ema_{self.window}_d"] = 0.0
            return out
        dates = pd.to_datetime(df['date'])
        start = dates.min().date().strftime('%Y-%m-%d')
        end = dates.max().date().strftime('%Y-%m-%d')
        daily = get_polygon_daily_bars(self.underlying, start, end)
        if daily.empty:
            out[f"ema_{self.window}_d"] = 0.0
            return out
        daily['date'] = pd.to_datetime(daily['date']).dt.date
        ema = daily['close'].astype(float).ewm(span=self.window, adjust=False).mean().shift(1).fillna(0.0)
        daily[f"ema_{self.window}_d"] = ema
        m = pd.Series(pd.to_datetime(df['date']).dt.date).map(daily.set_index('date')[f"ema_{self.window}_d"]).astype(float).fillna(0.0)
        out[f"ema_{self.window}_d"] = m.values
        return out
