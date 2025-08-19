"""Basic metrics (skeleton stub)."""

def sharpe_ratio(returns, eps: float = 1e-9):
    import numpy as np
    return float((np.mean(returns) / (np.std(returns) + eps)) if len(returns) else 0.0)

