#!/usr/bin/env python3
"""
Generate "live alerts" from a trained model by scoring the most recent rows
from a built matrix and writing a compact CSV under live_data/<model_id>/signals.csv.

Usage:
  python scripts/generate_live_alerts.py \
    --model_id spy_opt_0dte_hourly \
    --csv matrices/spy_opt_0dte_hourly/training_matrix_built.csv \
    --threshold 0.60 \
    --allowed_hours 13,14,15

Notes:
  - This does not fetch fresh data; it scores an existing matrix file.
  - For true intraday alerts, pair this with a fresh short build (today) and rerun.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
try:
    from edge_core.registry.signals_registry import upsert_signals as db_upsert_signals
except Exception:
    db_upsert_signals = None
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model_id', required=True)
    ap.add_argument('--csv', required=False)
    ap.add_argument('--threshold', type=float, default=0.6)
    ap.add_argument('--allowed_hours', default=None, help='comma-separated ET hours, e.g., 13,14,15')
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    art = root / 'artifacts' / args.model_id / 'gbm.pkl'
    if not art.exists():
        raise SystemExit(f"Model artifact missing: {art}")
    payload = joblib.load(art)
    model = payload.get('model')
    features = payload.get('features')
    label_encoder = payload.get('label_encoder')
    if model is None or features is None:
        raise SystemExit('Invalid model artifact (missing model or features)')

    csv_path = Path(args.csv) if args.csv else (root / 'matrices' / args.model_id / 'training_matrix_built.csv')
    if not csv_path.exists():
        raise SystemExit(f"Matrix CSV not found: {csv_path}")
    df = pd.read_csv(csv_path)
    # Filter to allowed hours if provided
    if args.allowed_hours and 'hour_et' in df.columns:
        hours = [int(x) for x in str(args.allowed_hours).split(',') if x]
        df = df[df['hour_et'].isin(hours)].copy()
    if df.empty:
        raise SystemExit('No rows to score after filtering')
    # Score the most recent session
    if 'date' in df.columns:
        last_day = pd.to_datetime(df['date']).dt.date.max()
        df = df[pd.to_datetime(df['date']).dt.date == last_day].copy()
    # Ensure feature availability
    missing = [c for c in features if c not in df.columns]
    for c in missing:
        df[c] = 0.0
    X = df[features].fillna(0.0).values
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(X)
        # choose best class per row
        best_idx = np.argmax(proba, axis=1)
        best_conf = proba[np.arange(len(proba)), best_idx]
        if label_encoder is not None:
            labels = label_encoder.inverse_transform(best_idx)
        else:
            labels = best_idx.astype(str)
    else:
        # fallback: decision_function or raw scores
        scores = model.predict(X)
        best_conf = np.ones(len(scores), dtype=float)
        labels = scores

    mask = best_conf >= float(args.threshold)
    alerts = df.loc[mask, ['date','hour_et']].copy() if 'hour_et' in df.columns else df.loc[mask, ['date']].copy()
    alerts['predicted_label'] = labels[mask]
    alerts['confidence'] = best_conf[mask]
    alerts['generated_at'] = datetime.utcnow().isoformat()

    # Optional: add ATR-based brackets for stocks if close and ATR_14 present
    try:
        if 'close' in df.columns and 'atr_14' in df.columns:
            # Use last available close and atr per row
            close = pd.to_numeric(df.loc[mask, 'close'], errors='coerce').astype(float)
            atr = pd.to_numeric(df.loc[mask, 'atr_14'], errors='coerce').astype(float)
            atr = atr.fillna(0.0).clip(lower=0.0)
            atr_floor = np.maximum(atr.values, 0.0005 * np.maximum(close.values, 1e-6))
            entry_ref = close.values
            k_stop = 1.2; k_tgt = 2.0; tstop = 120
            stop_px = entry_ref - k_stop * atr_floor
            target_px = entry_ref + k_tgt * atr_floor
            rr = np.where((entry_ref - stop_px) > 0, (target_px - entry_ref) / (entry_ref - stop_px), np.nan)
            alerts['side'] = 'buy'
            alerts['entry_mode'] = 'next_session_open'
            alerts['entry_ref_px'] = entry_ref
            alerts['stop_px'] = stop_px
            alerts['target_px'] = target_px
            alerts['time_stop_minutes'] = tstop
            alerts['rr'] = rr
    except Exception:
        pass

    out_dir = root / 'live_data' / args.model_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / 'signals.csv'
    mode = 'w'
    header = True
    if out_csv.exists():
        # append
        mode = 'a'; header = False
    alerts.to_csv(out_csv, index=False, mode=mode, header=header)
    print(f"Wrote {len(alerts)} alerts to {out_csv}")

    # Optional DB upsert
    try:
        if db_upsert_signals is not None and len(alerts):
            records = []
            for _, r in alerts.iterrows():
                rec = {
                    'date': pd.to_datetime(r.get('date')).date() if 'date' in r else None,
                    'model_id': args.model_id,
                    'ticker': str(r.get('ticker') or r.get('symbol') or ''),
                    'side': str(r.get('side') or 'buy'),
                    'entry_mode': str(r.get('entry_mode') or 'next_session_open'),
                    'entry_ref_px': float(r.get('entry_ref_px')) if r.get('entry_ref_px') is not None else None,
                    'stop_px': float(r.get('stop_px')) if r.get('stop_px') is not None else None,
                    'target_px': float(r.get('target_px')) if r.get('target_px') is not None else None,
                    'time_stop_minutes': int(r.get('time_stop_minutes')) if r.get('time_stop_minutes') is not None else None,
                    'rr': float(r.get('rr')) if r.get('rr') is not None else None,
                    'score_total': float(r.get('confidence')) if r.get('confidence') is not None else None,
                    'rank': None,
                }
                records.append(rec)
            if records:
                db_upsert_signals(records)
    except Exception:
        pass


if __name__ == '__main__':
    main()
