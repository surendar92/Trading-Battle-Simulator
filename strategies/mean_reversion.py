import pandas as pd
from .base import BaseStrategy

class MeanReversionStrategy(BaseStrategy):

    def __init__(self, window=20, k=1.5):
        self.window = window
        self.k = k

    def name(self):
        return f"Mean Reversion (w={self.window}, k={self.k})"

    def generate_signals(self, prices):

        rolling_mean = prices.rolling(window=self.window).mean()
        rolling_std  = prices.rolling(window=self.window).std()

        upper_band = rolling_mean + self.k * rolling_std
        lower_band = rolling_mean - self.k * rolling_std

        signals  = pd.Series(0, index=prices.index)
        position = 0  # 0 = flat, 1 = long

        for i in range(self.window, len(prices)):
            price = prices.iloc[i]
            lb    = lower_band.iloc[i]
            ub    = upper_band.iloc[i]

            if price <= lb:
                position = 1   # too cheap → BUY
            elif price >= ub:
                position = 0   # too expensive → SELL

            signals.iloc[i] = position

        return signals