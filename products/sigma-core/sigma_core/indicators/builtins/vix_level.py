from ..base import Indicator
import pandas as pd
import numpy as np
from datetime import datetime
from ...data.sources.polygon import get_polygon_index_daily_bars


class VIXLevel(Indicator):
    NAME = "vix_level"
    CATEGORY = "regime"
    SUBCATEGORY = "vix"

    def __init__(self, index_ticker: str = "I:VIX"):
        self.index_ticker = index_ticker

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['vix_level'] = float('nan')
            return out
        d0 = pd.to_datetime(df['date']).dt.date.min()
        d1 = pd.to_datetime(df['date']).dt.date.max()
        start = pd.Timestamp(d0).strftime('%Y-%m-%d')
        end = pd.Timestamp(d1).strftime('%Y-%m-%d')
        try:
            vix = get_polygon_index_daily_bars(self.index_ticker, start, end)
        except Exception:
            vix = pd.DataFrame()
        if vix.empty:
            out['vix_level'] = float('nan')
            return out
        vix['d'] = pd.to_datetime(vix['date']).dt.tz_convert('US/Eastern').dt.date
        m = pd.to_datetime(df['date']).dt.tz_convert('US/Eastern').dt.date
        map_close = vix.set_index('d')['close'].to_dict()
        out['vix_level'] = m.map(lambda x: map_close.get(x, np.nan)).astype(float)
        return out

