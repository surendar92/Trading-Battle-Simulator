import numpy as np
import pandas as pd
from .base import BaseStrategy


class RandomStrategy(BaseStrategy):

    def __init__(self, seed=42):
        self.seed = seed

    def name(self):
        return f"Random (seed={self.seed})"

    def generate_signals(self, prices: pd.Series) -> pd.Series:
        rng = np.random.default_rng(self.seed)
        random_signals = rng.integers(0, 2, size=len(prices))
        return pd.Series(random_signals, index=prices.index)