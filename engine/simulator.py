import numpy as np
import pandas as pd

class Simulator:

    def __init__(self, initial_capital=10000.0):
        self.initial_capital = initial_capital

    def run(self, prices, strategies):

        equity_curves = {}

        for strategy in strategies:
            print(f"Running: {strategy.name()}")
            signals = strategy.generate_signals(prices)
            equity  = self._simulate_portfolio(prices, signals)
            equity_curves[strategy.name()] = equity

        return pd.DataFrame(equity_curves, index=prices.index)

    def _simulate_portfolio(self, prices, signals):

        cash     = self.initial_capital
        holdings = 0.0
        equity   = []

        for i in range(len(prices)):
            price  = float(prices.iloc[i])
            signal = int(signals.iloc[i])

            if signal == 1 and holdings == 0 and cash > 0:
                # BUY — invest all cash
                holdings = cash / price
                cash = 0.0

            elif signal == 0 and holdings > 0:
                # SELL — convert all holdings to cash
                cash     = holdings * price
                holdings = 0.0

            # Record portfolio value today
            portfolio_value = cash + holdings * price
            equity.append(portfolio_value)

        return pd.Series(equity, index=prices.index)

    def compute_metrics(self, equity):

        returns      = equity.pct_change().dropna()
        total_return = (equity.iloc[-1] - equity.iloc[0]) / equity.iloc[0] * 100

        if returns.std() == 0:
            sharpe = 0.0
        else:
            sharpe = (returns.mean() / returns.std()) * np.sqrt(252)

        rolling_max  = equity.cummax()
        drawdown     = (equity - rolling_max) / rolling_max * 100
        max_drawdown = drawdown.min()

        return {
            "total_return (%)": round(total_return, 2),
            "sharpe_ratio"    : round(sharpe, 3),
            "max_drawdown (%)": round(max_drawdown, 2),
        }
