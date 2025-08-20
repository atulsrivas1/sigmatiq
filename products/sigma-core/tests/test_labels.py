import pandas as pd
import numpy as np

from sigma_core.labels.forward import label_forward_return_days
from sigma_core.labels.hourly_direction import label_next_hour_direction
from sigma_core.labels.zerosigma import label_headfake_reversal, label_pin_drift


def make_intraday_series(n=10, start_price=100.0):
    dates = pd.date_range('2024-01-01 09:30', periods=n, freq='H', tz='US/Eastern')
    close = start_price + np.cumsum(np.random.randn(n))
    df = pd.DataFrame({'date': dates, 'close': close})
    df['hour_et'] = range(n)
    return df


def test_label_forward_return_days_classify():
    df = make_intraday_series(8)
    out = label_forward_return_days(df, days=1, classify=True)
    assert 'ret_fwd_1d' in out.columns
    assert 'y' in out.columns and 'y_syn' in out.columns
    assert set(pd.unique(out['y']).tolist()) <= {'UP', 'DOWN', 'FLAT'}


def test_label_next_hour_direction_fixed_bp():
    df = make_intraday_series(6)
    out = label_next_hour_direction(df, fixed_bp=10)  # 10 bps
    assert 'ret_next_hour' in out.columns
    assert 'y' in out.columns and 'y_syn' in out.columns
    assert set(pd.unique(out['y']).tolist()) <= {'UP', 'DOWN', 'FLAT'}


def make_hourly_with_features(n=20):
    # Build a small hourly DF with required columns for zerosigma labels
    idx = pd.date_range('2024-01-02 09:30', periods=n, freq='H', tz='US/Eastern')
    df = pd.DataFrame({'date': idx})
    df['close'] = 100 + np.cumsum(np.random.randn(n))
    # Add ATR proxy and optional columns used by labels
    df['atr_14'] = np.abs(pd.Series(np.random.randn(n))).rolling(5, min_periods=1).mean()
    # Optional oi/gamma peaks for pin drift (mostly NaN-safe)
    df['gamma_peak_strike'] = np.nan
    df['oi_peak_strike'] = np.nan
    return df


def test_zerosigma_headfake_reversal_runs():
    df = make_hourly_with_features(24)
    out = label_headfake_reversal(df, open_time='09:30', window_end='10:30')
    assert 'y' in out.columns and 'y_syn' in out.columns
    assert set(pd.unique(out['y']).tolist()) <= {0, 1}


def test_zerosigma_pin_drift_runs():
    df = make_hourly_with_features(24)
    # Without peaks set, function should still return 0/1 labels robustly
    out = label_pin_drift(df, drift_start_time='15:00')
    assert 'y' in out.columns and 'y_syn' in out.columns
    assert set(pd.unique(out['y']).tolist()) <= {0, 1}
