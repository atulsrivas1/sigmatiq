-- Seed common universe presets for Simple Mode
BEGIN;

INSERT INTO sc.universe_presets (preset_id, title, description, source, version, symbol_count, symbols_uri)
VALUES
  ('sp500', 'S&P 500', 'Large-cap U.S. equities (top 500)', 'S&P Dow Jones Indices', '2024-08', 500, NULL)
ON CONFLICT (preset_id) DO NOTHING;

INSERT INTO sc.universe_presets (preset_id, title, description, source, version, symbol_count, symbols_uri)
VALUES
  ('nasdaq100', 'NASDAQ-100', 'NASDAQ top 100 non-financial companies', 'Nasdaq', '2024-08', 100, NULL)
ON CONFLICT (preset_id) DO NOTHING;

INSERT INTO sc.universe_presets (preset_id, title, description, source, version, symbol_count, symbols_uri)
VALUES
  ('dow30', 'Dow 30', 'Dow Jones Industrial Average constituents', 'Dow Jones', '2024-08', 30, NULL)
ON CONFLICT (preset_id) DO NOTHING;

INSERT INTO sc.universe_presets (preset_id, title, description, source, version, symbol_count, symbols_uri)
VALUES
  ('liquid_etfs', 'Liquid ETFs', 'Highly traded U.S. ETFs for quick testing', 'Internal curation', '2024-08', 12, NULL)
ON CONFLICT (preset_id) DO NOTHING;

-- Liquid ETFs explicit list
INSERT INTO sc.universe_preset_symbols (preset_id, symbol) VALUES
  ('liquid_etfs', 'SPY'),
  ('liquid_etfs', 'QQQ'),
  ('liquid_etfs', 'IWM'),
  ('liquid_etfs', 'DIA'),
  ('liquid_etfs', 'GLD'),
  ('liquid_etfs', 'SLV'),
  ('liquid_etfs', 'TLT'),
  ('liquid_etfs', 'HYG'),
  ('liquid_etfs', 'XLF'),
  ('liquid_etfs', 'XLK'),
  ('liquid_etfs', 'XLE'),
  ('liquid_etfs', 'XLV')
ON CONFLICT DO NOTHING;

COMMIT;
