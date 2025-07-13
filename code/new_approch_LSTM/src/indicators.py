# src/indicators.py

import sys, os
# When running as a script, __file__ is defined – prepend its folder
if '__file__' in globals():
    sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
from data_prep import load_data

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute RSI, MACD, and Bollinger Bands manually using Pandas.
    """
    # RSI
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(span=14, adjust=False).mean()
    avg_loss = loss.ewm(span=14, adjust=False).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    ema_fast = df['Close'].ewm(span=12, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_fast - ema_slow
    df['MACD_sig'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Bollinger Bands
    sma20 = df['Close'].rolling(window=20).mean()
    std20 = df['Close'].rolling(window=20).std()
    df['BB_upper'] = sma20 + (2 * std20)
    df['BB_lower'] = sma20 - (2 * std20)

    df.dropna(inplace=True)
    return df

if __name__ == '__main__':
    df = load_data()
    df = add_indicators(df)
    print(df.tail())
