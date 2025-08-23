-- Seed explicit symbols for common presets (nasdaq100 subset, dow30 full)
BEGIN;

-- Dow 30 (full constituent tickers)
INSERT INTO sc.universe_preset_symbols (preset_id, symbol) VALUES
 ('dow30','AAPL'),('dow30','MSFT'),('dow30','AMGN'),('dow30','AXP'),('dow30','BA'),
 ('dow30','CAT'),('dow30','CRM'),('dow30','CSCO'),('dow30','CVX'),('dow30','DIS'),
 ('dow30','DOW'),('dow30','GS'),('dow30','HD'),('dow30','HON'),('dow30','IBM'),
 ('dow30','INTC'),('dow30','JNJ'),('dow30','JPM'),('dow30','KO'),('dow30','MCD'),
 ('dow30','MMM'),('dow30','MRK'),('dow30','NKE'),('dow30','PG'),('dow30','TRV'),
 ('dow30','UNH'),('dow30','V'),('dow30','VZ'),('dow30','WBA'),('dow30','WMT')
ON CONFLICT DO NOTHING;

UPDATE sc.universe_presets SET symbol_count = 30 WHERE preset_id = 'dow30';

-- NASDAQ-100 (curated core subset of highly traded names)
INSERT INTO sc.universe_preset_symbols (preset_id, symbol) VALUES
 ('nasdaq100','AAPL'),('nasdaq100','MSFT'),('nasdaq100','AMZN'),('nasdaq100','NVDA'),('nasdaq100','META'),
 ('nasdaq100','TSLA'),('nasdaq100','GOOGL'),('nasdaq100','GOOG'),('nasdaq100','AVGO'),('nasdaq100','COST'),
 ('nasdaq100','PEP'),('nasdaq100','NFLX'),('nasdaq100','AMD'),('nasdaq100','ADBE'),('nasdaq100','CSCO'),
 ('nasdaq100','TMUS'),('nasdaq100','CMCSA'),('nasdaq100','INTU'),('nasdaq100','QCOM'),('nasdaq100','TXN'),
 ('nasdaq100','AMGN'),('nasdaq100','SBUX'),('nasdaq100','PYPL'),('nasdaq100','MRVL'),('nasdaq100','ADI'),
 ('nasdaq100','GILD'),('nasdaq100','BKNG'),('nasdaq100','LRCX'),('nasdaq100','INTC'),('nasdaq100','PDD')
ON CONFLICT DO NOTHING;

-- Reflect explicit subset count for now
UPDATE sc.universe_presets SET symbol_count = (
  SELECT COUNT(*) FROM sc.universe_preset_symbols WHERE preset_id = 'nasdaq100'
) WHERE preset_id = 'nasdaq100';

COMMIT;
