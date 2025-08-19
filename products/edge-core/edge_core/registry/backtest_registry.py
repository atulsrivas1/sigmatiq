from __future__ import annotations
from typing import Any, Dict, List, Optional
from psycopg2.extras import RealDictCursor
from datetime import datetime

from edge_core.storage.relational import get_db


def create_backtest_run(
    *,
    pack_id: str,
    model_id: str,
    started_at: Optional[datetime],
    finished_at: Optional[datetime],
    params: Dict[str, Any],
    metrics: Dict[str, Any],
    plots_uri: Optional[str],
    data_csv_uri: Optional[str],
    git_sha: Optional[str] = None,
    best_sharpe_hourly: Optional[float] = None,
    best_cum_ret: Optional[float] = None,
    trades_total: Optional[int] = None,
    tag: Optional[str] = None,
) -> Dict[str, Any]:
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO backtest_runs (pack_id, model_id, started_at, finished_at, params, metrics, plots_uri, data_csv_uri, git_sha,
                  best_sharpe_hourly, best_cum_ret, trades_total, tag)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, pack_id, model_id, started_at, finished_at, params, metrics, plots_uri, data_csv_uri, git_sha,
                  best_sharpe_hourly, best_cum_ret, trades_total, tag, created_at
                """,
                (
                    pack_id,
                    model_id,
                    started_at,
                    finished_at,
                    params,
                    metrics,
                    plots_uri,
                    data_csv_uri,
                    git_sha,
                    best_sharpe_hourly,
                    best_cum_ret,
                    trades_total,
                    tag,
                ),
            )
            row = cur.fetchone()
            conn.commit()
            return dict(row)


def leaderboard(
    *,
    pack_id: Optional[str] = None,
    model_id: Optional[str] = None,
    limit: int = 20,
    order_by: str = "sharpe_hourly",
    offset: int = 0,
) -> List[Dict[str, Any]]:
    # Prefer normalized columns; fallback to JSON if needed
    order_expr = "COALESCE(best_sharpe_hourly, (metrics->>'best_sharpe_hourly')::float) DESC"
    if order_by == "cum_ret":
        order_expr = "COALESCE(best_cum_ret, (metrics->>'best_cum_ret')::float) DESC"
    where = []
    params: List[Any] = []
    if pack_id:
        where.append("pack_id = %s")
        params.append(pack_id)
    if model_id:
        where.append("model_id = %s")
        params.append(model_id)
    sql = "SELECT id, pack_id, model_id, started_at, finished_at, plots_uri, data_csv_uri, metrics, params, best_sharpe_hourly, best_cum_ret, trades_total, tag, created_at FROM backtest_runs"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += f" ORDER BY {order_expr}, created_at DESC LIMIT %s OFFSET %s"
    params.append(limit)
    params.append(int(max(0, offset)))
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]


def create_backtest_folds(run_id: int, folds: List[Dict[str, Any]]) -> None:
    if not folds:
        return
    with get_db() as conn:
        with conn.cursor() as cur:
            for r in folds:
                cur.execute(
                    """
                    INSERT INTO backtest_folds (run_id, fold, thr_used, cum_ret, sharpe_hourly, trades)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        run_id,
                        int(r.get("fold", 0)),
                        (float(r.get("thr")) if r.get("thr") is not None else None),
                        float(r.get("cum_ret", 0.0)),
                        float(r.get("sharpe_hourly", 0.0)),
                        int(r.get("trades", 0)),
                    ),
                )
            conn.commit()
