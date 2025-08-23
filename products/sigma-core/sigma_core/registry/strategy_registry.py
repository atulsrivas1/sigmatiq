from typing import List, Optional
from psycopg2.extras import RealDictCursor
from sigma_core.storage.relational import get_db
from sigma_core.registry.artifacts import StrategyVersion


class StrategyRegistry:
    def create_strategy(
        self,
        *,
        strategy_id: str,
        version: int,
        title: str,
        objective: Optional[str] = None,
        status: str = 'published',
        risk: Optional[dict] = None,
        execution_policy: Optional[dict] = None,
        pre_reqs: Optional[dict] = None,
        performance_snapshot: Optional[dict] = None,
        caveats: Optional[str] = None,
        compliance_note: Optional[str] = None,
        how_to_evaluate: Optional[dict] = None,
        novice_ready: bool = False,
        beginner_summary: Optional[str] = None,
        simple_defaults: Optional[dict] = None,
        guardrails: Optional[dict] = None,
    ) -> StrategyVersion:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    (
                        "INSERT INTO sc.strategies (strategy_id, version, status, title, objective, risk, execution_policy, pre_reqs, performance_snapshot, caveats, compliance_note, how_to_evaluate, novice_ready, beginner_summary, simple_defaults, guardrails) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                        "ON CONFLICT (strategy_id, version) DO UPDATE SET title=EXCLUDED.title RETURNING strategy_id, version, status, title, objective, created_at, updated_at"
                    ),
                    (
                        strategy_id,
                        int(version),
                        status,
                        title,
                        objective,
                        risk,
                        execution_policy,
                        pre_reqs,
                        performance_snapshot,
                        caveats,
                        compliance_note,
                        how_to_evaluate,
                        novice_ready,
                        beginner_summary,
                        simple_defaults,
                        guardrails,
                    ),
                )
                row = cur.fetchone()
                conn.commit()
                return StrategyVersion(**row)

    def get_strategy(self, strategy_id: str, version: int) -> Optional[StrategyVersion]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT strategy_id, version, status, title, objective, created_at, updated_at FROM sc.strategies WHERE strategy_id = %s AND version = %s",
                    (strategy_id, int(version)),
                )
                row = cur.fetchone()
                return StrategyVersion(**row) if row else None

    def list_strategies(self) -> List[StrategyVersion]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT strategy_id, version, status, title, objective, created_at, updated_at FROM sc.strategies ORDER BY strategy_id, version"
                )
                return [StrategyVersion(**r) for r in cur.fetchall()]

    def link_indicator_set(self, *, strategy_id: str, strategy_version: int, set_id: str, set_version: int) -> None:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO sc.strategy_indicator_sets (strategy_id, strategy_version, set_id, set_version) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    (strategy_id, int(strategy_version), set_id, int(set_version)),
                )
                conn.commit()
