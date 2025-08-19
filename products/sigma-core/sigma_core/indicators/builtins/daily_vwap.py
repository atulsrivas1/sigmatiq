from ..base import Indicator
import pandas as pd
from ...data.sources.polygon import get_polygon_daily_bars

class DailyVWAP(Indicator):
    CATEGORY = "daily_volume"
    SUBCATEGORY = "vwap"

    def __init__(self, underlying: str = 'SPY', shift_days: int = 1):
        self.underlying = underlying
        self.shift_days = int(shift_days)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['vwap_d'] = 0.0
            return out
        dates = pd.to_datetime(df['date'])
        start = dates.min().date().strftime('%Y-%m-%d')
        end = dates.max().date().strftime('%Y-%m-%d')
        daily = get_polygon_daily_bars(self.underlying, start, end)
        if daily.empty or 'vwap' not in daily.columns:
            out['vwap_d'] = 0.0
            return out
        daily['date'] = pd.to_datetime(daily['date']).dt.date
        vwap = pd.to_numeric(daily['vwap'], errors='coerce')
        if self.shift_days:
            vwap = vwap.shift(self.shift_days)
        daily['vwap_d'] = vwap.fillna(0.0)
        mapped = pd.Series(pd.to_datetime(df['date']).dt.date).map(daily.set_index('date')['vwap_d']).astype(float).fillna(0.0)
        out['vwap_d'] = mapped.values
        return out

