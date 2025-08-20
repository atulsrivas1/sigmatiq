from __future__ import annotations
from typing import Optional, List, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
import pandas as pd
import numpy as np

from sigma_core.registry.signals_registry import (
    fetch_signals as db_fetch_signals,
    upsert_option_signals as db_upsert_option_signals,
)
try:
    from sigma_core.registry.signals_registry import replace_option_signals as db_replace_option_signals
except Exception:
    db_replace_option_signals = None
from sigma_core.data.sources.polygon import get_polygon_hourly_bars
try:
    from sigma_core.registry.signals_registry import fetch_option_signals as db_fetch_option_signals
except Exception:
    db_fetch_option_signals = None
from sigma_core.data.sources.polygon import get_polygon_option_chain_snapshot, get_polygon_option_quotes
from sigma_platform.io import workspace_paths as _ws_paths

router = APIRouter()


class OptionsOverlayRequest(BaseModel):
    model_id: str
    pack_id: Optional[str] = 'swingsigma'
    date: Optional[str] = None  # YYYY-MM-DD
    expiry: Optional[str] = None  # YYYY-MM-DD; if absent and dte_target provided, use date + dte_target
    dte_target: Optional[int] = None
    option_mode: Optional[str] = 'single'  # 'single' | 'vertical'
    spread_width: Optional[float] = 5.0
    side_override: Optional[str] = None  # 'call' | 'put'
    target_delta: float = 0.35
    min_oi: int = 0
    limit: int = 100
    # Parity controls
    include_underlying_parity: Optional[bool] = True
    include_premium_parity: Optional[bool] = True
    write_parity_csv: Optional[bool] = False


def _occ_symbol(underlying: str, expiry: date, strike: float, side: str) -> str:
    exp = expiry.strftime('%y%m%d')
    tchar = 'C' if side.lower().startswith('c') else 'P'
    cents = int(round(float(strike) * 1000))
    return f"O:{underlying.upper()}{exp}{tchar}{cents:08d}"


@router.post('/options_overlay')
def options_overlay_ep(payload: OptionsOverlayRequest):
    try:
        # Resolve signals source (DB preferred; else CSV fallback)
        d = payload.date
        if not d:
            d = date.today().isoformat()
        sig_rows: List[Dict[str, Any]] = []
        use_db = db_fetch_signals is not None
        if use_db:
            sig_rows = db_fetch_signals(model_id=payload.model_id, date_eq=d, limit=payload.limit) or []
        if not sig_rows:
            # CSV fallback
            from sigma_platform.io import workspace_paths as _ws
            ws = _ws(payload.model_id, payload.pack_id or 'swingsigma')
            csv_path = ws['live'] / 'signals.csv'
            if not csv_path.exists():
                return {'ok': False, 'error': f'No signals found in DB or CSV for {payload.model_id} on {d}'}
            df_csv = pd.read_csv(csv_path)
            if 'date' in df_csv.columns:
                try:
                    df_csv = df_csv[pd.to_datetime(df_csv['date']).dt.date == date.fromisoformat(d)]
                except Exception:
                    pass
            for _, r in df_csv.head(int(payload.limit or 100)).iterrows():
                sig_rows.append({'id': None,'ticker': r.get('ticker'),'side': r.get('side','buy'),'entry_ref_px': r.get('entry_ref_px'),'close': r.get('close'),'stop_px': r.get('stop_px'),'target_px': r.get('target_px')})
        if not sig_rows:
            return {'ok': False, 'error': f'No signals for model {payload.model_id} on {d}'}
        exp = date.fromisoformat(payload.expiry) if payload.expiry else (date.fromisoformat(d) + pd.Timedelta(days=int(payload.dte_target or 0)).to_pytimedelta())
        overlays: List[Dict[str, Any]] = []
        written = 0
        for r in sig_rows:
            ticker = str(r.get('ticker') or '').upper()
            if not ticker:
                continue
            side = ('call' if payload.side_override.lower().startswith('c') else 'put') if payload.side_override else ('call' if str(r.get('side') or 'buy').lower().startswith('b') else 'put')
            snap = get_polygon_option_chain_snapshot(ticker, exp)
            if snap is None or snap.empty:
                continue
            df = snap.copy()
            df = df[df['contract_type'].str.lower() == side]
            if payload.min_oi:
                df = df[pd.to_numeric(df['open_interest'], errors='coerce').fillna(0.0) >= float(payload.min_oi)]
            if df.empty:
                continue
            df['delta_abs'] = (pd.to_numeric(df['delta'], errors='coerce').astype(float) - float(payload.target_delta))**2
            df = df.sort_values(['delta_abs','implied_volatility'], ascending=[True, True])
            pick = df.iloc[0]
            strike = float(pick.get('strike'))
            iv = None
            try:
                iv = float(pick.get('implied_volatility')) if pick.get('implied_volatility') is not None else None
            except Exception:
                iv = None
            mid = pick.get('mid')
            try:
                mid = float(mid) if mid is not None else None
            except Exception:
                mid = None
            if mid is None:
                try:
                    qdf = get_polygon_option_quotes(ticker, exp, strike, side, date.fromisoformat(d), date.fromisoformat(d))
                    if not qdf.empty:
                        last = qdf.tail(1).iloc[0]
                        b = last.get('bid'); a = last.get('ask')
                        if pd.notna(b) and pd.notna(a):
                            mid = 0.5 * (float(b) + float(a))
                except Exception:
                    pass
            entry_ref = float(r.get('entry_ref_px') or r.get('close') or 0.0)
            stop_u = r.get('stop_px'); target_u = r.get('target_px')
            try:
                delta_val = float(pick.get('delta')) if pick.get('delta') is not None else None
            except Exception:
                delta_val = None
            prem_entry = mid
            prem_stop = None
            prem_target = None
            if prem_entry is not None and delta_val is not None and stop_u is not None and target_u is not None:
                try:
                    d_down = max(0.0, float(entry_ref) - float(stop_u))
                    d_up = max(0.0, float(target_u) - float(entry_ref))
                    prem_stop = max(0.0, prem_entry - delta_val * d_down)
                    prem_target = max(0.0, prem_entry + delta_val * d_up)
                except Exception:
                    pass
            
            if (payload.option_mode or 'single') == 'vertical':
                width = float(payload.spread_width or 5.0)
                short_strike = strike + width
                short = df[(pd.to_numeric(df['strike'], errors='coerce') - short_strike).abs() < 1e-6]
                short_mid = None; short_delta=None
                if not short.empty:
                    srow = short.iloc[0]
                    short_mid = float(srow.get('mid')) if srow.get('mid') is not None else None
                    try:
                        short_delta = float(srow.get('delta')) if srow.get('delta') is not None else None
                    except Exception: pass
                if short_mid is None:
                    try:
                        qdf2 = get_polygon_option_quotes(ticker, exp, short_strike, side, date.fromisoformat(d), date.fromisoformat(d))
                        if not qdf2.empty:
                            last2 = qdf2.tail(1).iloc[0]
                            b2 = last2.get('bid'); a2 = last2.get('ask')
                            if pd.notna(b2) and pd.notna(a2):
                                short_mid = 0.5 * (float(b2) + float(a2))
                    except Exception: pass
                net_debit = (max(0.0, prem_entry - short_mid) if (prem_entry is not None and short_mid is not None) else None)
                delta_net = (float(delta_val) - float(short_delta)) if (delta_val is not None and short_delta is not None) else None
                stop_val = None; target_val=None
                if net_debit is not None and delta_net is not None and stop_u is not None and target_u is not None:
                    try:
                        d_down = max(0.0, float(entry_ref) - float(stop_u))
                        d_up = max(0.0, float(target_u) - float(entry_ref))
                        stop_val = max(0.0, net_debit - delta_net * d_down)
                        target_val = max(0.0, net_debit + delta_net * d_up)
                    except Exception: pass
                overlays.append({
                'signal_id': int(r.get('id')) if r.get('id') is not None else None,
                'occ_symbol': _occ_symbol(ticker, exp, strike, side),
                'expiry': exp,
                'strike': strike,
                'type': side,
                'delta': float(pick.get('delta')) if pick.get('delta') is not None else None,
                'iv_used': iv,
                'entry_premium_est': prem_entry,
                'stop_premium_est': prem_stop,
                'target_premium_est': prem_target,
                'pricing_estimate': True if prem_entry is None else False,
                'legs_json': None,
                'net_debit_credit': net_debit,
                'stop_value': stop_val,
                'target_value': target_val,
            })
        if overlays:
            if use_db and (db_replace_option_signals is not None or db_upsert_option_signals is not None):
                # Prefer replace-by-signal_id to avoid duplicates on re-runs
                if db_replace_option_signals is not None and all(o.get('signal_id') is not None for o in overlays):
                    written = db_replace_option_signals(overlays)
                else:
                    written = db_upsert_option_signals(overlays)
            else:
                from sigma_platform.io import workspace_paths as _ws2
                ws2=_ws2(payload.model_id, payload.pack_id or 'swingsigma')
                out_csv = ws2['live'] / 'options_signals.csv'
                pd.DataFrame(overlays).to_csv(out_csv, index=False)
        # Parity summary (next session using underlying brackets)
        parity = None
        if bool(payload.include_underlying_parity):
            try:
                if sig_rows:
                    # group by ticker for efficiency
                    from datetime import timedelta as _td
                    start_date = date.fromisoformat(d)
                    next_date = start_date + _td(days=1)
                    bars_cache: Dict[str, pd.DataFrame] = {}
                    trades = 0; hits = 0
                    for r, o in zip(sig_rows, overlays):
                        t = str(r.get('ticker') or '').upper()
                        if not t:
                            continue
                        if t not in bars_cache:
                            try:
                                bars = get_polygon_hourly_bars(t, start_date.isoformat(), next_date.isoformat())
                            except Exception:
                                bars = pd.DataFrame()
                            bars_cache[t] = bars
                        bars = bars_cache[t]
                        if bars is None or bars.empty:
                            continue
                        # derive per-date
                        bars = bars.copy()
                        bars['_date'] = pd.to_datetime(bars.get('datetime') or bars.get('timestamp') or bars.index).dt.date
                        # pick next session bars
                        brs = bars[bars['_date'] == next_date]
                        if brs.empty:
                            continue
                        entry = float(brs['open'].iloc[0]) if 'open' in brs.columns else None
                        stop_u = r.get('stop_px'); target_u = r.get('target_px')
                        if entry is None or stop_u is None or target_u is None:
                            continue
                        trades += 1
                        hit = None
                        for _, row in brs.iterrows():
                            h = float(row.get('high') or entry); l = float(row.get('low') or entry)
                            if h >= float(target_u):
                                hit = True; break
                            if l <= float(stop_u):
                                hit = False; break
                        if hit is True:
                            hits += 1
                    if trades:
                        parity = {'ok': True, 'trades': trades, 'hit_rate': float(hits)/float(trades)}
            except Exception:
                parity = None

        # Premium-based parity (options quotes), per overlay
        parity_prem = None
        parity_csv = None
        if bool(payload.include_premium_parity):
            try:
                from datetime import timedelta as _td
                start_date = date.fromisoformat(d)
                next_date = start_date + _td(days=1)
                rows = []
                hits_t = 0; hits_s = 0; timeouts = 0; trades_p = 0
                for r, o in zip(sig_rows, overlays):
                    t = str(r.get('ticker') or '').upper()
                    strike = float(o.get('strike')) if o.get('strike') is not None else None
                    side = str(o.get('type')) if o.get('type') is not None else None
                    if not t or strike is None or side is None:
                        continue
                    # thresholds and entry
                    is_vertical = (payload.option_mode or 'single') == 'vertical'
                    if not is_vertical:
                        entry = o.get('entry_premium_est')
                        stopv = o.get('stop_premium_est')
                        targetv = o.get('target_premium_est')
                    else:
                        entry = o.get('net_debit_credit')
                        stopv = o.get('stop_value')
                        targetv = o.get('target_value')
                    if entry is None or stopv is None or targetv is None:
                        continue
                    # fetch quotes for next_date
                    try:
                        q_long = get_polygon_option_quotes(t, o['expiry'], strike, side, next_date, next_date)
                    except Exception:
                        q_long = None
                    if q_long is None or q_long.empty:
                        continue
                    # compute series for single or vertical
                    import pandas as _pd
                    q_long = q_long.copy()
                    q_long['mid'] = _pd.to_numeric(q_long.get('bid'), errors='coerce').fillna(0.0).astype(float)
                    ask = _pd.to_numeric(q_long.get('ask'), errors='coerce').fillna(0.0).astype(float)
                    q_long['mid'] = (q_long['mid'] + ask) / 2.0
                    ser = q_long[['mid']].copy()
                    if is_vertical:
                        # get short leg quotes and compute net
                        width = float(payload.spread_width or 5.0)
                        short_strike = strike + width
                        try:
                            q_short = get_polygon_option_quotes(t, o['expiry'], short_strike, side, next_date, next_date)
                        except Exception:
                            q_short = None
                        if q_short is None or q_short.empty:
                            continue
                        q_short = q_short.copy()
                        q_short['mid'] = _pd.to_numeric(q_short.get('bid'), errors='coerce').fillna(0.0).astype(float)
                        ask2 = _pd.to_numeric(q_short.get('ask'), errors='coerce').fillna(0.0).astype(float)
                        q_short['mid'] = (q_short['mid'] + ask2) / 2.0
                        # align on timestamp
                        ts_col = 'timestamp' if 'timestamp' in q_long.columns else q_long.columns[0]
                        ts2 = 'timestamp' if 'timestamp' in q_short.columns else q_short.columns[0]
                        try:
                            a = _pd.DataFrame({'ts': _pd.to_datetime(q_long[ts_col]), 'long_mid': q_long['mid']})
                            b = _pd.DataFrame({'ts': _pd.to_datetime(q_short[ts2]), 'short_mid': q_short['mid']})
                            dfm = _pd.merge_asof(a.sort_values('ts'), b.sort_values('ts'), on='ts', direction='nearest')
                            dfm['mid'] = dfm['long_mid'] - dfm['short_mid']
                            ser = dfm[['ts','mid']]
                        except Exception:
                            continue
                    # evaluate thresholds
                    try:
                        ser = ser.dropna()
                        if ser.empty:
                            continue
                        # Determine first hit order
                        hit_t = False; hit_s = False
                        for _, row in ser.iterrows():
                            m = float(row.get('mid'))
                            if m >= float(targetv):
                                hit_t = True
                                break
                            if m <= float(stopv):
                                hit_s = True
                                break
                        trades_p += 1
                        if hit_t:
                            hits_t += 1
                            outcome = 'target'
                        elif hit_s:
                            hits_s += 1
                            outcome = 'stop'
                        else:
                            timeouts += 1
                            outcome = 'timeout'
                        rows.append({
                            'ticker': t,
                            'occ_symbol': o.get('occ_symbol'),
                            'mode': ('vertical' if is_vertical else 'single'),
                            'entry_value': entry,
                            'stop_value': stopv,
                            'target_value': targetv,
                            'outcome': outcome,
                        })
                    except Exception:
                        continue
                if trades_p:
                    parity_prem = {
                        'ok': True,
                        'trades': trades_p,
                        'hit_rate_target': (hits_t / trades_p),
                        'hit_rate_stop': (hits_s / trades_p),
                        'timeouts': timeouts,
                    }
                    # Optional CSV
                    if bool(payload.write_parity_csv):
                        try:
                            ws = _ws_paths(payload.model_id, payload.pack_id or 'swingsigma')
                            out_csv2 = ws['reports'] / f"options_parity_{d}_{exp.strftime('%Y-%m-%d')}.csv"
                            import pandas as _pd
                            _pd.DataFrame(rows).to_csv(out_csv2, index=False)
                            parity_csv = str(out_csv2)
                        except Exception:
                            parity_csv = None
            except Exception:
                parity_prem = None

        exp_str = payload.expiry or (date.fromisoformat(d) + pd.Timedelta(days=int(payload.dte_target or 0))).strftime('%Y-%m-%d')
        return {'ok': True, 'count': len(overlays), 'written': written, 'date': d, 'expiry': exp_str, 'parity': parity, 'parity_premium': parity_prem, 'parity_csv': parity_csv}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


@router.get('/option_signals')
def option_signals_list(
    model_id: Optional[str] = None,
    pack_id: Optional[str] = None,
    date: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    tickers: Optional[str] = None,
    expiry: Optional[str] = None,
    occ_symbol: Optional[str] = None,
    limit: int = 200,
    offset: int = 0,
):
    if db_fetch_option_signals is None:
        return {'ok': True, 'rows': [], 'count': 0, 'limit': int(limit), 'offset': int(offset), 'next_offset': int(offset), 'warning': 'DB not configured'}
    try:
        tickers_list = None
        if tickers:
            tickers_list = [t.strip().upper() for t in tickers.split(',') if t.strip()]
        rows = db_fetch_option_signals(
            model_id=model_id,
            pack_id=pack_id,
            date_eq=date,
            start=start,
            end=end,
            tickers=tickers_list,
            expiry=expiry,
            occ_symbol=occ_symbol,
            limit=int(limit),
            offset=int(offset),
        )
        return {'ok': True, 'rows': rows, 'count': len(rows), 'limit': int(limit), 'offset': int(offset), 'next_offset': int(offset) + len(rows)}
    except Exception as e:
        msg = str(e)
        if 'Database env vars missing' in msg or 'psycopg2' in msg:
            return {'ok': True, 'rows': [], 'count': 0, 'limit': int(limit), 'offset': int(offset), 'next_offset': int(offset), 'warning': msg}
        return {'ok': False, 'error': msg}


@router.get('/options/expirations')
def list_expirations(ticker: str, start: Optional[str] = None, weeks: int = 12):
    """
    Convenience helper: probe upcoming weekly Fridays for available expirations by checking if a chain snapshot has data.
    This avoids wiring a separate Polygon reference endpoint and works with existing adapters.
    """
    try:
        from datetime import datetime, timedelta
        base = datetime.strptime(start, '%Y-%m-%d').date() if start else date.today()
        # Find next Friday from base
        days_ahead = (4 - base.weekday()) % 7  # Monday=0.. Sunday=6; Friday=4
        first = base + timedelta(days=days_ahead)
        out = []
        d = first
        for i in range(max(1, weeks)):
            try:
                snap = get_polygon_option_chain_snapshot(ticker.upper(), d)
                has_any = (snap is not None) and (not snap.empty)
                out.append({'date': d.isoformat(), 'has_chain': bool(has_any), 'count': int(len(snap)) if has_any else 0})
            except Exception:
                out.append({'date': d.isoformat(), 'has_chain': False, 'count': 0})
            d = d + timedelta(days=7)
        return {'ok': True, 'ticker': ticker.upper(), 'start': base.isoformat(), 'weeks': weeks, 'expirations': out}
    except Exception as e:
        return {'ok': False, 'error': str(e)}
