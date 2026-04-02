import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from engine.Fetcher import fetch_price_data
from strategies.momentum import MomentumStrategy
from strategies.mean_reversion import MeanReversionStrategy
from strategies.random_strat import RandomStrategy
from engine.simulator import Simulator
from visualization.animator import animate_equity_curves

# ── CONFIG ────────────────────────────────────────────────────────
TICKER          = "AAPL"
START_DATE      = "2015-01-01"
END_DATE        = ("2023"
                   "-01-01")
INITIAL_CAPITAL = 10_000
# ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  Algorithmic Trading Battle Simulator")
    print("=" * 50)

    # 1. Get data
    df     = fetch_price_data(TICKER, START_DATE, END_DATE)
    prices = df["Close"]

    # 2. Define strategies
    strategies = [
        MomentumStrategy(window=20),
        MeanReversionStrategy(window=20, k=1.5),
        RandomStrategy(seed=42),
    ]

    # 3. Run simulation
    sim       = Simulator(initial_capital=INITIAL_CAPITAL)
    equity_df = sim.run(prices, strategies)

    # 4. Print metrics
    print("\n── Performance Metrics ──────────────────────")
    for col in equity_df.columns:
        metrics = sim.compute_metrics(equity_df[col])
        print(f"\n{col}")
        for key, val in metrics.items():
            print(f"   {key:<25} {val}")

    # 5. Animate
    print("\nLaunching chart...")
    animate_equity_curves(
        equity_df,
        title=f"Trading Battle: {TICKER} ({START_DATE} to {END_DATE})"
    )

if __name__ == "__main__":
    main()