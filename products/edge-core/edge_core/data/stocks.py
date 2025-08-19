from __future__ import annotations
import pandas as pd
from .datasets import fetch_hourly_ticker
from ..features.loader import load_indicator_set
from ..features.builder import FeatureBuilder
from ..labels.hourly_direction import label_next_hour_direction
from ..labels.overnight import label_close_to_open_direction
from ..labels.forward import label_forward_return_days


def build_stock_matrix(
    start_date: str,
    end_date: str,
    out_csv: str,
    *,
    ticker: str = "AAPL",
    indicator_set_path: str | None = None,
    label_kind: str | None = None,
) -> str:
    """
    Minimal stocks-only pipeline: hourly OHLCV + indicator set + next-hour direction label.
    """
    hourly = fetch_hourly_ticker(ticker, start_date, end_date)
    if hourly.empty:
        raise RuntimeError(f"No hourly bars for {ticker} from {start_date} to {end_date}")
    df = hourly.copy()
    # Add indicator features via FeatureBuilder (no 0DTE flow)
    indicator_set = None
    if indicator_set_path:
        try:
            indicator_set = load_indicator_set(indicator_set_path)
        except Exception as e:
            print(f"WARN: failed to load indicator set from {indicator_set_path}: {e}")
    fb = FeatureBuilder(distance_max=0, indicator_set=indicator_set)
    df = fb.add_indicator_features(df)
    # Labels
    try:
        kind = (label_kind or '').lower()
        if kind in {'overnight_close_to_open','close_to_open'}:
            df = label_close_to_open_direction(df)
        elif kind.startswith('fwd_ret_') and kind.endswith('d'):
            try:
                n = int(kind.split('_')[-1][:-1])
            except Exception:
                n = 5
            df = label_forward_return_days(df, days=n, classify=True)
        else:
            df = label_next_hour_direction(df)
    except Exception:
        if 'close' in df.columns:
            df['y'] = (df['close'].shift(-1) > df['close']).astype(int)
    df.to_csv(out_csv, index=False)
    return out_csv
