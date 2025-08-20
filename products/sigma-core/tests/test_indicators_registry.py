from sigma_core.indicators.registry import registry


def test_registry_loads_builtins():
    # Should auto-load builtins from sigma_core.indicators.builtins
    assert isinstance(registry.indicators, dict)
    # Expect at least a handful of common indicators
    expected_some = {'rsi', 'ema', 'macd', 'adx'}
    have = set(registry.indicators.keys())
    assert len(have) > 10
    assert expected_some & have

