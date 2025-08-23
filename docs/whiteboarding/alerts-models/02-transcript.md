# Whiteboarding Transcript (Condensed) — AI Models for Alerts

Context: 3 Product Owners align on requirements to use AI models to generate novice​-friendly alerts, now explicitly including buy/sell intent and position​-management guidance (stop, take​-profit, max hold), while maintaining guardrails and plain language.

PO1 (Nina, UX): North Star first — zero jargon, one​-tap value. We can show “Buy” or “Sell” style intents if they’re framed as suggested plans with safety caps and always optional. Every alert must state: what, why, how long to hold, when to exit.

PO2 (Arjun, Data/ML): On the model side, we’ll output: direction (buy/sell), conviction 0–1, suggested SL/TP in ATR/percent, max hold bars, and a quick rationale (top features). For options, we map to simple contracts (ATM or nearest) with position caps.

PO3 (Maya, Safety/GT): We need strong guardrails: per​-user alert quotas, position size caps, and explicit novice disclaimers. Defaults conservative: small size, tight loss caps, max hold short. Users can change presets but not hidden automations.

PO1: Language: “Heads up: setup suggests a potential BUY.” Then bullet: Stop: X%, Take​-profit: Y%, Max hold: Z bars/hours. Include a 2​-line why in plain English. No jargon like RSI unless used as context with a micro​-tooltip.

PO2: Training: use our curated indicator sets as inputs. Labels can be profit targets hit within max hold (hit TP before SL) for both stock and an options proxy (e.g., ATM call/put). We’ll calibrate thresholds to meet alert budgets.

PO3: Compliance posture: this is educational guidance, not advice. Add undo/mute everywhere. Exposure caps per user and per symbol. No rapid​-fire during events unless the user opts in.

PO1: For options, keep the contract picker simple: default ATM, nearest expiry with min DTE guardrail, and always show an estimated premium band.

PO2: Scoring service can call `/indicator_sets/auto_build` (or strategies) to compute last​-row features, then output plan fields. We’ll store outcomes to measure precision@K and plan hit rate (TP vs SL) for continuous calibration.

PO3: MVP scope: Top​-N alerts daily/hourly, for sp500/liquid_etfs by default. Deliver “Buy/Sell + Plan” cards with dismiss/snooze. No auto​-execution, no orders. Add `/alerts/preview`, `/alerts/subscribe`, `/alerts/feed`.

PO1: Success looks like: users understand what to do in seconds and can follow the plan or learn from it, without tweaking parameters.
