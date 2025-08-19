from ..base import Indicator
import pandas as pd
import numpy as np
from ...data.sources.polygon import get_polygon_index_daily_bars


class VIXTermSlope(Indicator):
    NAME = "vix_term_slope"
    CATEGORY = "regime"
    SUBCATEGORY = "vix_term"

    def __init__(self, near: str = "I:VIX", far: str = "I:VIX3M"):
        def map_term(x: str) -> str:
            if not x:
                return 'I:VIX'
            xs = str(x).lower()
            if xs.startswith('i:'):
                return x
            # Accept shorthand like '1m','3m','6m'
            if xs in {'1m','near'}:
                return 'I:VIX'
            if xs in {'3m','next'}:
                return 'I:VIX3M'
            if xs in {'6m'}:
                return 'I:VIX6M'
            return 'I:VIX'
        self.near = map_term(near)
        self.far = map_term(far)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['vix_term_slope'] = float('nan')
            return out
        d0 = pd.to_datetime(df['date']).dt.date.min()
        d1 = pd.to_datetime(df['date']).dt.date.max()
        start = pd.Timestamp(d0).strftime('%Y-%m-%d')
        end = pd.Timestamp(d1).strftime('%Y-%m-%d')
        try:
            ndf = get_polygon_index_daily_bars(self.near, start, end)
            fdf = get_polygon_index_daily_bars(self.far, start, end)
        except Exception:
            ndf = pd.DataFrame(); fdf = pd.DataFrame()
        if ndf.empty or fdf.empty:
            out['vix_term_slope'] = float('nan')
            return out
        ndf['d'] = pd.to_datetime(ndf['date']).dt.tz_convert('US/Eastern').dt.date
        fdf['d'] = pd.to_datetime(fdf['date']).dt.tz_convert('US/Eastern').dt.date
        nmap = ndf.set_index('d')['close'].to_dict()
        fmap = fdf.set_index('d')['close'].to_dict()
        dates = pd.to_datetime(df['date']).dt.tz_convert('US/Eastern').dt.date
        out['vix_term_slope'] = dates.map(lambda d: fmap.get(d, np.nan) - nmap.get(d, np.nan)).astype(float)
        return out
