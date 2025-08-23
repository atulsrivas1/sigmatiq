# Extensibility Matrix — Markets, Instruments, Regimes

| Dimension   | Abstraction            | Strategy                                                                                |
|-------------|------------------------|-----------------------------------------------------------------------------------------|
| Market      | MarketAdapter          | Currency normalization, timezone/holidays, provider routing (polygon_us, …)            |
| Instrument  | InstrumentAdapter      | Equities/ETFs/Options/FX: labeler + plan knobs, sizing hints, leverage guards          |
| Regime      | RegimeAdapter          | Volatility/trend flags and threshold bending; disable/slow alerts in extreme regimes   |
| Features    | FeatureSet/IndicatorSet| Bind to indicator_set IDs per market; reuse interface across markets                    |
| Labels      | Labeler                | TP-before-SL w/ max-hold variants; options ATM proxy; multi-horizon                     |
| Serving     | Scorer + PlanGenerator | ModelSpec-calibrated thresholds; plan outputs in ATR/% with max-hold                    |

Notes
- Add new countries by implementing MarketAdapter and updating presets; no change to Scorer/PlanGenerator.
- Add instruments by implementing an InstrumentAdapter; reuse FeatureSource and Scorer.
- Add regime logic without retraining by bending thresholds and sizing hints conservatively.
