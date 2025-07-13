import pandas as pd
import numpy as np

# 1) RSI overbought/oversold crossing events
def find_rsi_events(df: pd.DataFrame, oversold=30, overbought=70) -> pd.DatetimeIndex:
    delta = df['Close'].diff()
    gain = delta.clip(lower=0).ewm(span=14, adjust=False).mean()
    loss = -delta.clip(upper=0).ewm(span=14, adjust=False).mean()
    rsi = 100 - 100 / (1 + gain / loss)
    cross_up = (rsi.shift(1) < oversold) & (rsi >= oversold)
    cross_down = (rsi.shift(1) > overbought) & (rsi <= overbought)
    return df.index[cross_up | cross_down]

# 2) MACD line & signal line crossovers
def find_macd_crossovers(df: pd.DataFrame) -> pd.DatetimeIndex:
    ema_fast = df['Close'].ewm(span=12, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=26, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=9, adjust=False).mean()
    cross_up = (macd.shift(1) < signal.shift(1)) & (macd > signal)
    cross_down = (macd.shift(1) > signal.shift(1)) & (macd < signal)
    return df.index[cross_up | cross_down]

# 3) Fast/Slow EMA cross events
def find_ema_crosses(df: pd.DataFrame, fast=12, slow=26) -> pd.DatetimeIndex:
    ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
    cross_up = (ema_fast.shift(1) < ema_slow.shift(1)) & (ema_fast > ema_slow)
    cross_down = (ema_fast.shift(1) > ema_slow.shift(1)) & (ema_fast < ema_slow)
    return df.index[cross_up | cross_down]

# 4) Bollinger Band touches
def find_bb_touch(df: pd.DataFrame, window=20, dev=2) -> pd.DatetimeIndex:
    sma = df['Close'].rolling(window, min_periods=window).mean()
    std = df['Close'].rolling(window, min_periods=window).std()
    upper = sma + dev * std
    lower = sma - dev * std
    touch_up = df['Close'] >= upper
    touch_down = df['Close'] <= lower
    return df.index[touch_up | touch_down]

# 5) Support & Resistance (local minima/maxima)
def find_support_resistance(df: pd.DataFrame, lookback=100) -> pd.DatetimeIndex:
    lows = df['Low'].rolling(lookback, center=True, min_periods=1).min()
    highs = df['High'].rolling(lookback, center=True, min_periods=1).max()
    sr = (df['Low'] == lows) | (df['High'] == highs)
    return df.index[sr]