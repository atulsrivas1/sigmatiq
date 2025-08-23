# Workflow Authoring Template

Title: Find Oversold Stocks (5 minutes)
Subtitle: Use RSI to quickly surface oversold names on your watchlist.
Persona: beginner | day_trader | swing_trader
Difficulty: beginner
Time to complete: 5
Goal: Get a list of oversold candidates using RSI.
Prerequisites:
- API running at http://localhost:8001
- Data access for chosen tickers

Dependencies:
- Indicators: ["rsi"]
- Indicator Sets: []
- Strategies: []

Steps:
1. Describe: Choose timeframe (hourly) and threshold (RSI < 30)
   Rationale: Focuses on clean oversold signals on larger intraday bars.
   API: POST /screen { universe: ["SPY","AAPL",...], condition: { id:"rsi", params:{ period:14 }, op:"<", value:30 }, timeframe:"hourly" }
   Expects: `ok:true` and `matches` list.
2. Describe: Save the result to review
   Rationale: Keep a snapshot to compare day‑to‑day.
   API: (optional) export CSV from results.

Outputs:
- List of matches `{ symbol, ts, value }`

Best when:
- Markets are range‑bound

Avoid when:
- Major news events or very low liquidity

Caveats:
- RSI can stay oversold during strong downtrends; consider risk controls.

Media:
- cover_uri: /static/workflows/oversold_cover.png

Links:
- Indicator: /catalog/indicator/rsi

Research:
- references: [ { title: "Wilder 1978", url: "https://..." } ]

