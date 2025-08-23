-- Seed initial cohort models (Phase 1)
BEGIN;

-- 1) sq_rsi_oversold_daily
INSERT INTO sc.model_specs (
  model_id, version, status, title, description,
  target_kind, target_id, target_version,
  timeframe, market, instrument,
  featureset, label_cfg, thresholds, guardrails, artifacts, plan_template,
  brand, display_name, novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
  horizon, style, tags, scope, training_cfg
) VALUES (
  'sq_rsi_oversold_daily', 1, 'draft',
  'RSI Oversold (Daily)', 'Daily BUY/SELL based on RSI/Stoch confluence with conservative plan.',
  'indicator_set', 'rsi_stoch_confluence_v1', 1,
  'day', 'US', 'equity',
  '{"set_id":"rsi_stoch_confluence_v1","version":1}'::jsonb,
  '{"horizon_bars":5, "tp_pct":2.0, "sl_pct":1.0, "max_hold_bars":5}'::jsonb,
  '{"buy_min_score":0.7, "sell_min_score":0.7, "budgets":{"daily":5}, "diversity":{"per_symbol_cooldown_bars":10}}'::jsonb,
  '{"exposure_caps":{"equity_notional_pct":5}}'::jsonb,
  '{"model_uri":"s3://sigmatiq/models/sq_rsi_oversold_daily_v1.pkl"}'::jsonb,
  '{"stop_atr":1.0, "tp_atr":1.5, "max_hold_bars":5, "sizing_hint":"small"}'::jsonb,
  'sigmatiq', 'Sigmatiq RSI Oversold (Daily)', TRUE,
  'Looks for oversold conditions with RSI/Stoch; exits quickly with tight stop and modest target.',
  '{"operation":"preview","timeframe":"day","cap":50}'::jsonb,
  '{"summary_tpl":"Heads up: Oversold setup on {{symbol}} (daily).","why_tpl":"RSI/Stoch show oversold; bounce odds higher.","how_to_check_tpl":"Confirm with price stabilizing and small green bars."}'::jsonb,
  '{"high_vol":"In choppy regimes, signals can whipsaw; use smaller size."}'::jsonb,
  'position','mean_reversion', ARRAY['cohort:sp500'],
  '{"type":"cohort","allow_presets":["sp500"]}'::jsonb,
  '{"data_window":{"start":"2023-01-01","end":"2024-08-01"},"session":{"hours":"RTH","timezone":"US/Eastern"},"cv":{"method":"rolling","folds":5,"gap_bars":5},"filters":{"weekdays":[1,2,3,4,5],"time":"09:30-16:00","min_dollar_vol":1000000},"cohort_filter":{"presets":["sp500"]},"adjusted_daily":true}'::jsonb
) ON CONFLICT (model_id, version) DO NOTHING;

-- 2) sq_macd_trend_pullback_5m
INSERT INTO sc.model_specs (
  model_id, version, status, title, description,
  target_kind, target_id, target_version,
  timeframe, market, instrument,
  featureset, label_cfg, thresholds, guardrails, artifacts, plan_template,
  brand, display_name, novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
  horizon, style, tags, scope, training_cfg
) VALUES (
  'sq_macd_trend_pullback_5m', 1, 'draft',
  'MACD Trend Pullback (5m)', 'Intraday BUY/SELL with MACD trend + pullback pattern.',
  'indicator_set', 'macd_trend_pullback_v1', 1,
  '5m', 'US', 'equity',
  '{"set_id":"macd_trend_pullback_v1","version":1}'::jsonb,
  '{"horizon_bars":12, "tp_pct":1.0, "sl_pct":0.5, "max_hold_bars":12}'::jsonb,
  '{"buy_min_score":0.7, "sell_min_score":0.7, "budgets":{"daily":0, "hourly":5}, "diversity":{"per_symbol_cooldown_bars":10}}'::jsonb,
  '{"exposure_caps":{"equity_notional_pct":2}}'::jsonb,
  '{"model_uri":"s3://sigmatiq/models/sq_macd_trend_pullback_5m_v1.pkl"}'::jsonb,
  '{"stop_atr":0.8, "tp_atr":1.2, "max_hold_bars":12, "sizing_hint":"small"}'::jsonb,
  'sigmatiq', 'Sigmatiq MACD Trend Pullback (5m)', TRUE,
  'Follows intraday trend and enters on clean pullbacks; quick exits.',
  '{"operation":"preview","timeframe":"5m","cap":25}'::jsonb,
  '{"summary_tpl":"Heads up: Trend pullback on {{symbol}} (5m).","why_tpl":"MACD trend intact; price pulling back to support.","how_to_check_tpl":"Confirm with bounce at EMA/VWAP and volume stabilization."}'::jsonb,
  '{"events":"Avoid fresh earnings/fed events unless opted in."}'::jsonb,
  'intraday','trend_follow', ARRAY['cohort:liquid_etfs'],
  '{"type":"cohort","allow_presets":["liquid_etfs"]}'::jsonb,
  '{"data_window":{"start":"2024-01-01","end":"2024-08-01"},"session":{"hours":"RTH","timezone":"US/Eastern"},"cv":{"method":"rolling","folds":5,"gap_bars":5},"filters":{"weekdays":[1,2,3,4,5],"time":"09:30-16:00"},"cohort_filter":{"presets":["liquid_etfs"]}}'::jsonb
) ON CONFLICT (model_id, version) DO NOTHING;

-- 3) sq_keltner_break_alignment_hourly
INSERT INTO sc.model_specs (
  model_id, version, status, title, description,
  target_kind, target_id, target_version,
  timeframe, market, instrument,
  featureset, label_cfg, thresholds, guardrails, artifacts, plan_template,
  brand, display_name, novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
  horizon, style, tags, scope, training_cfg
) VALUES (
  'sq_keltner_break_alignment_hourly', 1, 'draft',
  'Keltner Break Alignment (Hourly)', 'Hourly channel break aligned with EMA trend.',
  'indicator_set', 'keltner_channel_trend_v1', 1,
  'hour', 'US', 'equity',
  '{"set_id":"keltner_channel_trend_v1","version":1}'::jsonb,
  '{"horizon_bars":24, "tp_pct":1.5, "sl_pct":0.75, "max_hold_bars":24}'::jsonb,
  '{"buy_min_score":0.7, "sell_min_score":0.7, "budgets":{"daily":5}, "diversity":{"per_symbol_cooldown_bars":12}}'::jsonb,
  '{"exposure_caps":{"equity_notional_pct":3}}'::jsonb,
  '{"model_uri":"s3://sigmatiq/models/sq_keltner_break_alignment_hourly_v1.pkl"}'::jsonb,
  '{"stop_atr":1.0, "tp_atr":1.6, "max_hold_bars":24, "sizing_hint":"small"}'::jsonb,
  'sigmatiq', 'Sigmatiq Keltner Break Alignment (Hourly)', TRUE,
  'Looks for channel breaks aligned with trend to avoid false moves.',
  '{"operation":"preview","timeframe":"hour","cap":50}'::jsonb,
  '{"summary_tpl":"Heads up: Channel break on {{symbol}} (hourly).","why_tpl":"Price breaking Keltner channel with EMA alignment.","how_to_check_tpl":"Confirm with sustained above-channel prints."}'::jsonb,
  '{"chop":"Reduce size during high volatility to avoid whipsaws."}'::jsonb,
  'swing','breakout', ARRAY['cohort:sp500'],
  '{"type":"cohort","allow_presets":["sp500"]}'::jsonb,
  '{"data_window":{"start":"2023-06-01","end":"2024-08-01"},"session":{"hours":"RTH","timezone":"US/Eastern"},"cv":{"method":"rolling","folds":5,"gap_bars":5},"filters":{"weekdays":[1,2,3,4,5],"time":"09:30-16:00"},"cohort_filter":{"presets":["sp500"]}}'::jsonb
) ON CONFLICT (model_id, version) DO NOTHING;

-- 4) sq_vwap_reversion_5m
INSERT INTO sc.model_specs (
  model_id, version, status, title, description,
  target_kind, target_id, target_version,
  timeframe, market, instrument,
  featureset, label_cfg, thresholds, guardrails, artifacts, plan_template,
  brand, display_name, novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
  horizon, style, tags, scope, training_cfg
) VALUES (
  'sq_vwap_reversion_5m', 1, 'draft',
  'VWAP Reversion (5m)', 'Intraday mean‑reversion toward VWAP with OBV context.',
  'indicator_set', 'vwap_distance_obv_v1', 1,
  '5m', 'US', 'equity',
  '{"set_id":"vwap_distance_obv_v1","version":1}'::jsonb,
  '{"horizon_bars":12, "tp_pct":0.7, "sl_pct":0.4, "max_hold_bars":12}'::jsonb,
  '{"buy_min_score":0.7, "sell_min_score":0.7, "budgets":{"hourly":5}, "diversity":{"per_symbol_cooldown_bars":10}}'::jsonb,
  '{"exposure_caps":{"equity_notional_pct":2}}'::jsonb,
  '{"model_uri":"s3://sigmatiq/models/sq_vwap_reversion_5m_v1.pkl"}'::jsonb,
  '{"stop_atr":0.7, "tp_atr":1.1, "max_hold_bars":12, "sizing_hint":"small"}'::jsonb,
  'sigmatiq', 'Sigmatiq VWAP Reversion (5m)', TRUE,
  'Fades short‑term stretches away from VWAP with volume confirmation.',
  '{"operation":"preview","timeframe":"5m","cap":25}'::jsonb,
  '{"summary_tpl":"Heads up: VWAP reversion setup on {{symbol}} (5m).","why_tpl":"Price stretched from VWAP; OBV supports a revert.","how_to_check_tpl":"Confirm contraction toward VWAP with weakening momentum."}'::jsonb,
  '{"risk":"Avoid low‑liquidity names; prefer liquid ETFs."}'::jsonb,
  'intraday','mean_reversion', ARRAY['cohort:liquid_etfs'],
  '{"type":"cohort","allow_presets":["liquid_etfs"]}'::jsonb,
  '{"data_window":{"start":"2024-01-01","end":"2024-08-01"},"session":{"hours":"RTH","timezone":"US/Eastern"},"cv":{"method":"rolling","folds":5,"gap_bars":5},"filters":{"weekdays":[1,2,3,4,5],"time":"09:30-16:00"},"cohort_filter":{"presets":["liquid_etfs"]}}'::jsonb
) ON CONFLICT (model_id, version) DO NOTHING;

-- 5) sq_momentum_breakout_5m
INSERT INTO sc.model_specs (
  model_id, version, status, title, description,
  target_kind, target_id, target_version,
  timeframe, market, instrument,
  featureset, label_cfg, thresholds, guardrails, artifacts, plan_template,
  brand, display_name, novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
  horizon, style, tags, scope, training_cfg
) VALUES (
  'sq_momentum_breakout_5m', 1, 'draft',
  'Momentum Breakout (5m)', 'Intraday momentum breakout with volume alignment.',
  'indicator_set', 'momentum_breakout_v1', 1,
  '5m', 'US', 'equity',
  '{"set_id":"momentum_breakout_v1","version":1}'::jsonb,
  '{"horizon_bars":12, "tp_pct":1.0, "sl_pct":0.6, "max_hold_bars":12}'::jsonb,
  '{"buy_min_score":0.72, "sell_min_score":0.72, "budgets":{"hourly":5}, "diversity":{"per_symbol_cooldown_bars":10}}'::jsonb,
  '{"exposure_caps":{"equity_notional_pct":2}}'::jsonb,
  '{"model_uri":"s3://sigmatiq/models/sq_momentum_breakout_5m_v1.pkl"}'::jsonb,
  '{"stop_atr":0.8, "tp_atr":1.2, "max_hold_bars":12, "sizing_hint":"small"}'::jsonb,
  'sigmatiq', 'Sigmatiq Momentum Breakout (5m)', TRUE,
  'Finds fresh momentum surges with volume support and quick exits.',
  '{"operation":"preview","timeframe":"5m","cap":25}'::jsonb,
  '{"summary_tpl":"Heads up: Momentum breakout on {{symbol}} (5m).","why_tpl":"Break with volume above recent range.","how_to_check_tpl":"Confirm follow‑through on next few bars."}'::jsonb,
  '{"risk":"False breaks happen; keep stops tight."}'::jsonb,
  'intraday','momentum', ARRAY['cohort:liquid_etfs'],
  '{"type":"cohort","allow_presets":["liquid_etfs"]}'::jsonb,
  '{"data_window":{"start":"2024-01-01","end":"2024-08-01"},"session":{"hours":"RTH","timezone":"US/Eastern"},"cv":{"method":"rolling","folds":5,"gap_bars":5},"filters":{"weekdays":[1,2,3,4,5],"time":"09:30-16:00"},"cohort_filter":{"presets":["liquid_etfs"]}}'::jsonb
) ON CONFLICT (model_id, version) DO NOTHING;

COMMIT;

