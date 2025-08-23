# Trading Strategies — Research Package

Scope
- Research and specifications for end-to-end trading strategies that include entry/exit logic, risk management, position sizing, execution policy, and deployment. Strategies may consume indicator sets but focus here is the full strategy lifecycle.

Contents
- `use-cases.md` — 12+ concrete strategy archetypes with personas, data, latency, and outputs.
- `use-case-matrix.md` — summary matrix for prioritization.
- `strategy-architecture.md` — components: signals → policy → sizing → orders → PnL.
- `technical-requirements.md` — rules engine, position/risk model, TX costs, metrics, WFA.
- `strategy-api-spec.md` — CRUD, backtest, walk-forward, optimize, deploy, live status.
- `performance-analysis.md` — compute and data costs for backtests/live.
- `priority-matrix.md` — phased rollout plan and decision gates.
- `feature-specs.md` — top 5 features with acceptance criteria and designs.
- `interaction-transcript.md` — Engineer A/B whiteboard + critique on strategies.
- `competitive-analysis.md` (optional) — platform comparison for strategy lifecycle.
- `cost-model.md` (optional) — cost envelope for backtest/live execution.

Notes
- Indicators and indicator sets are documented separately; strategies reference them via policies and rules but this package focuses on orchestration and lifecycle.

