# AlgoTraderAI — Technical Indicators Catalog (Polygon‑first)

> **Generated:** 2025-08-14  
> **Primary Provider:** Polygon.io (stocks + options first)  
> **Context:** Built for AlgoTraderAI; fallbacks listed for Alpha Vantage (TA functions) and Alpaca (execution + bars).


## Table of Contents
- [Overview](#overview)
- [API Endpoint Quick Reference](#api-endpoint-quick-reference)
- [Indicators Catalog](#indicators-catalog)
- [Provider Mapping (Polygon-first)](#provider-mapping-polygon-first)
- [Notes & Caveats](#notes--caveats)

## Overview
- **Generated On:** 2025-08-14
- **Primary Provider:** Polygon.io (stocks + options first)
- **Key Notes - Polygon Indicators:** Native endpoints for SMA/EMA/RSI/MACD; compute others from aggregates.
- **Key Notes - Options:** Chain/contract snapshots include IV, greeks, OI (current); store daily snapshots for IVR/IV% time series.
- **VWAP:** Daily grouped endpoint returns vwap; for intraday/session use trades or minute aggregates.
- **Breadth Metrics:** Require grouped market bars for entire universe (heavy).
- **Alpha Vantage:** Use for many TA indicators via Technical Indicator API (fallback).
- **Alpaca:** Use for execution; compute indicators from bars; options snapshots provide greeks/IV on some plans.
- **License:** This sheet is provided as-is with no warranty.

## API Endpoint Quick Reference
Name | Endpoint | Notes
--- | --- | ---
Polygon Stocks - SMA | `/v1/indicators/sma/{stockTicker}` | native
Polygon Stocks - EMA | `/v1/indicators/ema/{stockTicker}` | native
Polygon Stocks - RSI | `/v1/indicators/rsi/{stockTicker}` | native
Polygon Stocks - MACD | `/v1/indicators/macd/{stockTicker}` | native
Polygon Stocks - Aggregates (custom bars) | `/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}` | compute base
Polygon Stocks - Grouped Daily (includes VWAP) | `/v2/aggs/grouped/locale/us/market/stocks/{date}` | daily market summary
Polygon Options - Contract Snapshot | `/v3/snapshot/options/{underlyingAsset}/{optionContract}` | IV, OI, greeks
Polygon Options - Chain Snapshot | `/v3/snapshot/options/{underlyingAsset}` | iterate chain
Polygon Options - Aggregates (custom bars) | `/v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | contract OHLCV
Polygon Indices - RSI (example) | `/v1/indicators/rsi/{indicesTicker}` | indices indicators
Polygon Indices - EMA (example) | `/v1/indicators/ema/{indicesTicker}` | indices indicators
Polygon Indices - Tickers | `/v3/reference/tickers?ticker=I:VIX` | find VIX family

## Indicators Catalog

### Breadth & Internals
Indicator | Typical Params | Inputs | Formula / Pseudocode (brief)
--- | --- | --- | ---
% Above 200-day MA | — | Market-wide aggregates | 
% Above 50-day MA | — | Market-wide aggregates | 
Advance-Decline Line (A/D) | — | Market-wide aggregates | 
Advance-Decline Ratio (ADR) | — | Market-wide aggregates | 
Arms Index (TRIN) | — | Market-wide aggregates | 
Cumulative TICK | — | Market-wide aggregates | 
McClellan Oscillator | 19/39 EMA of A-D | Market-wide aggregates | 
McClellan Summation Index | cumulative McClellan | Market-wide aggregates | 
NYSE TICK | — | Market-wide aggregates | 
New Highs - New Lows (NH-NL) | — | Market-wide aggregates | 
Upside/Downside Volume Ratio | — | Market-wide aggregates | 
Zweig Breadth Thrust | 10-day adv% | Market-wide aggregates | 

### Chart Types & Profiles
Indicator | Typical Params | Inputs | Formula / Pseudocode (brief)
--- | --- | --- | ---
Heikin Ashi (Heikin-Ashi candles) | — | OHLCV | HA_close=(O+H+L+C)/4; HA_open=(HA_open_prev+HA_close_prev)/2
Kagi | reversal amount | OHLCV | 
Point & Figure (P&F) | box size, reversal | OHLCV | 
Range Bars | tick/ATR range | OHLCV | 
Renko | box size | OHLCV | 
Volume Profile (Volume by Price) | bins/rows | OHLCV | 

### Momentum
Indicator | Typical Params | Inputs | Formula / Pseudocode (brief)
--- | --- | --- | ---
Aroon Down | n=25 | OHLCV | 
Aroon Oscillator | n=25 | OHLCV | AroonOsc = AroonUp - AroonDown
Aroon Up | n=25 | OHLCV | 
Average Directional Index (ADX) | n=14 | OHLCV | Compute +DM/-DM, +DI/-DI, then ADX = SMA(DX,n)
Average Directional Index Rating (ADXR) | n=14 | OHLCV | 
Awesome Oscillator (AO) | 5/34 | OHLCV | 
Chande Momentum Oscillator (CMO) | n=14 | OHLCV | 
Commodity Channel Index (CCI) | n=20 | OHLCV | CCI = (TP - SMA(TP,n)) / (0.015*MD)
Connors RSI (CRSI) | n=14 | OHLCV | 
Detrended Price Oscillator (DPO) | n=20 | OHLCV | DPO = price - SMA(price, n/2+1)
Elder Ray Bear Power | ema=13 | OHLCV | 
Elder Ray Bull Power | ema=13 | OHLCV | 
Fast Stochastic %K | %K=14 | OHLCV | 
Fisher Transform | n=9 | OHLCV | 
Know Sure Thing (KST) | ROCs 10/15/20/30 | OHLCV | KST = Σ ROC_i * SMA(ROC_i, w_i) with weights
MACD | fast=12, slow=26, signal=9 | OHLCV | MACD = EMA(close,12)-EMA(close,26); Signal=EMA(MACD,9); Hist=MACD-Signal
MACD Histogram | fast=12, slow=26, signal=9 | OHLCV | 
MACD Signal | fast=12, slow=26, signal=9 | OHLCV | 
Minus Directional Indicator (-DI) | n=14 | OHLCV | 
Momentum (MOM) | n=10 | OHLCV | MOM = close - close_{n}
Percentage Price Oscillator (PPO) | fast=12, slow=26, signal=9 | OHLCV | PPO = (EMA_fast-EMA_slow)/EMA_slow *100
Plus Directional Indicator (+DI) | n=14 | OHLCV | 
Qstick | n=8-20 | OHLCV | 
Rate of Change (ROC) | n=12 | OHLCV | ROC = (close/close_{n} - 1)*100
Relative Strength Index (RSI) | n=14 | OHLCV | RSI = 100 - 100/(1+RS), RS=EMA(gains)/EMA(losses)
Relative Vigor Index (RVI) | n=10 | OHLCV | 
Slow Stochastic %D | %D=3 | OHLCV | 
Stochastic %D | %D=3 | OHLCV | %D = SMA(%K,3)
Stochastic %K | %K=14 | OHLCV | %K = 100*(close-LL_n)/(HH_n-LL_n)
Stochastic RSI | n=14 | OHLCV | StochRSI = (RSI - min_n(RSI))/(max_n(RSI)-min_n(RSI))
TRIX | n=14 | OHLCV | TRIX = 100 * (EMA(EMA(EMA(close,n),n),n)_t / prev - 1)
True Strength Index (TSI) | short=13, long=25 | OHLCV | TSI = 100 * EMA(EMA(dm, r), s) / EMA(EMA(\|dm\|, r), s)
Ultimate Oscillator (ULTOSC) | 7/14/28 | OHLCV | ULTO = weighted averages of BP/TR over 7/14/28
Williams %R | n=14 | OHLCV | %R = -100*(HH_n - close)/(HH_n-LL_n)

### Options & Volatility Analytics
Indicator | Typical Params | Inputs | Formula / Pseudocode (brief)
--- | --- | --- | ---
IV Percentile (52W) | — | Options chain / snapshots | % of 52W days where IV <= IV_today
IV Rank (52W) | — | Options chain / snapshots | 100 * (IV_today - IV_min) / (IV_max - IV_min) over 52W
IV Skew (25-delta RR) | — | Options chain / snapshots | 
IV Smile (Butterfly Width) | — | Options chain / snapshots | 
IV30 (30D ATM IV) | — | Options chain / snapshots | 
Max Pain | — | Options chain / snapshots | Strike with min Σ (OI_put*\|S-Strike\| + OI_call*\|S-Strike\|)
Open Interest (per contract) | — | Options chain / snapshots | 
Option Delta | — | Options chain / snapshots | ∂OptionPrice/∂Underlying
Option Gamma | — | Options chain / snapshots | ∂²OptionPrice/∂Underlying²
Option Implied Volatility (IV) | per contract | Options chain / snapshots | Solve σ in Black-Scholes given market price
Option Theta | — | Options chain / snapshots | ∂OptionPrice/∂Time
Option Vega | — | Options chain / snapshots | ∂OptionPrice/∂Volatility
Put/Call Ratio (Open Interest) | — | Options chain / snapshots | PCR_OI = Σ OI_put / Σ OI_call
Put/Call Ratio (Volume) | — | Options chain / snapshots | PCR_Vol = Σ Vol_put / Σ Vol_call
Realized vs IV Spread (20D) | — | Options chain / snapshots | IV30 - HV20
Term Structure Slope (Front vs Back) | — | Options chain / snapshots | IV_near - IV_far (or regression slope)
Total Call Open Interest (chain) | — | Options chain / snapshots | 
Total Put Open Interest (chain) | — | Options chain / snapshots | 
VIX (S&P 500 30D IV) | — | Options chain / snapshots | 
VIX3M (S&P 500 3M IV) | — | Options chain / snapshots | 
VIX9D (S&P 500 9D IV) | — | Options chain / snapshots | 

### Statistical & Other
Indicator | Typical Params | Inputs | Formula / Pseudocode (brief)
--- | --- | --- | ---
Autocorrelation (Lag-1) | window=20 | OHLCV | corr(R_t, R_{t-1}, window)
Cumulative Return | — | OHLCV | 
Drawdown | — | OHLCV | 
Fractal Dimension (Katz/Petrosian) | window=100-500 | OHLCV | 
Hurst Exponent | window=100-500 | OHLCV | 
Kurtosis (Rolling) | window=60/252 | OHLCV | 
Linear Regression Slope | window=20 | OHLCV | slope from OLS over window n
R-squared (Trend Strength) | window=20 | OHLCV | R^2 from OLS over window n
Rolling Beta (CAPM) | window=60/252 | OHLCV | cov(Ra,Rm)/var(Rm) over window
Rolling Correlation (with Benchmark) | window=20/60/120 | OHLCV | corr(returns_asset, returns_benchmark, window)
Rolling Sharpe Ratio | window=60/252 | OHLCV | mean(R)/stdev(R) * sqrt(252)
Rolling Sortino Ratio | window=60/252 | OHLCV | mean(R)/stdev(min(R,0)) * sqrt(252)
Shannon Entropy (Returns) | window=60 | OHLCV | 
Skewness (Rolling) | window=60/252 | OHLCV | 
Z-Score of Price | window=20 | OHLCV | (price - SMA(price,n))/StDev(price,n)
Z-Score of Return | window=20 | OHLCV | 

### Trend & Overlays
Indicator | Typical Params | Inputs | Formula / Pseudocode (brief)
--- | --- | --- | ---
Anchored VWAP (AVWAP) | anchor timestamp | OHLCV | Same as VWAP but start at anchor timestamp
Arnaud Legoux Moving Average (ALMA) | n=9, offset=0.85, sigma=6 | OHLCV | ALMA = Σ w_i*price_{t-i} with gaussian weights
Bollinger %B | ma=20, sd=2 | OHLCV | %B=(price-Lower)/(Upper-Lower)
Bollinger BandWidth | ma=20, sd=2 | OHLCV | BW=(Upper-Lower)/Mid
Bollinger Bands | ma=20, sd=2 | OHLCV | Mid=SMA(n); Upper=Mid+k*σ_n; Lower=Mid-k*σ_n
Chande Kroll Stop | n1=10, n2=20, mult=1.5 | OHLCV | LongStop=HH(n1) - m*ATR(n2); ShortStop=LL(n1) + m*ATR(n2)
Donchian Channels | lookback=20 | OHLCV | Upper=max(high,n); Lower=min(low,n); Mid=(U+L)/2
Double Exponential Moving Average (DEMA) | n=12 or 26 (common cross: 12/26) | OHLCV | DEMA = 2*EMA(n) - EMA(EMA(n))
Exponential Moving Average (EMA) | n=12 or 26 (common cross: 12/26) | OHLCV | EMA_t = α*close_t + (1-α)*EMA_{t-1}; α=2/(n+1)
Fractal Adaptive Moving Average (FRAMA) | n=10-20 | OHLCV | 
Gann HiLo Activator | n=10 | OHLCV | 
Hull Moving Average (HMA) | n=9 or 20 | OHLCV | HMA_n = WMA(2*WMA(n/2) - WMA(n), sqrt(n))
Ichimoku Chikou Span | shift=-26 | OHLCV | Chikou=close shifted -26
Ichimoku Kijun-sen | period=26 | OHLCV | Kijun=(HH_26+LL_26)/2
Ichimoku Senkou Span A | tenkan=9, kijun=26, shift=26 | OHLCV | SpanA=(Tenkan+Kijun)/2 shifted +26
Ichimoku Senkou Span B | period=52, shift=26 | OHLCV | SpanB=(HH_52+LL_52)/2 shifted +26
Ichimoku Tenkan-sen | period=9 | OHLCV | Tenkan=(HH_9+LL_9)/2
Kaufman Adaptive Moving Average (KAMA) | n=10, fast=2, slow=30 | OHLCV | KAMA_t = KAMA_{t-1} + SC*(price_t - KAMA_{t-1}), SC from ER
Keltner Channels | ema=20, atr_mult=2 | OHLCV | Mid=EMA(n); Upper=Mid + m*ATR; Lower=Mid - m*ATR
Linear Regression Channel | window=20, stdev=2 | OHLCV | 
Linear Regression Line (LSMA) | n=20 (common: 5/10/20/50/100/200) | OHLCV | Slope, intercept via OLS on (t, price) over window n
Median Price (HL2) | — | OHLCV | 
Moving Average Envelope | base MA=20, offset=2% | OHLCV | 
Parabolic SAR (PSAR) | step=0.02, max=0.2 | OHLCV | Iterative: SAR_{t} = SAR_{t-1} + AF*(EP - SAR_{t-1})
Pivot Points (Camarilla) |  | OHLCV | 
Pivot Points (Fibonacci) |  | OHLCV | 
Pivot Points (Standard) | prev H/L/C | OHLCV | 
Pivot Points (Woodie) |  | OHLCV | 
Price Channels | lookback=20 | OHLCV | 
Simple Moving Average (SMA) | n=20 (common: 5/10/20/50/100/200) | OHLCV | SMA_n = mean(close[-n:])
Supertrend | atr_period=10/14, mult=3 | OHLCV | Upper=(HL2 + m*ATR); Lower=(HL2 - m*ATR); flip by trend
Triangular Moving Average (TRIMA) | n=20 | OHLCV | TRIMA = SMA(SMA(close, n), n)
Triple Exponential Moving Average (TEMA) | n=12 or 26 (common cross: 12/26) | OHLCV | TEMA = 3*EMA - 3*EMA(EMA) + EMA(EMA(EMA))
Typical Price (HLC3) | — | OHLCV | 
VWAP (Session) | session start->end | OHLCV | VWAP=Σ(price*volume)/Σ(volume) from session start
Variable Index Dynamic Average (VIDYA) | n=20, alpha=0.2 | OHLCV | 
Weighted Close (HLCC4) | — | OHLCV | 
Weighted Moving Average (WMA) | n=20 | OHLCV | WMA_n = sum(w_i*close_{t-i})/sum(w_i), w_i=i
Zero-Lag Exponential MA (ZLEMA) | n=12 or 26 (common cross: 12/26) | OHLCV | ZLEMA = EMA(price + (price - price_{lag}), n)

### Volatility
Indicator | Typical Params | Inputs | Formula / Pseudocode (brief)
--- | --- | --- | ---
Average True Range (ATR) | n=14 | OHLCV | TR = max(H-L, \|H-C_{-1}\|, \|L-C_{-1}\|); ATR=EMA(TR,n)
Chaikin Volatility | n=10 | OHLCV | 
Choppiness Index | n=14 | OHLCV | 
Garman-Klass Volatility (OHLC) | window=20 | OHLCV | σ^2 = 0.5(ln(H/L))^2 - (2ln2-1)(ln(C/O))^2
Historical Volatility (Close-to-Close) | window=20 | OHLCV | HV = stdev(ln(close/prev_close), n) * sqrt(252)
Normalized ATR (NATR) | n=14 | OHLCV | NATR = 100 * ATR / close
Parkinson Volatility (HL) | window=20 | OHLCV | σ = sqrt( (1/(4n ln2)) * Σ (ln(H/L))^2 ) * sqrt(252)
Rogers-Satchell Volatility (OHLC) | window=20 | OHLCV | σ^2 = ln(H/C)ln(H/O) + ln(L/C)ln(L/O)
Standard Deviation (StDev) | n=20 | OHLCV | σ_n = sqrt(mean((x-mean)^2))
Ulcer Index | n=14 | OHLCV | UI = sqrt( mean( drawdown_pct^2 ) )
Yang-Zhang Volatility | window=20 | OHLCV | Combination of overnight, rs, and open-close var

### Volume
Indicator | Typical Params | Inputs | Formula / Pseudocode (brief)
--- | --- | --- | ---
Accumulation/Distribution Line (ADL) | — | OHLCV | MF Multiplier=((C-L)-(H-C))/(H-L); ADL=Σ(MF*V)
Chaikin Money Flow (CMF) | n=20 | OHLCV | CMF = Σ( ( (C-L)-(H-C) )/(H-L) * V ) / Σ(V)
Chaikin Oscillator | ema fast/slow 3/10 | OHLCV | EMA(ADL,3) - EMA(ADL,10)
Ease of Movement (EOM) | n=14 | OHLCV | EOM = ((H+L)/2 - (H_{-1}+L_{-1})/2) * (H-L)/V
Klinger Volume Oscillator (KVO) | — | OHLCV | KVO = EMA(VF,34)-EMA(VF,55)
Money Flow Index (MFI) | n=14 | OHLCV | MFI = 100 - 100/(1+ PMF/NMF) on TP*V
Negative Volume Index (NVI) | — | OHLCV | 
On-Balance Volume (OBV) | — | OHLCV | OBV_t = OBV_{t-1} + sign(C_t - C_{t-1})*V_t
Positive Volume Index (PVI) | — | OHLCV | 
Price Volume Trend (PVT) | — | OHLCV | 
Volume Oscillator (VO) | fast/slow 14/28 | OHLCV | 

## Provider Mapping (Polygon-first)

### Breadth & Internals
Indicator | Asset Class | Polygon Support | Polygon Endpoint / Recipe | Polygon Notes | Alpha Vantage | Alpaca
--- | --- | --- | --- | --- | --- | ---
% Above 200-day MA | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
% Above 50-day MA | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Advance-Decline Line (A/D) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute from market-wide dataset (grouped daily across all stocks). | compute | compute
Advance-Decline Ratio (ADR) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute from market-wide dataset (grouped daily across all stocks). | compute | compute
Arms Index (TRIN) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Cumulative TICK | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
McClellan Oscillator | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
McClellan Summation Index | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
NYSE TICK | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute from market-wide dataset (grouped daily across all stocks). | compute | compute
New Highs - New Lows (NH-NL) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Upside/Downside Volume Ratio | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Zweig Breadth Thrust | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute from market-wide dataset (grouped daily across all stocks). | compute | compute

### Chart Types & Profiles
Indicator | Asset Class | Polygon Support | Polygon Endpoint / Recipe | Polygon Notes | Alpha Vantage | Alpaca
--- | --- | --- | --- | --- | --- | ---
Heikin Ashi (Heikin-Ashi candles) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Kagi | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Point & Figure (P&F) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Range Bars | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Renko | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Volume Profile (Volume by Price) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute

### Momentum
Indicator | Asset Class | Polygon Support | Polygon Endpoint / Recipe | Polygon Notes | Alpha Vantage | Alpaca
--- | --- | --- | --- | --- | --- | ---
Aroon Down | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Aroon Oscillator | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Aroon Up | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Average Directional Index (ADX) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Average Directional Index Rating (ADXR) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Awesome Oscillator (AO) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Chande Momentum Oscillator (CMO) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Commodity Channel Index (CCI) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Connors RSI (CRSI) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Detrended Price Oscillator (DPO) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Elder Ray Bear Power | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Elder Ray Bull Power | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Fast Stochastic %K | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Fisher Transform | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Know Sure Thing (KST) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
MACD | Stocks/General | native | `/v1/indicators/macd/{stockTicker}` | Polygon provides a direct endpoint for this indicator. | native | compute
MACD Histogram | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
MACD Signal | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Minus Directional Indicator (-DI) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Momentum (MOM) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Percentage Price Oscillator (PPO) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Plus Directional Indicator (+DI) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Qstick | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Rate of Change (ROC) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Relative Strength Index (RSI) | Stocks/General | native | `/v1/indicators/rsi/{stockTicker}` | Polygon provides a direct endpoint for this indicator. | native | compute
Relative Vigor Index (RVI) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Slow Stochastic %D | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Stochastic %D | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Stochastic %K | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Stochastic RSI | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
TRIX | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
True Strength Index (TSI) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Ultimate Oscillator (ULTOSC) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Williams %R | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute

### Options & Volatility Analytics
Indicator | Asset Class | Polygon Support | Polygon Endpoint / Recipe | Polygon Notes | Alpha Vantage | Alpaca
--- | --- | --- | --- | --- | --- | ---
IV Percentile (52W) | Options/Volatility | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Not provided directly; compute from historical daily ATM IV that you store. |  | compute
IV Rank (52W) | Options/Volatility | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Not provided directly; compute from historical daily ATM IV that you store. |  | compute
IV Skew (25-delta RR) | Options/Volatility | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute from full options chain snapshot across strikes/expirations. |  | compute
IV Smile (Butterfly Width) | Options/Volatility | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute from full options chain snapshot across strikes/expirations. |  | compute
IV30 (30D ATM IV) | Options/Volatility | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). |  | compute
Max Pain | Options/Volatility | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute from full options chain snapshot across strikes/expirations. |  | compute
Open Interest (per contract) | Options/Volatility | native | `/v3/snapshot/options/{underlyingAsset}/{optionContract}` | Returned in options snapshot payload (real-time/current). Historical time series requires storing snapshots. |  | trading-api (contract info)*
Option Delta | Options/Volatility | native | `/v3/snapshot/options/{underlyingAsset}/{optionContract}` | Returned in options snapshot payload (real-time/current). Historical time series requires storing snapshots. |  | snapshot
Option Gamma | Options/Volatility | native | `/v3/snapshot/options/{underlyingAsset}/{optionContract}` | Returned in options snapshot payload (real-time/current). Historical time series requires storing snapshots. |  | snapshot
Option Implied Volatility (IV) | Options/Volatility | native | `/v3/snapshot/options/{underlyingAsset}/{optionContract}` | Returned in options snapshot payload (real-time/current). Historical time series requires storing snapshots. |  | snapshot
Option Theta | Options/Volatility | native | `/v3/snapshot/options/{underlyingAsset}/{optionContract}` | Returned in options snapshot payload (real-time/current). Historical time series requires storing snapshots. |  | snapshot
Option Vega | Options/Volatility | native | `/v3/snapshot/options/{underlyingAsset}/{optionContract}` | Returned in options snapshot payload (real-time/current). Historical time series requires storing snapshots. |  | snapshot
Put/Call Ratio (Open Interest) | Options/Volatility | native | `/v3/snapshot/options/{underlyingAsset}` | Returned in options snapshot payload (real-time/current). Historical time series requires storing snapshots. |  | compute
Put/Call Ratio (Volume) | Options/Volatility | native | `/v3/snapshot/options/{underlyingAsset}` | Returned in options snapshot payload (real-time/current). Historical time series requires storing snapshots. |  | compute
Realized vs IV Spread (20D) | Options/Volatility | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). |  | compute
Term Structure Slope (Front vs Back) | Options/Volatility | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute from full options chain snapshot across strikes/expirations. |  | compute
Total Call Open Interest (chain) | Options/Volatility | native | `/v3/snapshot/options/{underlyingAsset}` | Returned in options snapshot payload (real-time/current). Historical time series requires storing snapshots. |  | compute
Total Put Open Interest (chain) | Options/Volatility | native | `/v3/snapshot/options/{underlyingAsset}` | Returned in options snapshot payload (real-time/current). Historical time series requires storing snapshots. |  | compute
VIX (S&P 500 30D IV) | Options/Volatility | native | `Indices API (e.g., ticker I:VIX)` | Fetch via Indices API. Symbol format often 'I:VIX', etc. |  | compute
VIX3M (S&P 500 3M IV) | Options/Volatility | native | `Indices API (e.g., ticker I:VIX3M)` | Fetch via Indices API. Symbol format often 'I:VIX', etc. |  | compute
VIX9D (S&P 500 9D IV) | Options/Volatility | native | `Indices API (e.g., ticker I:VIX9D)` | Fetch via Indices API. Symbol format often 'I:VIX', etc. |  | compute

### Statistical & Other
Indicator | Asset Class | Polygon Support | Polygon Endpoint / Recipe | Polygon Notes | Alpha Vantage | Alpaca
--- | --- | --- | --- | --- | --- | ---
Autocorrelation (Lag-1) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Cumulative Return | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Drawdown | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Fractal Dimension (Katz/Petrosian) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Hurst Exponent | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Kurtosis (Rolling) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Linear Regression Slope | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
R-squared (Trend Strength) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Rolling Beta (CAPM) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Rolling Correlation (with Benchmark) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Rolling Sharpe Ratio | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Rolling Sortino Ratio | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Shannon Entropy (Returns) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Skewness (Rolling) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Z-Score of Price | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Z-Score of Return | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute

### Trend & Overlays
Indicator | Asset Class | Polygon Support | Polygon Endpoint / Recipe | Polygon Notes | Alpha Vantage | Alpaca
--- | --- | --- | --- | --- | --- | ---
Anchored VWAP (AVWAP) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Arnaud Legoux Moving Average (ALMA) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Bollinger %B | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Bollinger BandWidth | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Bollinger Bands | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Chande Kroll Stop | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Donchian Channels | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Double Exponential Moving Average (DEMA) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Exponential Moving Average (EMA) | Stocks/General | native | `/v1/indicators/ema/{stockTicker}` | Polygon provides a direct endpoint for this indicator. | native | compute
Fractal Adaptive Moving Average (FRAMA) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Gann HiLo Activator | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Hull Moving Average (HMA) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Ichimoku Chikou Span | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Ichimoku Kijun-sen | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Ichimoku Senkou Span A | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Ichimoku Senkou Span B | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Ichimoku Tenkan-sen | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Kaufman Adaptive Moving Average (KAMA) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Keltner Channels | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Linear Regression Channel | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Linear Regression Line (LSMA) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Median Price (HL2) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Moving Average Envelope | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Parabolic SAR (PSAR) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Pivot Points (Camarilla) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Pivot Points (Fibonacci) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Pivot Points (Standard) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Pivot Points (Woodie) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Price Channels | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Simple Moving Average (SMA) | Stocks/General | native | `/v1/indicators/sma/{stockTicker}` | Polygon provides a direct endpoint for this indicator. | native | compute
Supertrend | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Triangular Moving Average (TRIMA) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Triple Exponential Moving Average (TEMA) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Typical Price (HLC3) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
VWAP (Session) | Stocks/General | native+compute | `Grouped Daily: /v2/aggs/grouped/locale/us/market/stocks/{date} -> vwap; Intraday: compute from trades /v3/trades/{ticker} or minute aggs` | Daily grouped endpoint returns VWAP; for intraday/session VWAP use trades or minute bars. | compute | compute
Variable Index Dynamic Average (VIDYA) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Weighted Close (HLCC4) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Weighted Moving Average (WMA) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Zero-Lag Exponential MA (ZLEMA) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute

### Volatility
Indicator | Asset Class | Polygon Support | Polygon Endpoint / Recipe | Polygon Notes | Alpha Vantage | Alpaca
--- | --- | --- | --- | --- | --- | ---
Average True Range (ATR) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Chaikin Volatility | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Choppiness Index | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Garman-Klass Volatility (OHLC) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Historical Volatility (Close-to-Close) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Normalized ATR (NATR) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Parkinson Volatility (HL) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Rogers-Satchell Volatility (OHLC) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Standard Deviation (StDev) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Ulcer Index | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Yang-Zhang Volatility | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute

### Volume
Indicator | Asset Class | Polygon Support | Polygon Endpoint / Recipe | Polygon Notes | Alpha Vantage | Alpaca
--- | --- | --- | --- | --- | --- | ---
Accumulation/Distribution Line (ADL) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Chaikin Money Flow (CMF) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Chaikin Oscillator | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Ease of Movement (EOM) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Klinger Volume Oscillator (KVO) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Money Flow Index (MFI) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Negative Volume Index (NVI) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
On-Balance Volume (OBV) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | native | compute
Positive Volume Index (PVI) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Price Volume Trend (PVT) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute
Volume Oscillator (VO) | Stocks/General | compute | `Stocks: /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to} \| Options: /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Compute locally from aggregates (OHLCV). | compute | compute

## Notes & Caveats
- **Polygon native TA**: Currently includes SMA, EMA, RSI, MACD (stocks/indices). Most other indicators are computed from **Aggregates** or **Trades**.
- **VWAP**: Daily VWAP is available from **Grouped Daily Market Summary**. Intraday/session VWAP and **Anchored VWAP** must be computed from trades or minute bars.
- **Options snapshots**: Greeks, IV, and OI are returned for the **current moment**. To build historical series (e.g., IV Rank/Percentile, OI change), persist snapshots daily.
- **Breadth metrics**: Require market‑wide aggregates (may be heavy). Consider universe scoping (e.g., S&P 500 constituents) for practicality.
- **Indices (e.g., VIX family)**: Query via Polygon **Indices API** (e.g., `I:VIX`, `I:VIX9D`, `I:VIX3M`).

