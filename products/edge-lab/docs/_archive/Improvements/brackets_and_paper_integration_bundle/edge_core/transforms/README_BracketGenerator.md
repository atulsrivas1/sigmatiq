# BracketGenerator — Quick Start
*Generated: 2025-08-15 21:19 UTC*

- Import: `from edge_core.transforms.bracket_generator import Params, generate_brackets`
- Call at **signal-time** with features available to the model (no look-ahead).
- Returned dict is inserted into the order payload as `bracket` for Paper Broker.

**Example**
```python
row = { "entry_px": 100.0, "atr_14": 2.5 }
params = Params(mode="atr", atr_mult_stop=1.2, atr_mult_target=2.0, time_stop_days=10)
bracket = generate_brackets(row, params)
```
