from __future__ import annotations
from typing import Optional, Dict, Any
from psycopg2.extras import RealDictCursor

from sigma_core.services.io import PACKS_DIR
from sigma_core.storage.relational import get_db


def _latest_policy_version(cur, pack_id: str, model_id: str) -> Optional[int]:
    cur.execute(
        "SELECT MAX(version) AS v FROM policies WHERE pack_id=%s AND model_id=%s",
        (pack_id, model_id),
    )
    row = cur.fetchone()
    return int(row['v']) if row and row.get('v') is not None else None


def get_policy_db(pack_id: str, model_id: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT policy FROM policies
                WHERE pack_id=%s AND model_id=%s
                ORDER BY version DESC
                LIMIT 1
                """,
                (pack_id, model_id),
            )
            row = cur.fetchone()
            return row['policy'] if row else None


def upsert_policy_db(pack_id: str, model_id: str, policy: Dict[str, Any], bump_version: bool = True) -> Dict[str, Any]:
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            v = _latest_policy_version(cur, pack_id, model_id)
            new_v = (v + 1) if (v is not None and bump_version) else (v or 1)
            if (v is not None) and (not bump_version):
                cur.execute(
                    "UPDATE policies SET policy=%s WHERE pack_id=%s AND model_id=%s AND version=%s",
                    (policy, pack_id, model_id, v),
                )
            else:
                cur.execute(
                    "INSERT INTO policies (pack_id, model_id, version, policy) VALUES (%s,%s,%s,%s)",
                    (pack_id, model_id, new_v, policy),
                )
        conn.commit()
    return {"ok": True, "version": new_v}


def get_model_config_db(pack_id: str, model_id: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT config FROM model_configs WHERE pack_id=%s AND model_id=%s",
                (pack_id, model_id),
            )
            row = cur.fetchone()
            return row['config'] if row else None


def upsert_model_config_db(pack_id: str, model_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO model_configs (pack_id, model_id, config)
                VALUES (%s,%s,%s)
                ON CONFLICT (pack_id, model_id)
                DO UPDATE SET config=EXCLUDED.config, updated_at=now()
                """,
                (pack_id, model_id, config),
            )
        conn.commit()
    return {"ok": True}


def list_models_db(pack_id: Optional[str] = None) -> list[Dict[str, Any]]:
    q = "SELECT pack_id, model_id FROM model_configs"
    args: tuple = ()
    if pack_id:
        q += " WHERE pack_id=%s"
        args = (pack_id,)
    q += " ORDER BY pack_id, model_id"
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(q, args)
            rows = cur.fetchall()
    return [{"id": r["model_id"], "pack_id": r["pack_id"]} for r in rows]


# --- Indicator sets (pack or model scope) ---

def upsert_indicator_set_db(
    pack_id: str,
    scope: str,
    *,
    model_id: Optional[str] = None,
    name: Optional[str] = None,
    data: Dict[str, Any],
    version: int = 1,
) -> Dict[str, Any]:
    scope = (scope or 'pack').lower()
    if scope not in {'pack', 'model'}:
        raise ValueError('scope must be pack or model')
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO indicator_sets (pack_id, scope, model_id, name, data, version) VALUES (%s,%s,%s,%s,%s,%s)",
                (pack_id, scope, (model_id if scope == 'model' else None), (name if scope == 'pack' else None), data, int(version)),
            )
        conn.commit()
    return {"ok": True}


def get_indicator_set_model_db(pack_id: str, model_id: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT data FROM indicator_sets
                WHERE pack_id=%s AND scope='model' AND model_id=%s
                ORDER BY id DESC
                LIMIT 1
                """,
                (pack_id, model_id),
            )
            row = cur.fetchone()
            return row['data'] if row else None


def get_indicator_set_pack_db(pack_id: str, name: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT data FROM indicator_sets
                WHERE pack_id=%s AND scope='pack' AND name=%s
                ORDER BY id DESC
                LIMIT 1
                """,
                (pack_id, name),
            )
            row = cur.fetchone()
            return row['data'] if row else None
