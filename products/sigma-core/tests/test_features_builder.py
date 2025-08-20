import pandas as pd
import numpy as np
from sigma_core.features.builder import FeatureBuilder, select_features


def make_flow_df(n=21):
    df = pd.DataFrame({
        'date': pd.date_range('2024-01-02', periods=n, freq='H'),
        'price_level': np.linspace(95, 105, n),
        'spy_prev_close': 100.0,
        'calls_sold': np.random.rand(n),
        'puts_sold': np.random.rand(n),
    })
    return df


def test_feature_builder_adds_expected_columns():
    df = make_flow_df(21)
    fb = FeatureBuilder(distance_max=2)
    out = fb.add_base_features(df)
    # Check a few derived features exist
    for c in ['calls_sold_d-2','calls_sold_d0','calls_sold_d2','puts_sold_total','pc_ratio','imbalance']:
        assert c in out.columns
    # Dealer orientation flag present
    out2 = fb.add_dealer_orientation(out)
    assert 'mm_profit_dir_simple' in out2.columns


def test_select_features_filters_by_prefixes():
    df = make_flow_df(10)
    fb = FeatureBuilder(distance_max=1)
    out = fb.add_base_features(df)
    feats = select_features(out)
    assert isinstance(feats, list) and feats
    # Should include at least one per-distance feature
    assert any(c.startswith('calls_sold_d') for c in feats)

