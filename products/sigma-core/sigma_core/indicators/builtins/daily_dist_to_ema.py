from ..base import Indicator
import pandas as pd
import numpy as np
from ...data.sources.polygon import get_polygon_daily_bars

class DailyDistToEma(Indicator):
    CATEGORY = "daily_moving_average"
    SUBCATEGORY = "distance"
    """Normalized distance of daily price to daily EMA, shifted 1 day.

    Params: underlying: str='SPY', window: int=20, normalize: str='price'|'ema'
    Output: dist_ema{window}_d
    """
    def __init__(self, underlying: str = 'SPY', window: int = 20, normalize: str = 'price'):
        self.underlying = underlying
        self.window = int(window)
        self.normalize = normalize

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out[f"dist_ema{self.window}_d"] = 0.0
            return out
        dates = pd.to_datetime(df['date'])
        start = dates.min().date().strftime('%Y-%m-%d')
        end = dates.max().date().strftime('%Y-%m-%d')
        daily = get_polygon_daily_bars(self.underlying, start, end)
        if daily.empty:
            out[f"dist_ema{self.window}_d"] = 0.0
            return out
        daily['date'] = pd.to_datetime(daily['date']).dt.date
        price = daily['close'].astype(float)
        ema = price.ewm(span=self.window, adjust=False).mean()
        denom = price.abs() if self.normalize == 'price' else ema.abs()
        dist = (price - ema) / (denom + 1e-12)
        daily[f"dist_ema{self.window}_d"] = dist.shift(1).fillna(0.0)
        m = pd.Series(pd.to_datetime(df['date']).dt.date).map(daily.set_index('date')[f"dist_ema{self.window}_d"]).astype(float).fillna(0.0)
        out[f"dist_ema{self.window}_d"] = m.values
        return out
