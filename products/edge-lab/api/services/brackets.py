from __future__ import annotations
from typing import Dict
import numpy as np
import pandas as pd


def apply_stock_brackets(scored: pd.DataFrame, exec_br: Dict) -> pd.DataFrame:
    """
    Add stock bracket fields to the scored DataFrame using execution.brackets policy.
    Required columns: close, (optional) atr_* (first atr_ column found).
    Adds: side, entry_mode, entry_ref_px, stop_px, target_px, time_stop_minutes, rr.
    Applies min_rr filter if provided.
    """
    if scored is None or scored.empty:
        return scored
    k_stop = float(exec_br.get('atr_mult_stop', 1.2))
    k_tgt = float(exec_br.get('atr_mult_target', 2.0))
    tstop = int(exec_br.get('time_stop_minutes', 120))
    min_rr = float(exec_br.get('min_rr', 0.0) or 0.0)
    entry_mode = str(exec_br.get('entry_mode', 'next_session_open'))

    close_arr = np.array(pd.to_numeric(scored.get('close', pd.Series(np.nan, index=scored.index))), dtype=float)
    atr_cols = [c for c in scored.columns if c.startswith('atr_')]
    atr_arr = np.array(pd.to_numeric(scored[atr_cols[0]] if atr_cols else pd.Series(np.nan, index=scored.index)), dtype=float)
    atr_arr = np.where(~np.isfinite(atr_arr), 0.0, atr_arr)
    # ATR floor at 0.05% of price
    atr_eff = np.maximum(atr_arr, 0.0005 * np.maximum(close_arr, 1e-6))
    entry_ref = close_arr.copy()
    stop_px = entry_ref - k_stop * atr_eff
    target_px = entry_ref + k_tgt * atr_eff
    rr = np.where((entry_ref - stop_px) > 0, (target_px - entry_ref) / (entry_ref - stop_px), np.nan)
    scored = scored.copy()
    scored['side'] = 'buy'
    scored['entry_mode'] = entry_mode
    scored['entry_ref_px'] = entry_ref
    scored['stop_px'] = stop_px
    scored['target_px'] = target_px
    scored['time_stop_minutes'] = tstop
    scored['rr'] = rr
    if min_rr > 0:
        scored = scored[(pd.to_numeric(scored['rr'], errors='coerce') >= min_rr)].copy()
    return scored

