from __future__ import annotations
import pandas as pd
import numpy as np
import pytz


def label_close_to_open_direction(df: pd.DataFrame, *, tz: str = 'US/Eastern') -> pd.DataFrame:
    """
    Label each session by the direction from today's close to next day's first bar (approx open).
    Produces numeric return 'ret_close_to_open' and categorical 'y' (UP/DOWN/FLAT) via small band.
    Expects columns: 'date','close'. If hourly, uses last bar of the day as close and first bar next day as open.
    """
    out = df.copy()
    if 'date' not in out.columns or 'close' not in out.columns:
        out['ret_close_to_open'] = np.nan; out['y'] = 'FLAT'; out['y_syn'] = 'FLAT'; return out
    ts = pd.to_datetime(out['date'])
    if ts.dt.tz is None:
        ts = ts.dt.tz_localize(tz)
    else:
        ts = ts.dt.tz_convert(tz)
    s = out.copy(); s['ts'] = ts
    s = s.sort_values('ts')
    s['session_date'] = s['ts'].dt.date
    # close = last bar of session; open = first bar of next session
    last_per_day = s.groupby('session_date').tail(1).set_index('session_date')['close']
    first_per_day = s.groupby('session_date').head(1).set_index('session_date')['close']
    days = sorted(last_per_day.index)
    ret_map = {}
    for i in range(len(days)-1):
        d = days[i]; d_next = days[i+1]
        c = float(last_per_day.loc[d]); o_next = float(first_per_day.loc[d_next])
        ret_map[d] = (o_next - c) / (c + 1e-12)
    # map returns to all rows of day d
    ret_series = s['session_date'].map(lambda d: ret_map.get(d, np.nan)).astype(float)
    out['ret_close_to_open'] = ret_series.values
    # classify with tiny band
    thr = 0.0005
    y = np.where(out['ret_close_to_open'] > thr, 'UP', np.where(out['ret_close_to_open'] < -thr, 'DOWN', 'FLAT'))
    out['y'] = y; out['y_syn'] = y
    return out

