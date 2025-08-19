from __future__ import annotations
import os
import json
from datetime import date


def main():
    try:
        import psycopg2
        from psycopg2.extras import Json
    except Exception:
        raise SystemExit("psycopg2 is not installed; cannot seed DB")

    user = os.getenv('DB_USER'); password = os.getenv('DB_PASSWORD'); host = os.getenv('DB_HOST'); port = os.getenv('DB_PORT'); database = os.getenv('DB_NAME')
    missing = [k for k,v in {'DB_USER':user,'DB_PASSWORD':password,'DB_HOST':host,'DB_PORT':port,'DB_NAME':database}.items() if not v]
    if missing:
        raise SystemExit(f"Database env vars missing: {', '.join(missing)}")

    conn = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    try:
        cur = conn.cursor()
        today = date.today()
        # Seed a minimal signals row
        try:
            cur.execute(
                """
                INSERT INTO signals (date, model_id, ticker, side, entry_mode, entry_ref_px, stop_px, target_px, time_stop_minutes, rr, score_total, rank, pack_id, policy_version)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (date, model_id, ticker) DO NOTHING
                """,
                (today, 'sample_model', 'SPY', 'buy', 'next_session_open', 500.0, 495.0, 510.0, 120, 2.0, 0.75, 1, 'zerosigma', 'v1'),
            )
            conn.commit()
            print("Seeded signals: 1")
        except Exception as e:
            print(f"WARN: signals seed failed: {e}")
            conn.rollback()

        # Fetch id for option_signals seed (if any)
        signal_id = None
        try:
            cur.execute("SELECT id FROM signals WHERE model_id=%s AND ticker=%s ORDER BY id DESC LIMIT 1", ('sample_model','SPY'))
            row = cur.fetchone()
            if row:
                signal_id = int(row[0])
        except Exception:
            pass
        # Seed option_signals row
        if signal_id is not None:
            try:
                cur.execute(
                    """
                    INSERT INTO option_signals (signal_id, occ_symbol, expiry, strike, type, delta, iv_used, entry_premium_est, stop_premium_est, target_premium_est, pricing_estimate)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (signal_id, 'O:SPY250101C00500000', today.replace(month=12, day=31), 500.0, 'call', 0.35, 0.20, 5.0, 3.0, 8.0, True),
                )
                conn.commit()
                print("Seeded option_signals: 1")
            except Exception as e:
                print(f"WARN: option_signals seed failed: {e}")
                conn.rollback()

        # Seed a minimal backtest_run
        try:
            params = {'csv': 'matrices/sample_model/training_matrix_built.csv'}
            metrics = {'best_sharpe_hourly': 1.23, 'best_cum_ret': 0.45}
            cur.execute(
                """
                INSERT INTO backtest_runs (pack_id, model_id, params, metrics)
                VALUES (%s,%s,%s,%s)
                """,
                ('zerosigma','sample_model', Json(params), Json(metrics)),
            )
            conn.commit()
            print("Seeded backtest_runs: 1")
        except Exception as e:
            print(f"WARN: backtest_runs seed failed: {e}")
            conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    main()

