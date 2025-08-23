-- Enrich explainer templates and add assistant hints for seeded models/packs
BEGIN;

-- Helper updates encapsulated in one migration; safe if rows don't exist

-- Phase 1 models
UPDATE sc.model_specs SET
  explainer_templates = (COALESCE(explainer_templates, '{}'::jsonb) ||
    '{"summary_tpl_alt":"Potential setup on {{symbol}} ({{timeframe}})","why_tpl_alt":"Signals align; odds tilt modestly","how_to_check_tpl_alt":"Look for confirmation: structure + volume"}'::jsonb),
  assistant_hints = '{"tips":["Check liquidity (volume/spread)","Keep size small by default"],"cautions":["Avoid events unless opted in","Choppy regimes increase false signals"]}'::jsonb
WHERE model_id IN ('sq_rsi_oversold_daily','sq_macd_trend_pullback_5m','sq_keltner_break_alignment_hourly','sq_vwap_reversion_5m','sq_momentum_breakout_5m');

-- Phase 2 models
UPDATE sc.model_specs SET
  explainer_templates = (COALESCE(explainer_templates, '{}'::jsonb) ||
    '{"summary_tpl_alt":"Setup on {{symbol}} ({{timeframe}})","why_tpl_alt":"Context supports the plan","how_to_check_tpl_alt":"Confirm with trend/mean-revert cues"}'::jsonb),
  assistant_hints = '{"tips":["Prefer liquid names","Confirm with one additional signal"],"cautions":["Reduce size in high vol","Be mindful of gaps on open"]}'::jsonb
WHERE model_id IN ('sq_trend_follow_alignment_hourly','sq_mean_reversion_bands_hourly','sq_relative_strength_rotation_daily','sq_options_premium_selector_daily');

-- Phase 3 per-ticker model
UPDATE sc.model_specs SET
  explainer_templates = (COALESCE(explainer_templates, '{}'::jsonb) ||
    '{"summary_tpl_alt":"Cautious 0DTE gate on {{symbol}}","why_tpl_alt":"Micro-structure looks supportive","how_to_check_tpl_alt":"Confirm stability; very small size"}'::jsonb),
  assistant_hints = '{"tips":["Use smallest size","Avoid taking multiple overlapping entries"],"cautions":["0DTE is high risk","Respect DTE and leverage caps"]}'::jsonb
WHERE model_id = 'sq_spy_0dte_gate_5m';

-- Consensus pack
UPDATE sc.model_packs SET
  explainer_templates = (COALESCE(explainer_templates, '{}'::jsonb) ||
    '{"summary_tpl_alt":"Consensus setup on {{symbol}} ({{timeframe}})","why_tpl_alt":"Multiple models agree","how_to_check_tpl_alt":"Confirm structure + volume"}'::jsonb),
  assistant_hints = '{"tips":["Consensus reduces noise","Use pack for higher confidence"],"cautions":["Consensus is not a guarantee","Still keep size small"]}'::jsonb
WHERE pack_id = 'sq_consensus_trend_5m';

COMMIT;

