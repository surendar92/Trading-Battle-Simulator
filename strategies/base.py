import pandas as pd

class BaseStrategy:

    def name(self):
        raise NotImplementedError("Strategy must have a name")

    def generate_signals(self, prices: pd.Series) -> pd.Series:
        raise NotImplementedError("Strategy must implement generate_signals()")