"""Model interfaces (skeleton stub)."""

from typing import Protocol, Any

class PredictProba(Protocol):
    def predict_proba(self, X: Any): ...

