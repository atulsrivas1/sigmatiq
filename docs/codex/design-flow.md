# Sigma Suite — Beginner Flow (Packs → Model → Sweep → Backtest → Leaderboard → Train)

## Overview
- Goal: a simple, linear journey for non‑technical, non‑market users.
- Starting point: Strategy Packs (e.g., zerosigma, swingsigma, gapsigma, gammasigma) act as starter kits with pre‑selected indicators and risk defaults.
- Outcome: user tweaks a couple of sliders, runs a quick test, sees traffic‑light results, compares models on a board, and trains when ready.
- Color cues: teal = success, golden = warning, red = fail.

## Flow Diagram
```
[1] Pick a Strategy Pack
          │
          ▼
[2] Create a Model (name, horizon, cadence, risk)
          │
          ▼
[3] Configure a Sweep (thresholds, hours, top %)
          │
          ▼
[4] Run Backtest (traffic‑light results)
          │
          ▼
[5] Leaderboard (rank & compare, badges)
          │
          ▼
[6] Train (lock config, show progress)
```

## Step‑by‑Step

### 1) Pick a Strategy Pack
- Inputs:
  - Pack: choose one (zerosigma, swingsigma, gapsigma, gammasigma)
  - Risk profile: Conservative / Balanced / Aggressive (uses pack defaults)
- Outputs:
  - Pack summary: what it’s good for; default indicators; default risk
  - Status badge: Ready to create
- Simple labels: Pick a Pack, Risk Level, Ready to Create

### 2) Create a Model
- Inputs:
  - Model name (auto‑suggested from ticker + horizon)
  - Ticker (e.g., SPY)
  - Horizon (e.g., 0DTE, Intraday, Swing)
  - Cadence (e.g., Hourly)
  - Risk profile (pre‑filled from step 1; editable)
- Outputs:
  - Model card (empty metrics placeholders: Score, Trades, Risk)
  - Badge: Draft
- Simple labels: Name, Ticker, Horizon, Cadence, Risk, Draft

### 3) Configure a Sweep
- Inputs (Beginner view = sliders + chips):
  - Score threshold(s): 0.50 → 0.75 (slider; defaults from pack)
  - Allowed hours: 9–16 (chips; default is typical market hours)
  - Top % select: 1% → 10% (slider; optional)
  - Advanced (collapsed): YAML view for power users
- Outputs:
  - Summary pill: “3 variants × 1 hour set”
  - Badge: Ready to Run
- Simple labels: Score Threshold, Hours, Top %, Ready to Run

### 4) Run Backtest
- Inputs:
  - Click Run Test
- Outputs (simple, color‑coded):
  - Pass/Fail: teal = pass, red = fail, golden = borderline
  - Win rate (%), Sharpe (score), Return (%), Trades (#)
  - Notes: any data quality warnings
- Simple labels: Pass/Fail, Win Rate, Score, Return, Trades

### 5) Leaderboard
- Inputs:
  - None (auto‑populates from backtests). Optional filters: Pack, Ticker, Tag
- Outputs:
  - Ranked cards: Score (Sharpe), Return, Trades, Risk badge
  - Badges: teal = Good, golden = Warning, red = Needs Work
  - Quick actions: Open, Compare, Train
- Simple labels: Best Score, Compare, Train

### 6) Train
- Inputs:
  - Click Train when satisfied
- Outputs:
  - Training progress: spinner → teal “Trained” badge
  - Model status: Ready for use
- Simple labels: Training, In Progress, Trained, Ready

## User Story
As a non‑technical trader, I pick a Pack, choose a risk level, and name my Model. I tweak one slider for the score threshold and select market hours. I run a quick test and see traffic‑light results: teal for good, golden for borderline, red for needs work. I compare my models on a simple board and, when satisfied, I click Train. The system locks the config, shows a progress badge, and marks my model as Ready.

## Tips (Onboarding + UI)
- Quick actions: surface “Run Test”, “Compare”, and “Train” as one‑click buttons on cards.
- Docs: keep a “?” help icon linking to Start Here and Pipeline Runbook.
- Guidance: show micro‑copy under sliders (e.g., “Higher threshold = fewer but stronger signals”).
- Simplify menus: keep only one sidebar menu expanded at a time.
- Defaults: pre‑fill Pack and Risk profile; the user can change later.
- Badges: use teal/golden/red consistently across cards, lists, and detail pages.

## Appendix (Modules → Steps)
- Strategy Pack registry → Step 1 (Pick a Pack)
- Model create → Step 2 (Create a Model)
- Sweep config → Step 3 (Configure a Sweep)
- Backtest → Step 4 (Run Backtest)
- Leaderboard → Step 5 (Leaderboard)
- Training → Step 6 (Train)

