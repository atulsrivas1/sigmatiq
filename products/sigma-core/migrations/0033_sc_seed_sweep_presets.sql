-- Seed frequently used sweep presets (novice-first)
BEGIN;

INSERT INTO sc.backtest_sweep_presets (preset_id, title, description, grid, guardrails, owner_user_id, visibility, tags)
VALUES
('rth_thresholds_basic', 'RTH thresholds basic',
 'Basic thresholds across regular trading hours',
 '{"thresholds_list": [[0.55, 0.6, 0.65, 0.7]], "allowed_hours_list": [[9,10,11,12,13,14,15]]}',
 '{"max_combos": 20, "min_trades": 50, "universe_cap": 50, "days_cap": 90}',
 NULL, 'public', '["novice","intraday"]'
) ON CONFLICT (preset_id) DO NOTHING;

INSERT INTO sc.backtest_sweep_presets (preset_id, title, description, grid, guardrails, owner_user_id, visibility, tags)
VALUES
('rth_top_pct_light', 'RTH top-pct light',
 'Select top bucket of confidence intraday; small grid',
 '{"top_pct_list": [0.05, 0.1, 0.15], "allowed_hours_list": [[9,10,11,12,13,14,15]]}',
 '{"max_combos": 20, "min_trades": 50, "universe_cap": 50, "days_cap": 90}',
 NULL, 'public', '["novice","intraday"]'
) ON CONFLICT (preset_id) DO NOTHING;

INSERT INTO sc.backtest_sweep_presets (preset_id, title, description, grid, guardrails, owner_user_id, visibility, tags)
VALUES
('swing_daily_thresholds', 'Swing daily thresholds',
 'Daily timeframe, moderate thresholds',
 '{"thresholds_list": [[0.55, 0.6, 0.65]], "allowed_hours_list": [[]]}',
 '{"max_combos": 20, "min_trades": 30, "universe_cap": 200, "days_cap": 365}',
 NULL, 'public', '["novice","swing"]'
) ON CONFLICT (preset_id) DO NOTHING;

INSERT INTO sc.backtest_sweep_presets (preset_id, title, description, grid, guardrails, owner_user_id, visibility, tags)
VALUES
('hourly_momentum_gate', 'Hourly thresholds with momentum gate',
 'Hourly timeframe with momentum gate sizing',
 '{"thresholds_list": [[0.55, 0.6]], "allowed_hours_list": [[9,10,11,12,13,14,15]], "size_by_conf_list": [true], "conf_cap_list": [1.0]}',
 '{"max_combos": 20, "min_trades": 50, "universe_cap": 50, "days_cap": 180}',
 NULL, 'public', '["intermediate","intraday"]'
) ON CONFLICT (preset_id) DO NOTHING;

COMMIT;

