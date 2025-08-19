from ..base import Indicator
import pandas as pd
import numpy as np


class ReturnsLast30m(Indicator):
    NAME = "returns_last_30m"
    CATEGORY = "intraday"
    SUBCATEGORY = "windowed"

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns or 'close' not in df.columns:
            out['returns_last_30m'] = float('nan')
            return out
        ts = pd.to_datetime(df['date'])
        close = pd.to_numeric(df['close'], errors='coerce').astype(float)
        # For each timestamp, look back 30 minutes and compute return
        ref = ts - pd.Timedelta(minutes=30)
        # merge_asof to align ref times to nearest prior bar
        a = pd.DataFrame({'ts': ts, 'close': close}).sort_values('ts')
        b = a.rename(columns={'ts':'ref_ts','close':'ref_close'})
        # We need to merge for each row the ref_close from the latest prior ref_ts
        merged = pd.merge_asof(a, b, left_on='ts', right_on='ref_ts', direction='backward', tolerance=pd.Timedelta('1D'))
        # But this just aligns on same ts; instead, reindex b on ts and use searchsorted logic
        # Simpler: create a mapping from ts to close and lookup nearest prior ref time via asof
        s_close = a.set_index('ts')['close'].sort_index()
        ref_close_vals = s_close.reindex(s_close.index.union(ref)).sort_index().asof(ref).values
        ret = (close.values - ref_close_vals) / np.where(ref_close_vals==0.0, np.nan, ref_close_vals)
        out['returns_last_30m'] = ret
        return out

