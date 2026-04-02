import os
import pandas as pd
import yfinance as yf

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")


def fetch_price_data(ticker, start, end, use_cache=True):
    # Create the cache folder if it doesn't exist yet
    os.makedirs(CACHE_DIR, exist_ok=True)

    # Unique filename per ticker + date range
    cache_file = os.path.join(CACHE_DIR, f"{ticker}_{start}_{end}.csv")

    # If we already downloaded this before, just load it from disk
    if use_cache and os.path.exists(cache_file):
        print(f"Loading cached data for {ticker}...")
        df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
        return df

    # Otherwise download fresh from Yahoo Finance
    print(f"Downloading {ticker} from {start} to {end}...")
    raw = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)

    if raw.empty:
        raise ValueError(f"No data found for '{ticker}'. Check the symbol.")

    # Keep ONLY the Close column, drop any missing rows
    df = raw[["Close"]].copy()
    df.columns=['Close']
    df=df.dropna()
    df.index.name = "Date"

    # Save to cache for next time
    if use_cache:
        df.to_csv(cache_file)

    print(f"Got {len(df)} trading days.")
    return df

