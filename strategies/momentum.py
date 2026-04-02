import pandas as pd
from .base import BaseStrategy


class MomentumStrategy(BaseStrategy):
    def __init__(self, window=20):
        self.window = window
    def name(self):
        return f"Momentum (w={self.window})"
    def generate_signals(self, prices):
        # Get the price from `window` days ago
        past_prices = prices.shift(self.window)

        # 1 if today > past, else 0
        signals = (prices > past_prices).astype(int)

        # No past data for first `window` days → stay out
        signals.iloc[:self.window] = 0

        return signals