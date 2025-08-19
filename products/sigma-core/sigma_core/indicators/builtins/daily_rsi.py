from ..base import Indicator
import pandas as pd
import numpy as np
from datetime import datetime
from ...data.sources.polygon import get_polygon_daily_bars

class DailyRSI(Indicator):
    CATEGORY = "daily_momentum"
    SUBCATEGORY = "rsi"
    """Daily RSI shifted 1 day to avoid leakage.

    Params: underlying: str='SPY', period: int=14, column: str='close'
    Output: rsi_{period}_d
    """
    def __init__(self, underlying: str = 'SPY', period: int = 14, column: str = 'close'):
        self.underlying = underlying
        self.period = int(period)
        self.column = column

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out[f"rsi_{self.period}_d"] = 0.0
            return out
        dates = pd.to_datetime(df['date'])
        start = dates.min().date().strftime('%Y-%m-%d')
        end = dates.max().date().strftime('%Y-%m-%d')
        daily = get_polygon_daily_bars(self.underlying, start, end)
        if daily.empty:
            out[f"rsi_{self.period}_d"] = 0.0
            return out
        daily['date'] = pd.to_datetime(daily['date']).dt.date
        s = daily['close'].astype(float)
        delta = s.diff()
        gain = delta.clip(lower=0.0)
        loss = -delta.clip(upper=0.0)
        avg_gain = gain.ewm(alpha=1.0/self.period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1.0/self.period, adjust=False).mean()
        rs = avg_gain / (avg_loss + 1e-12)
        rsi = 100.0 - (100.0 / (1.0 + rs))
        daily[f"rsi_{self.period}_d"] = rsi.shift(1).fillna(0.0)  # shift one day
        m = pd.Series(pd.to_datetime(df['date']).dt.date).map(daily.set_index('date')[f"rsi_{self.period}_d"])\
            .astype(float).fillna(0.0)
        out[f"rsi_{self.period}_d"] = m.values
        return out
