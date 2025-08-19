from abc import ABC, abstractmethod
import pandas as pd

class Indicator(ABC):
    """
    Base class for all technical indicators.
    """

    @abstractmethod
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the indicator and returns a DataFrame with the results.
        """
        pass
