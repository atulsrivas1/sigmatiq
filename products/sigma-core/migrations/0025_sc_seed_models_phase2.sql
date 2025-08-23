-- Seed Phase-2 models (broaden coverage)
BEGIN;

-- 1) sq_trend_follow_alignment_hourly
INSERT INTO sc.model_specs (
  model_id, version, status, title, description,
  target_kind, target_id, target_version,
  timeframe, market, instrument,
  featureset, label_cfg, thresholds, guardrails, artifacts, plan_template,
  brand, display_name, novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
  horizon, style, tags, scope, training_cfg
) VALUES (
  'sq_trend_follow_alignment_hourly', 1, 'draft',
  'Trend Follow Alignment (Hourly)', 'Hourly trend-follow alignment across signals; conservative exits.',
  'strategy', 'trend_follow_alignment', 1,
  'hour', 'US', 'equity',
  '{"strategy_id":"trend_follow_alignment","strategy_version":1}'::jsonb,
  '{"horizon_bars":24, "tp_pct":1.5, "sl_pct":0.75, "max_hold_bars":24}'::jsonb,
  '{"buy_min_score":0.7, "sell_min_score":0.7, "budgets":{"daily":5}, "diversity":{"per_symbol_cooldown_bars":12}}'::jsonb,
  '{"exposure_caps":{"equity_notional_pct":3}}'::jsonb,
  '{"model_uri":"s3://sigmatiq/models/sq_trend_follow_alignment_hourly_v1.pkl"}'::jsonb,
  '{"stop_atr":1.0, "tp_atr":1.6, "max_hold_bars":24, "sizing_hint":"small"}'::jsonb,
  'sigmatiq', 'Sigmatiq Trend Follow Alignment (Hourly)', TRUE,
  'Follows hourly trend when key signals align; avoids chop with conservative sizing.',
  '{"operation":"preview","timeframe":"hour","cap":50}'::jsonb,
  '{"summary_tpl":"Heads up: Trend alignment on {{symbol}} (hourly).","why_tpl":"Multiple trend signals align.","how_to_check_tpl":"Confirm EMA alignment and sustained strength."}'::jsonb,
  '{"chop":"Reduce size in high-vol regimes to avoid whipsaws."}'::jsonb,
  'swing','trend_follow', ARRAY['cohort:sp500'],
  '{"type":"cohort","allow_presets":["sp500"]}'::jsonb,
  '{"data_window":{"start":"2023-06-01","end":"2024-08-01"},"session":{"hours":"RTH","timezone":"US/Eastern"},"cv":{"method":"rolling","folds":5,"gap_bars":5},"filters":{"weekdays":[1,2,3,4,5],"time":"09:30-16:00"},"cohort_filter":{"presets":["sp500"]}}'::jsonb
) ON CONFLICT (model_id, version) DO NOTHING;

-- 2) sq_mean_reversion_bands_hourly
INSERT INTO sc.model_specs (
  model_id, version, status, title, description,
  target_kind, target_id, target_version,
  timeframe, market, instrument,
  featureset, label_cfg, thresholds, guardrails, artifacts, plan_template,
  brand, display_name, novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
  horizon, style, tags, scope, training_cfg
) VALUES (
  'sq_mean_reversion_bands_hourly', 1, 'draft',
  'Mean Reversion Bands (Hourly)', 'Hourly reversion from band extremes with EMA context.',
  'indicator_set', 'mean_reversion_bands_v1', 1,
  'hour', 'US', 'equity',
  '{"set_id":"mean_reversion_bands_v1","version":1}'::jsonb,
  '{"horizon_bars":24, "tp_pct":1.0, "sl_pct":0.5, "max_hold_bars":24}'::jsonb,
  '{"buy_min_score":0.7, "sell_min_score":0.7, "budgets":{"daily":5}, "diversity":{"per_symbol_cooldown_bars":12}}'::jsonb,
  '{"exposure_caps":{"equity_notional_pct":3}}'::jsonb,
  '{"model_uri":"s3://sigmatiq/models/sq_mean_reversion_bands_hourly_v1.pkl"}'::jsonb,
  '{"stop_atr":1.0, "tp_atr":1.4, "max_hold_bars":24, "sizing_hint":"small"}'::jsonb,
  'sigmatiq', 'Sigmatiq Mean Reversion Bands (Hourly)', TRUE,
  'Fades band extremes with context; aims for quick mean reversion.',
  '{"operation":"preview","timeframe":"hour","cap":50}'::jsonb,
  '{"summary_tpl":"Heads up: Band reversion on {{symbol}} (hourly).","why_tpl":"Price stretched to bands; EMA context supports fade.","how_to_check_tpl":"Confirm pause/turn at band edges."}'::jsonb,
  '{"gap":"Beware of gaps; avoid low-liquidity names."}'::jsonb,
  'swing','mean_reversion', ARRAY['cohort:sp500'],
  '{"type":"cohort","allow_presets":["sp500"]}'::jsonb,
  '{"data_window":{"start":"2023-06-01","end":"2024-08-01"},"session":{"hours":"RTH","timezone":"US/Eastern"},"cv":{"method":"rolling","folds":5,"gap_bars":5},"filters":{"weekdays":[1,2,3,4,5],"time":"09:30-16:00"},"cohort_filter":{"presets":["sp500"]}}'::jsonb
) ON CONFLICT (model_id, version) DO NOTHING;

-- 3) sq_relative_strength_rotation_daily
INSERT INTO sc.model_specs (
  model_id, version, status, title, description,
  target_kind, target_id, target_version,
  timeframe, market, instrument,
  featureset, label_cfg, thresholds, guardrails, artifacts, plan_template,
  brand, display_name, novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
  horizon, style, tags, scope, training_cfg
) VALUES (
  'sq_relative_strength_rotation_daily', 1, 'draft',
  'Relative Strength Rotation (Daily)', 'Daily rotation toward high relative strength vs SPY with breadth filter.',
  'indicator_set', 'relative_strength_rotation_v1', 1,
  'day', 'US', 'equity',
  '{"set_id":"relative_strength_rotation_v1","version":1}'::jsonb,
  '{"horizon_bars":20, "tp_pct":3.0, "sl_pct":1.5, "max_hold_bars":20}'::jsonb,
  '{"buy_min_score":0.7, "sell_min_score":0.7, "budgets":{"daily":5}}'::jsonb,
  '{"exposure_caps":{"equity_notional_pct":5}}'::jsonb,
  '{"model_uri":"s3://sigmatiq/models/sq_relative_strength_rotation_daily_v1.pkl"}'::jsonb,
  '{"stop_atr":1.2, "tp_atr":1.8, "max_hold_bars":20, "sizing_hint":"small"}'::jsonb,
  'sigmatiq', 'Sigmatiq Relative Strength Rotation (Daily)', TRUE,
  'Rotates into stronger names vs SPY with breadth confirmation.',
  '{"operation":"preview","timeframe":"day","cap":50}'::jsonb,
  '{"summary_tpl":"Heads up: Strong relative momentum on {{symbol}} (daily).","why_tpl":"Outperforming SPY; breadth supportive.","how_to_check_tpl":"Confirm sustained RS and trend alignment."}'::jsonb,
  '{"regime":"Trendless markets reduce edge; watch breadth."}'::jsonb,
  'position','momentum', ARRAY['cohort:sp500'],
  '{"type":"cohort","allow_presets":["sp500"]}'::jsonb,
  '{"data_window":{"start":"2023-01-01","end":"2024-08-01"},"session":{"hours":"RTH","timezone":"US/Eastern"},"cv":{"method":"rolling","folds":5,"gap_bars":5},"filters":{"weekdays":[1,2,3,4,5],"time":"09:30-16:00"},"cohort_filter":{"presets":["sp500"]},"adjusted_daily":true}'::jsonb
) ON CONFLICT (model_id, version) DO NOTHING;

-- 4) sq_options_premium_selector_daily (options proxy)
INSERT INTO sc.model_specs (
  model_id, version, status, title, description,
  target_kind, target_id, target_version,
  timeframe, market, instrument,
  featureset, label_cfg, thresholds, guardrails, artifacts, plan_template,
  brand, display_name, novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
  horizon, style, tags, scope, training_cfg
) VALUES (
  'sq_options_premium_selector_daily', 1, 'draft',
  'Options Premium Selector (Daily)', 'Daily option premium selection using IV context; conservative sizing.',
  'indicator_set', 'options_premium_selector_v1', 1,
  'day', 'US', 'option',
  '{"set_id":"options_premium_selector_v1","version":1}'::jsonb,
  '{"horizon_bars":5, "tp_pct":null, "sl_pct":null, "max_hold_bars":5, "options_proxy":{"type":"atm","dte_min":7,"delta":0.5}}'::jsonb,
  '{"buy_min_score":0.7, "sell_min_score":0.7, "budgets":{"daily":5}}'::jsonb,
  '{"exposure_caps":{"option_contracts_max":1}, "options":{"dte_min":7, "leverage_cap":3}}'::jsonb,
  '{"model_uri":"s3://sigmatiq/models/sq_options_premium_selector_daily_v1.pkl"}'::jsonb,
  '{"max_hold_bars":5, "sizing_hint":"small"}'::jsonb,
  'sigmatiq', 'Sigmatiq Options Premium Selector (Daily)', TRUE,
  'Uses IV context to pick conservative premium exposures with low size.',
  '{"operation":"preview","timeframe":"day","cap":50}'::jsonb,
  '{"summary_tpl":"Heads up: Options premium setup on {{symbol}} (daily).","why_tpl":"IV context and trend support a small premium idea.","how_to_check_tpl":"Confirm IV/price alignment; small size only."}'::jsonb,
  '{"options":"Respect min DTE and leverage caps; do not oversize."}'::jsonb,
  'position','volatility', ARRAY['cohort:liquid_etfs'],
  '{"type":"cohort","allow_presets":["liquid_etfs"]}'::jsonb,
  '{"data_window":{"start":"2023-01-01","end":"2024-08-01"},"session":{"hours":"RTH","timezone":"US/Eastern"},"cv":{"method":"rolling","folds":3,"gap_bars":5},"filters":{"weekdays":[1,2,3,4,5],"time":"09:30-16:00"},"cohort_filter":{"presets":["liquid_etfs"]},"adjusted_daily":true}'::jsonb
) ON CONFLICT (model_id, version) DO NOTHING;

COMMIT;

