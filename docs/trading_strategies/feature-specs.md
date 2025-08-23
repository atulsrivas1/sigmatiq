# Feature Specs — Top 5 Strategy Features

Format
- User Story, Acceptance Criteria, Technical Design, Dependencies, Effort

1) Strategy Templates Library
- Story: As a user, I can create a strategy from curated templates (breakout, mean-reversion, trend, 0DTE, wheel).
- Acceptance: Browse/search templates; preview rules/policy; instantiate with defaults.
- Technical: Templates with YAML/JSON; render explainer; copy-on-create.
- Deps: Registry of indicator sets, policy presets.
- Effort: 2 sprints

2) Backtest Engine v1 (Event-Driven)
- Story: As a user, I can backtest strategies with realistic fills and TX costs.
- Acceptance: Configurable slippage, commissions; plots and trade logs; CV folds.
- Technical: Event-driven sim; order/fill model; artifacts.
- Deps: Market data adapters; artifacts store.
- Effort: 4–6 sprints

3) Walk-Forward Analysis
- Story: As a user, I can run WFA to validate robustness across time splits.
- Acceptance: Define windows; retrain/retune per window; aggregate metrics.
- Technical: Orchestrate sequential backtests; lineage per window.
- Deps: Backtest engine
- Effort: 3 sprints

4) Risk Profiles Integration
- Story: As a user, I select a risk profile to automatically adjust sizing and stops.
- Acceptance: Profiles (Conservative/Balanced/Aggressive); explain changes; audit.
- Technical: Policy transforms; param injection; lineage.
- Deps: Policy/risk modules
- Effort: 2 sprints

5) Deploy to Live (Paper/Live)
- Story: As a user, I can deploy a backtested strategy to paper/live with monitoring.
- Acceptance: Venue selection; capital; start/stop/pause; live status; alerts.
- Technical: Strategy runner; broker adapters; health checks.
- Deps: Order manager; monitoring stack
- Effort: 4–6 sprints

