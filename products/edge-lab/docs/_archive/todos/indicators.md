Indicators & Registry

Completed
- Builtins implemented (momentum, volatility/rolling std, RSI, EMA, EMA slope, distance-to-EMA, returns, sold_flow_ratio, IV–RV spread; daily RSI/EMA/RET/dist-to-EMA; momentum_score_total).
- Registry now auto-discovers builtins and registers snake_case keys.
- Feature builder uses indicator_set to append features.
- ZeroEdge indicator set expanded to include intraday + daily + composite.

Pending
- Tag indicators with category/subcategory metadata for API browsing.
- Add additional Polygon-driven indicators from the Excel catalog (e.g., VWAP, Bollinger, MACD, ADX, IV skew/term).
