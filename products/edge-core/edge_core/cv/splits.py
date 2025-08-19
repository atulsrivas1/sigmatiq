from typing import Iterator, Tuple
import numpy as np


class PurgedEmbargoedWalkForwardSplit:
    def __init__(self, n_splits: int = 5, *, embargo: float = 0.0):
        self.n_splits = int(n_splits)
        self.embargo = float(embargo)

    def split(self, X) -> Iterator[Tuple[np.ndarray, np.ndarray]]:
        n = len(X)
        fold_sizes = np.full(self.n_splits, n // self.n_splits, dtype=int)
        fold_sizes[: n % self.n_splits] += 1
        indices = np.arange(n)
        current = 0
        for fold_size in fold_sizes:
            start, stop = current, current + fold_size
            test_idx = indices[start:stop]
            # Embargo: drop a fraction of samples before and after test
            embargo_len = int(np.floor(fold_size * self.embargo))
            train_mask = np.ones(n, dtype=bool)
            lo = max(0, start - embargo_len)
            hi = min(n, stop + embargo_len)
            train_mask[lo:hi] = False
            train_idx = indices[train_mask]
            yield train_idx, test_idx
            current = stop
