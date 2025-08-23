BEGIN;
UPDATE sc.universe_presets SET novice_ready = TRUE, beginner_summary = 'Large-cap U.S. stocks; broad market exposure. Good default universe.' WHERE preset_id = 'sp500';
UPDATE sc.universe_presets SET novice_ready = TRUE, beginner_summary = 'Top 100 NASDAQ non-financials; tech-heavy, higher volatility.' WHERE preset_id = 'nasdaq100';
UPDATE sc.universe_presets SET novice_ready = TRUE, beginner_summary = 'Blue-chip U.S. companies; very liquid, smaller list.' WHERE preset_id = 'dow30';
UPDATE sc.universe_presets SET novice_ready = TRUE, beginner_summary = 'Highly traded ETFs for quick checks and demos.' WHERE preset_id = 'liquid_etfs';
COMMIT;
