-- Seed Phase-3 per-ticker 0DTE model and a consensus pack
BEGIN;

-- sq_spy_0dte_gate_5m (per-ticker)
INSERT INTO sc.model_specs (
  model_id, version, status, title, description,
  target_kind, target_id, target_version,
  timeframe, market, instrument,
  featureset, label_cfg, thresholds, guardrails, artifacts, plan_template,
  brand, display_name, novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
  horizon, style, tags, scope, training_cfg
) VALUES (
  'sq_spy_0dte_gate_5m', 1, 'draft',
  'SPY 0DTE Gate (5m)', 'Per-ticker 0DTE event gate with cautious options proxy.',
  'indicator_set', 'zerosigma_0dte_gate', 1,
  '5m', 'US', 'option',
  '{"set_id":"zerosigma_0dte_gate","version":1}'::jsonb,
  '{"horizon_bars":12, "tp_pct":null, "sl_pct":null, "max_hold_bars":12, "options_proxy":{"type":"atm","dte_min":0,"delta":0.5}}'::jsonb,
  '{"buy_min_score":0.72, "sell_min_score":0.72, "budgets":{"hourly":3}}'::jsonb,
  '{"options":{"dte_min":0, "leverage_cap":2}, "exposure_caps":{"option_contracts_max":1}}'::jsonb,
  '{"model_uri":"s3://sigmatiq/models/sq_spy_0dte_gate_5m_v1.pkl"}'::jsonb,
  '{"max_hold_bars":12, "sizing_hint":"small"}'::jsonb,
  'sigmatiq', 'Sigmatiq SPY 0DTE Gate (5m)', TRUE,
  '0DTE gate for SPY with event awareness and conservative risk.',
  '{"operation":"preview","timeframe":"5m","cap":1}'::jsonb,
  '{"summary_tpl":"Heads up: 0DTE gate on SPY (5m).","why_tpl":"Conditions align for a cautious 0DTE idea.","how_to_check_tpl":"Confirm micro-structure stability; very small size."}'::jsonb,
  '{"0dte":"High risk; tight controls and minimal size only."}'::jsonb,
  '0dte','momentum', ARRAY['per_ticker'],
  '{"type":"per_ticker","allow_symbols":["SPY"]}'::jsonb,
  '{"data_window":{"start":"2024-03-01","end":"2024-08-01"},"session":{"hours":"RTH","timezone":"US/Eastern"},"cv":{"method":"rolling","folds":3,"gap_bars":5},"filters":{"weekdays":[1,2,3,4,5],"time":"09:30-16:00"}}'::jsonb
) ON CONFLICT (model_id, version) DO NOTHING;

-- Consensus pack: sq_consensus_trend_5m
INSERT INTO sc.model_packs (
  pack_id, version, status, title, description,
  brand, display_name,
  timeframe, market, instrument,
  horizon, style, tags, instrument_profile, suitability,
  novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
  consensus
) VALUES (
  'sq_consensus_trend_5m', 1, 'draft',
  'Consensus Trend (5m)', 'Final BUY only when multiple intraday trend models agree.',
  'sigmatiq', 'Sigmatiq Consensus Trend (5m)',
  '5m', 'US', 'equity',
  'intraday','momentum', ARRAY['consensus','cohort:liquid_etfs'], NULL, NULL,
  TRUE,
  'Combines multiple intraday models to reduce noise; BUY only on consensus.',
  '{"operation":"preview","timeframe":"5m","cap":25}'::jsonb,
  '{"summary_tpl":"Heads up: Consensus BUY on {{symbol}} (5m).","why_tpl":"Multiple models agree; trend conditions favorable.","how_to_check_tpl":"Confirm clean structure and volume alignment."}'::jsonb,
  '{"risk":"Consensus reduces but does not eliminate false signals."}'::jsonb,
  '{"policy":"majority","min_quorum":2,"buy_score":0.70,"sell_score":0.70,"tie_breaker":"hold"}'::jsonb
) ON CONFLICT (pack_id, version) DO NOTHING;

-- Components for the pack (must exist)
INSERT INTO sc.model_pack_components (pack_id, pack_version, ord, model_id, model_version, weight, required, min_score) VALUES
  ('sq_consensus_trend_5m', 1, 0, 'sq_macd_trend_pullback_5m', 1, 1.0, FALSE, 0.70),
  ('sq_consensus_trend_5m', 1, 1, 'sq_momentum_breakout_5m', 1, 1.0, FALSE, 0.70),
  ('sq_consensus_trend_5m', 1, 2, 'sq_vwap_reversion_5m', 1, 1.0, FALSE, 0.70)
ON CONFLICT DO NOTHING;

COMMIT;

