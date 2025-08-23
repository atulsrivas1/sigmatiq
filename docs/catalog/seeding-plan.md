# Seeding Plan — From Existing Docs

Sources
- Indicators: `docs/INDICATORS_REFERENCE.md`, `docs/codex/indicators-map.md`, `docs/MODELING_REFERENCE.md`.
- Indicator Sets: `docs/indicator_sets/use-cases.md` + rationale we authored.
- Strategies: `docs/trading_strategies/use-cases.md` + `strategy-architecture.md`.
- Media: diagrams from `docs/*`; later add annotated charts.

Approach
1) Extract names, categories, params for indicators from the catalog files.
2) Author explainer text (What/How/When/Caveats) per indicator using templates.
3) Curate 8–12 set templates (components, logic, alignment, rationale).
4) Curate 6+ strategy templates (objective, rules, risk, policy, typical ranges).
5) Create minimal media assets (covers, diagrams) and link via URIs.
6) Fill research references and evidence summaries; add QA checklists.

Priorities
- Phase 1: Top 12 single indicators (RSI, MACD, ATR, BB, VWAP, Vol Z, IV Rank, Donchian, Supertrend, Stoch, Dist to EMA, VIX Level).
- Phase 2: Top 8 sets (Momentum Breakout, 0DTE Gate, Multi-TF Trend, Mean Reversion Bands, Breakout Pullback, VPA Scanner, Vol Expansion, Premium Selector).
- Phase 3: Top 6 strategies (Breakout, VWAP Reversion, Trend Following, 0DTE, Iron Condor, Wheel).

Deliverables
- JSON explainer drafts under `docs/catalog/examples/` for review before DB seeding.

