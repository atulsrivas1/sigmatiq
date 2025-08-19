from ..base import Indicator
import pandas as pd

class IntradayVWAP(Indicator):
    CATEGORY = "volume"
    SUBCATEGORY = "intraday_vwap"

    def __init__(self, price_col: str = 'vwap', volume_col: str = 'volume'):
        self.price_col = price_col
        self.volume_col = volume_col

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        required = {self.volume_col}
        if not required.issubset(df.columns) or (self.price_col not in df.columns and 'close' not in df.columns):
            out['vwap_intraday'] = 0.0
            return out
        price = pd.to_numeric(df.get(self.price_col, df.get('close')), errors='coerce').astype(float)
        vol = pd.to_numeric(df[self.volume_col], errors='coerce').astype(float).fillna(0.0)
        # Group by session date component (assumes df['date'] is tz-aware or date-indexable)
        if 'date' in df.columns:
            sess = pd.to_datetime(df['date']).dt.date
        else:
            # fallback: a rolling cumulative without daily reset
            sess = pd.Series([None]*len(df), index=df.index)
        numer = (price * vol)
        denom = vol
        vwap = numer.groupby(sess).cumsum() / (denom.groupby(sess).cumsum() + 1e-12)
        out['vwap_intraday'] = vwap.fillna(0.0)
        return out

