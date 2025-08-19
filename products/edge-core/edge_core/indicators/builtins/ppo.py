from ..base import Indicator
import pandas as pd

class PPO(Indicator):
    CATEGORY = "oscillator"
    SUBCATEGORY = "ppo"

    def __init__(self, column: str = 'close', fast: int = 12, slow: int = 26, signal: int = 9):
        self.column = column
        self.fast = int(fast)
        self.slow = int(slow)
        self.signal = int(signal)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out['ppo_line'] = 0.0
            out['ppo_signal'] = 0.0
            out['ppo_hist'] = 0.0
            return out
        x = pd.to_numeric(df[self.column], errors='coerce').astype(float)
        ema_fast = x.ewm(span=self.fast, adjust=False).mean()
        ema_slow = x.ewm(span=self.slow, adjust=False).mean()
        ppo_line = (ema_fast - ema_slow) / (ema_slow + 1e-12) * 100.0
        ppo_signal = ppo_line.ewm(span=self.signal, adjust=False).mean()
        ppo_hist = ppo_line - ppo_signal
        out['ppo_line'] = ppo_line.fillna(0.0)
        out['ppo_signal'] = ppo_signal.fillna(0.0)
        out['ppo_hist'] = ppo_hist.fillna(0.0)
        return out

