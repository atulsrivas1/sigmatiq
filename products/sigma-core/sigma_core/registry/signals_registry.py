from __future__ import annotations
from typing import Any, Dict, Iterable, List, Optional
from psycopg2.extras import RealDictCursor
from datetime import date

from sigma_core.storage.relational import get_db


def upsert_signals(rows: Iterable[Dict[str, Any]]) -> int:
    """
    Upsert stock signals into the `signals` table.
    Each row should include at minimum: date, model_id, ticker.
    Optional fields are persisted when present.
    On conflict (date, model_id, ticker), updates core/scoring/exec fields.
    Returns number of rows written.
    """
    rows = list(rows)
    if not rows:
        return 0
    cols = [
        'date', 'model_id', 'ticker',
        'side', 'entry_mode', 'entry_ref_px', 'stop_px', 'target_px', 'time_stop_minutes', 'rr',
        'score_total', 'rank', 'score_breakout', 'score_momentum', 'score_trend_quality', 'score_alignment',
        'pack_id', 'policy_version', 'pack_sha', 'indicator_set_sha', 'model_config_sha', 'policy_sha',
    ]
    # Prepare value tuples with None for missing keys
    values: List[tuple] = []
    for r in rows:
        values.append(tuple(r.get(c) for c in cols))
    placeholders = ",".join(["(" + ",".join(["%s"] * len(cols)) + ")"] * len(values))
    update_set = ", ".join([f"{c} = EXCLUDED.{c}" for c in cols if c not in {'date','model_id','ticker'}])

    sql = f"""
        INSERT INTO signals ({', '.join(cols)})
        VALUES {placeholders}
        ON CONFLICT (date, model_id, ticker) DO UPDATE SET
          {update_set}
    """
    flat_params: List[Any] = []
    for t in values:
        flat_params.extend(t)
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, flat_params)
            conn.commit()
            return len(values)


def fetch_signals(
    *,
    model_id: Optional[str] = None,
    pack_id: Optional[str] = None,
    date_eq: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    tickers: Optional[List[str]] = None,
    limit: int = 200,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    """Fetch signals with simple filters.

    - model_id/pack_id optional filters
    - date_eq exact date OR start/end window (YYYY-MM-DD)
    - tickers optional list to include
    - limit defaults to 200
    Returns list of dict rows ordered by date DESC, rank ASC when present
    """
    where = []
    params: List[Any] = []
    if model_id:
        where.append("model_id = %s"); params.append(model_id)
    if pack_id:
        where.append("pack_id = %s"); params.append(pack_id)
    if date_eq:
        where.append("date = %s"); params.append(date_eq)
    else:
        if start:
            where.append("date >= %s"); params.append(start)
        if end:
            where.append("date <= %s"); params.append(end)
    if tickers:
        where.append("ticker = ANY(%s)"); params.append(tickers)
    sql = (
        "SELECT id, date, model_id, ticker, side, entry_mode, entry_ref_px, stop_px, target_px, time_stop_minutes, rr, "
        "score_total, rank, score_breakout, score_momentum, score_trend_quality, score_alignment, pack_id, policy_version, created_at "
        "FROM signals"
    )
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY date DESC, COALESCE(rank, 999999) ASC LIMIT %s OFFSET %s"
    params.append(int(limit))
    params.append(int(max(0, offset)))
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]


def upsert_option_signals(rows: List[Dict[str, Any]]) -> int:
    """Insert option overlay rows for signals. Does not update; callers should delete/replace as needed."""
    if not rows:
        return 0
    cols = [
        'signal_id','occ_symbol','expiry','strike','type','delta','iv_used',
        'entry_premium_est','stop_premium_est','target_premium_est','pricing_estimate','legs_json','net_debit_credit','stop_value','target_value'
    ]
    values = [tuple(r.get(c) for c in cols) for r in rows]
    placeholders = ",".join(["(" + ",".join(["%s"] * len(cols)) + ")"] * len(values))
    sql = f"INSERT INTO option_signals ({', '.join(cols)}) VALUES {placeholders}"
    flat: List[Any] = []
    for v in values:
        flat.extend(v)
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, flat)
            conn.commit()
            return len(values)


def fetch_option_signals(
    *,
    model_id: Optional[str] = None,
    pack_id: Optional[str] = None,
    date_eq: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    tickers: Optional[List[str]] = None,
    expiry: Optional[str] = None,
    occ_symbol: Optional[str] = None,
    limit: int = 200,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    """Fetch option overlay rows, optionally filtered by linked signal fields.

    Joins `option_signals` (os) with `signals` (s) to support model_id/pack_id/date/tickers filters.
    Returns list of dict rows ordered by expiry DESC, signal_id DESC.
    """
    where = []
    params: List[Any] = []
    if model_id:
        where.append("s.model_id = %s"); params.append(model_id)
    if pack_id:
        where.append("s.pack_id = %s"); params.append(pack_id)
    if date_eq:
        where.append("s.date = %s"); params.append(date_eq)
    else:
        if start:
            where.append("s.date >= %s"); params.append(start)
        if end:
            where.append("s.date <= %s"); params.append(end)
    if tickers:
        where.append("s.ticker = ANY(%s)"); params.append(tickers)
    if expiry:
        where.append("os.expiry = %s"); params.append(expiry)
    if occ_symbol:
        where.append("os.occ_symbol = %s"); params.append(occ_symbol)
    sql = (
        "SELECT os.id, os.signal_id, os.occ_symbol, os.expiry, os.strike, os.type, os.delta, os.iv_used, "
        "os.entry_premium_est, os.stop_premium_est, os.target_premium_est, os.pricing_estimate, os.legs_json, os.net_debit_credit, os.stop_value, os.target_value, "
        "s.date as signal_date, s.model_id, s.ticker, s.pack_id "
        "FROM option_signals os LEFT JOIN signals s ON s.id = os.signal_id"
    )
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY os.expiry DESC NULLS LAST, os.signal_id DESC LIMIT %s OFFSET %s"
    params.append(int(limit)); params.append(int(max(0, offset)))
    from psycopg2.extras import RealDictCursor
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]


def replace_option_signals(rows: List[Dict[str, Any]]) -> int:
    """Replace option overlay rows for their signal_ids.

    Deletes existing rows for all signal_ids present in `rows`, then inserts the provided rows.
    Returns number of rows written.
    """
    if not rows:
        return 0
    sig_ids = sorted({int(r.get('signal_id')) for r in rows if r.get('signal_id') is not None})
    cols = [
        'signal_id','occ_symbol','expiry','strike','type','delta','iv_used',
        'entry_premium_est','stop_premium_est','target_premium_est','pricing_estimate','legs_json','net_debit_credit','stop_value','target_value'
    ]
    values = [tuple(r.get(c) for c in cols) for r in rows]
    placeholders = ",".join(["(" + ",".join(["%s"] * len(cols)) + ")"] * len(values))
    sql_ins = f"INSERT INTO option_signals ({', '.join(cols)}) VALUES {placeholders}"
    flat: List[Any] = []
    for v in values:
        flat.extend(v)
    with get_db() as conn:
        with conn.cursor() as cur:
            if sig_ids:
                cur.execute("DELETE FROM option_signals WHERE signal_id = ANY(%s)", (sig_ids,))
            cur.execute(sql_ins, flat)
            conn.commit()
            return len(values)
