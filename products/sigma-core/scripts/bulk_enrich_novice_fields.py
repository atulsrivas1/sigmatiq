#!/usr/bin/env python3
"""
Bulk-enrich indicator and indicator set override JSON files with novice-first fields.

Adds, if missing:
 - indicators: novice_ready=true, beginner_summary (from subtitle or measures)
 - indicator_sets: novice_ready=true, beginner_summary (from purpose/title),
                   simple_defaults.timeframe (from reading_guide.timeframe_alignment),
                   guardrails with sensible defaults by timeframe
"""
from __future__ import annotations
import json
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[3]
IND_OVR = REPO / 'docs' / 'catalog' / 'overrides' / 'indicators'
SET_OVR = REPO / 'docs' / 'catalog' / 'overrides' / 'indicator_sets'


def pick_timeframe(tf_str: str | None) -> str | None:
    if not tf_str:
        return None
    s = tf_str.lower()
    # pick first token like 1m|5m|15m|hourly|daily
    m = re.search(r'(1m|2m|3m|5m|15m|30m|hourly|daily)', s)
    if m:
        return m.group(1)
    # fallbacks
    if 'hour' in s:
        return 'hourly'
    if 'day' in s:
        return 'daily'
    return None


def guardrails_for_timeframe(tf: str | None) -> dict:
    tf = (tf or '').lower()
    if tf in {'1m', '2m', '3m'}:
        return {'universe_cap': 50, 'throttle_per_min': 2}
    if tf in {'5m', '15m', '30m', 'hourly'}:
        return {'universe_cap': 200, 'throttle_per_min': 2}
    if tf == 'daily':
        return {'universe_cap': 500, 'throttle_per_min': 1}
    return {'universe_cap': 200, 'throttle_per_min': 1}


def shorten(text: str, max_len: int = 180) -> str:
    t = ' '.join(text.split())
    return t if len(t) <= max_len else t[: max_len - 1].rstrip() + '…'


def enrich_indicators() -> int:
    changed = 0
    if not IND_OVR.exists():
        return changed
    for fp in sorted(IND_OVR.glob('*.json')):
        try:
            data = json.loads(fp.read_text(encoding='utf-8'))
        except Exception:
            continue
        orig = json.dumps(data, sort_keys=True)

        if 'novice_ready' not in data:
            data['novice_ready'] = True

        if not data.get('beginner_summary'):
            subtitle = data.get('subtitle')
            measures = data.get('measures') or {}
            what = (measures.get('what_it_measures') or '').strip()
            how = (measures.get('how_to_read') or '').strip()
            summary = subtitle or what or how
            if not summary:
                # fallback to tags/title hint
                summary = 'Simple explanation for beginners.'
            data['beginner_summary'] = shorten(summary)

        # Ensure core measures/usage/assistant_hints
        stem = fp.stem
        measures = data.get('measures') or {}
        usage = data.get('usage') or {}
        hints = data.get('assistant_hints') or []

        def set_if_missing(obj: dict, key: str, val: str):
            if not obj.get(key):
                obj[key] = val

        mapping = {
            'atr': {
                'what': 'Average True Range — recent volatility of price moves.',
                'how': 'Rising ATR suggests expanding volatility; use for position sizing and stops.',
                'ex': ['atr(period=14) rising', 'atr(period=14) > atr(period=14).rolling(20).mean()'],
                'hints': ['Use ATR for stops/targets sizing.', 'Rising ATR implies wider expected ranges.', 'Avoid comparing ATR across tickers without normalization.'],
            },
            'ema': {
                'what': 'Exponential moving average of price to track trend.',
                'how': 'Price above EMA suggests uptrend; below suggests downtrend.',
                'ex': ['close > ema(window=20)', 'ema(window=20) slope > 0'],
                'hints': ['Use EMA as a trend filter, not an entry trigger.', 'Longer windows reduce noise but lag more.', 'Combine with momentum for entries.'],
            },
            'sma': {
                'what': 'Simple moving average of price.',
                'how': 'Price above SMA suggests bullish context; below bearish.',
                'ex': ['close > sma(window=50)'],
                'hints': ['SMA is slower than EMA.', 'Use crossovers cautiously due to lag.', 'Confirm with price structure.'],
            },
            'bollinger_bands': {
                'what': 'Moving average with upper/lower bands at N standard deviations.',
                'how': 'Touches of bands indicate extremes; width reflects volatility.',
                'ex': ['close >= bb_upper(window=20, num_std=2.0)', 'close <= bb_lower(window=20, num_std=2.0)'],
                'hints': ['Avoid chasing band breaks without context.', 'Use mid-band as first target on reversions.', 'Band width expansion often precedes breakouts.'],
            },
            'rsi': {
                'what': 'Relative Strength Index — momentum oscillator 0–100.',
                'how': 'Above 70 overbought; below 30 oversold; 50 is bias.',
                'ex': ['rsi(period=14) < 30', 'rsi(period=14) crosses up 30'],
                'hints': ['Prefer crosses back through thresholds.', 'Shift to 40/60 in strong trends.', 'Combine with trend filters.'],
            },
            'stoch_rsi': {
                'what': 'Stochastic RSI — speed of RSI changes, 0–1.',
                'how': 'Values near 0/1 mark potential exhaustion; crosses signal turns.',
                'ex': ['stoch_rsi(window=14) crosses up 0.2'],
                'hints': ['Faster but noisier than RSI.', 'Use with volatility context.', 'Prefer crosses with confluence.'],
            },
            'obv': {
                'what': 'On-Balance Volume — cumulative volume flow with price direction.',
                'how': 'Rising OBV confirms uptrends; falling confirms downtrends.',
                'ex': ['obv slope > 0'],
                'hints': ['Look for divergences vs price.', 'Confirm with volume z-scores.', 'Smooth OBV to reduce noise.'],
            },
            'cmf': {
                'what': 'Chaikin Money Flow — volume-weighted accumulation/distribution.',
                'how': 'Positive CMF suggests accumulation; negative suggests distribution.',
                'ex': ['cmf(period=20) > 0'],
                'hints': ['Use with trend filter.', 'Beware in thinly traded symbols.', 'Combine with OBV for confirmation.'],
            },
            'donchian': {
                'what': 'Channel of highest high and lowest low over a window.',
                'how': 'Breaks above/below channels suggest momentum breakout.',
                'ex': ['close > donchian_upper(window=20)'],
                'hints': ['Wait for bar closes to avoid wicks.', 'Confirm with volume or momentum.', 'Use stops below channel on breakouts.'],
            },
            'momentum': {
                'what': 'Rate of price change; positive = up momentum, negative = down.',
                'how': 'Higher values mean stronger directional push.',
                'ex': ['momentum(window=10) > 0'],
                'hints': ['Normalize or compare relatively across symbols.', 'Combine with trend filters.', 'Fade weak momentum in ranges.'],
            },
            'ppo': {
                'what': 'Percentage Price Oscillator — MACD variant normalized by price.',
                'how': 'Above signal bullish; below bearish; histogram shows strength.',
                'ex': ['ppo(12,26,9) crosses above signal'],
                'hints': ['Use with trend to avoid chop.', 'Normalize across prices.', 'Confirm with higher timeframe.'],
            },
            'psar': {
                'what': 'Parabolic SAR — trailing stop indicator.',
                'how': 'Dots below price imply uptrend; above imply downtrend.',
                'ex': ['psar flip to below price'],
                'hints': ['Works in trends, whipsaws in ranges.', 'Use as trailing stop, not entry.', 'Adjust acceleration for sensitivity.'],
            },
            'keltner': {
                'what': 'EMA-based channel using ATR as band width.',
                'how': 'Touches suggest extremes; width reflects volatility.',
                'ex': ['close >= keltner_upper(window=20,mult=2)'],
                'hints': ['Compare with Bollinger for context.', 'ATR-based width adapts to volatility.', 'Use midline as mean-revert target.'],
            },
            'vol_zscore': {
                'what': 'Volume z-score — how unusual current volume is vs recent average.',
                'how': 'Z > 2 indicates unusually high volume; Z < -2 unusually low.',
                'ex': ['vol_zscore(window=20) > 2'],
                'hints': ['Use with breakouts to confirm.', 'Debounce repeated spikes.', 'Beware in micro timeframes.'],
            },
            'intraday_vwap': {
                'what': 'Volume-weighted average price for the session.',
                'how': 'Price far above/below VWAP indicates overextension.',
                'ex': ['abs(close - vwap)/vwap > 0.005'],
                'hints': ['Reset VWAP each session.', 'Prefer liquid hours.', 'Use distance bounds to avoid chasing.'],
            },
            'close_vs_vwap': {
                'what': 'Distance of close from VWAP.',
                'how': 'Large positive/negative values show overbought/oversold vs VWAP.',
                'ex': ['close_vs_vwap(kind="pct") > 0.5%'],
                'hints': ['Normalize by VWAP.', 'Use bands to bound entries.', 'Combine with OBV/volume.'],
            },
            'iv_rank_52w': {
                'what': 'Percentile of current ATM IV vs past year (0–1).',
                'how': '> 0.8 high IV; < 0.2 low IV.',
                'ex': ['iv_rank_52w(underlying="SPY") > 0.8'],
                'hints': ['Check earnings/events.', 'Define ATM consistently.', 'Use with term slope for context.'],
            },
            'iv_percentile_52w': {
                'what': 'Percentile rank of IV vs 52-week history.',
                'how': 'Higher percentile = richer premium; lower = cheaper.',
                'ex': ['iv_percentile_52w(underlying="SPY") > 80'],
                'hints': ['Mind data provider consistency.', 'Prefer daily granularity.', 'Combine with realized vol.'],
            },
            'vix_level': {
                'what': 'CBOE VIX level — implied vol of S&P 500 options.',
                'how': 'Low VIX ~ calm markets; high VIX ~ stress/volatility.',
                'ex': ['vix_level() > 25'],
                'hints': ['Use as regime context, not entry.', 'Combine with trend bias.', 'Check term structure.'],
            },
            'vix_term_slope': {
                'what': 'Slope of VIX term structure (contango/backwardation).',
                'how': 'Positive slope (contango) is normal; negative (backwardation) is risk-off.',
                'ex': ['vix_term_slope() < 0'],
                'hints': ['Backwardation is a caution flag.', 'Pair with IV rank.', 'Daily updates suffice.'],
            },
            'open_gap_z': {
                'what': 'Opening gap size normalized by ATR.',
                'how': 'Large positive/negative gaps can change regime; caution at extremes.',
                'ex': ['abs(open_gap_z(ticker="SPY")) < 2.0'],
                'hints': ['Avoid fading extreme gaps.', 'Wait for first minutes to settle.', 'Gate entries by gap size.'],
            },
        }

        m = mapping.get(stem, None)
        if m:
            set_if_missing(measures, 'what_it_measures', m.get('what', 'Derived measure from price/volume.'))
            set_if_missing(measures, 'how_to_read', m.get('how', 'Interpret with typical thresholds per timeframe.'))
            if not usage.get('example_conditions') and m.get('ex'):
                usage['example_conditions'] = m['ex']
            if not hints and m.get('hints'):
                hints = m['hints']
        else:
            # Generic fallbacks
            set_if_missing(measures, 'what_it_measures', f"{stem.replace('_',' ').title()} derived from market data.")
            set_if_missing(measures, 'how_to_read', 'Interpret using trend/volatility context; thresholds depend on timeframe.')
            if not usage.get('example_conditions'):
                usage['example_conditions'] = [f"{stem}(...) condition"]
            if not hints:
                hints = ['Use with a trend filter.', 'Avoid thinly traded symbols.', 'Validate on your timeframe.']

        data['measures'] = measures
        data['usage'] = usage
        data['assistant_hints'] = hints

        new = json.dumps(data, sort_keys=True)
        if new != orig:
            fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            changed += 1
    return changed


def enrich_indicator_sets() -> int:
    changed = 0
    if not SET_OVR.exists():
        return changed
    for fp in sorted(SET_OVR.glob('*.json')):
        try:
            data = json.loads(fp.read_text(encoding='utf-8'))
        except Exception:
            continue
        orig = json.dumps(data, sort_keys=True)

        if 'novice_ready' not in data:
            data['novice_ready'] = True

        if not data.get('beginner_summary'):
            summary = data.get('purpose') or data.get('title') or ''
            data['beginner_summary'] = shorten(summary) if summary else 'Beginner-friendly preset for this set.'

        rg = (data.get('reading_guide') or {})
        tf = pick_timeframe(rg.get('timeframe_alignment'))

        sd = data.get('simple_defaults') or {}
        if not sd.get('timeframe') and tf:
            sd['timeframe'] = tf
        if sd:
            data['simple_defaults'] = sd

        gr = data.get('guardrails') or {}
        # Only fill if missing keys
        if 'universe_cap' not in gr or 'throttle_per_min' not in gr:
            defaults = guardrails_for_timeframe(sd.get('timeframe') if sd else tf)
            gr = {**defaults, **gr}
        data['guardrails'] = gr

        new = json.dumps(data, sort_keys=True)
        if new != orig:
            fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            changed += 1
    return changed


def main():
    c1 = enrich_indicators()
    c2 = enrich_indicator_sets()
    print(f'Enriched indicators: {c1}, sets: {c2}')


if __name__ == '__main__':
    main()
