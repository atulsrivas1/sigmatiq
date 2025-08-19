from __future__ import annotations
import pandas as pd
import numpy as np
import pytz


def label_forward_return_days(df: pd.DataFrame, *, days: int = 5, classify: bool = True, band: float = 0.001, tz: str = 'US/Eastern') -> pd.DataFrame:
    """
    Compute forward N-day return labels on an intraday timeline.
    - If classify=True: produces categorical y (UP/DOWN/FLAT by band) and stores numeric ret in `ret_fwd_{days}d`.
    - If classify=False: sets y to the numeric forward return.
    Assumes df has 'date' and 'close'. Uses last close per day and maps result back to all rows of that day.
    """
    out = df.copy()
    if 'date' not in out.columns or 'close' not in out.columns:
        out[f'ret_fwd_{days}d'] = np.nan
        out['y'] = np.nan
        out['y_syn'] = np.nan
        return out
    ts = pd.to_datetime(out['date'])
    if ts.dt.tz is None:
        ts = ts.dt.tz_localize(tz)
    else:
        ts = ts.dt.tz_convert(tz)
    s = out.copy(); s['ts'] = ts; s = s.sort_values('ts')
    s['session_date'] = s['ts'].dt.date
    last_close = s.groupby('session_date').tail(1).set_index('session_date')['close'].astype(float)
    days_list = sorted(last_close.index)
    fwd_map = {}
    for i, d in enumerate(days_list):
        j = i + int(days)
        if j < len(days_list):
            c0 = float(last_close.loc[d])
            cN = float(last_close.loc[days_list[j]])
            fwd_map[d] = (cN - c0) / (c0 + 1e-12)
        else:
            fwd_map[d] = np.nan
    sess = ts.dt.date
    ret = [fwd_map.get(d, np.nan) for d in sess]
    out[f'ret_fwd_{days}d'] = ret
    if classify:
        y = np.where(out[f'ret_fwd_{days}d'] > band, 'UP', np.where(out[f'ret_fwd_{days}d'] < -band, 'DOWN', 'FLAT'))
        out['y'] = y; out['y_syn'] = y
    else:
        out['y'] = out[f'ret_fwd_{days}d']
        out['y_syn'] = out['y']
    return out

