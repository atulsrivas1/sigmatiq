from __future__ import annotations
import pandas as pd
import numpy as np
import pytz


def _pick_at_time(g: pd.DataFrame, hhmm: str, tz: str = 'US/Eastern') -> pd.Timestamp:
    t = pd.to_datetime(g.index.date[0].strftime('%Y-%m-%d') + ' ' + hhmm).tz_localize(tz)
    sub = g[g.index >= t]
    return sub.index[0] if not sub.empty else g.index[-1]


def label_headfake_reversal(df: pd.DataFrame, *, open_time: str = '09:30', window_end: str = '10:30', min_open_move_atr: float = 0.5, min_reversal_move_atr: float = 0.5, tz: str = 'US/Eastern') -> pd.DataFrame:
    """
    Labels 1 at window_end if the open→window_end move reverses into the close by at least min_reversal_move_atr*ATR.
    Emits 'y' as 0/1 across all rows of that day, and 'y_syn' for compatibility.
    Requires columns: 'date','close'; optional 'atr_14' or 'rolling_std_20' as ATR proxy.
    """
    out = df.copy()
    if 'date' not in out.columns or 'close' not in out.columns:
        out['y_syn'] = 'FLAT'; out['y'] = 'FLAT'; return out
    x = out.copy()
    x['ts'] = pd.to_datetime(x['date'])
    if x['ts'].dt.tz is None:
        x['ts'] = x['ts'].dt.tz_localize(tz)
    else:
        x['ts'] = x['ts'].dt.tz_convert(tz)
    x = x.set_index('ts').sort_index()
    labels = []
    idxs = []
    for day, g in x.groupby(x.index.date):
        g = g.sort_index()
        try:
            t_open = _pick_at_time(g, open_time, tz)
            t_end = _pick_at_time(g, window_end, tz)
            t_close = _pick_at_time(g, '16:00', tz)
        except Exception:
            continue
        p_open = float(g.loc[t_open, 'close'])
        p_end = float(g.loc[t_end, 'close'])
        p_close = float(g.loc[t_close, 'close'])
        early = p_end - p_open
        late = p_close - p_end
        # ATR proxy
        if 'atr_14' in g.columns:
            atr = float(pd.to_numeric(g.loc[:t_end, 'atr_14'], errors='coerce').tail(1).iloc[0])
        elif 'rolling_std_20' in g.columns:
            atr = float(pd.to_numeric(g.loc[:t_end, 'rolling_std_20'], errors='coerce').tail(1).iloc[0])
        else:
            atr = float(np.nanstd(pd.to_numeric(g['close'], errors='coerce').pct_change().dropna())) * p_end
        cond_mag = (abs(early) >= min_open_move_atr * max(atr, 1e-9)) and (abs(late) >= min_reversal_move_atr * max(atr, 1e-9))
        cond_sign = (early * late) < 0
        y = 1 if (cond_mag and cond_sign) else 0
        labels.append(y); idxs.append(day)
    # Broadcast per-day label to rows
    day_map = {d: y for d, y in zip(idxs, labels)}
    days = pd.to_datetime(out['date']).dt.tz_convert(tz).dt.date
    out['y'] = [day_map.get(d, 0) for d in days]
    out['y_syn'] = out['y']
    return out


def label_pin_drift(df: pd.DataFrame, *, drift_start_time: str = '15:00', min_pull_atr: float = 0.2, tz: str = 'US/Eastern') -> pd.DataFrame:
    """
    Labels 1 if price drifts toward the nearest OI/gamma peak from drift_start_time to close by >= min_pull_atr*ATR.
    Requires 'close','date'; optional 'oi_peak_strike' or 'gamma_peak_strike' and 'atr_14' or 'rolling_std_20'.
    """
    out = df.copy()
    if 'date' not in out.columns or 'close' not in out.columns:
        out['y_syn'] = 0; out['y'] = 0; return out
    x = out.copy()
    x['ts'] = pd.to_datetime(x['date'])
    if x['ts'].dt.tz is None:
        x['ts'] = x['ts'].dt.tz_localize(tz)
    else:
        x['ts'] = x['ts'].dt.tz_convert(tz)
    x = x.set_index('ts').sort_index()
    labels = []
    idxs = []
    for day, g in x.groupby(x.index.date):
        g = g.sort_index()
        try:
            t_start = _pick_at_time(g, drift_start_time, tz)
            t_close = _pick_at_time(g, '16:00', tz)
        except Exception:
            continue
        p_start = float(g.loc[t_start, 'close']); p_close = float(g.loc[t_close, 'close'])
        # choose target peak
        target = None
        if 'gamma_peak_strike' in g.columns:
            try: target = float(pd.to_numeric(g.loc[:t_close, 'gamma_peak_strike'], errors='coerce').tail(1).iloc[0])
            except Exception: target = None
        if (target is None or not np.isfinite(target)) and 'oi_peak_strike' in g.columns:
            try: target = float(pd.to_numeric(g.loc[:t_close, 'oi_peak_strike'], errors='coerce').tail(1).iloc[0])
            except Exception: target = None
        if target is None or not np.isfinite(target):
            labels.append(0); idxs.append(day); continue
        dist_start = abs(p_start - target); dist_close = abs(p_close - target)
        if 'atr_14' in g.columns:
            atr = float(pd.to_numeric(g.loc[:t_close, 'atr_14'], errors='coerce').tail(1).iloc[0])
        elif 'rolling_std_20' in g.columns:
            atr = float(pd.to_numeric(g.loc[:t_close, 'rolling_std_20'], errors='coerce').tail(1).iloc[0])
        else:
            atr = float(np.nanstd(pd.to_numeric(g['close'], errors='coerce').pct_change().dropna())) * p_close
        y = 1 if (dist_start - dist_close) >= (min_pull_atr * max(atr, 1e-9)) else 0
        labels.append(y); idxs.append(day)
    day_map = {d: y for d, y in zip(idxs, labels)}
    days = pd.to_datetime(out['date']).dt.tz_convert(tz).dt.date
    out['y'] = [day_map.get(d, 0) for d in days]
    out['y_syn'] = out['y']
    return out

