import pandas as pd

def moving_average(series, period=10):
    return series.rolling(window=period).mean()

def exponential_moving_average(series, period):
    return series.ewm(span=period, adjust=False).mean()

def macd(series, short_period=12, long_period=26):
    ema_short = exponential_moving_average(series, short_period)
    ema_long = exponential_moving_average(series, long_period)
    return ema_short - ema_long

def momentum(series, period=4):
    return series - series.shift(period)

def rate_of_change(series, period=2):
    return (series - series.shift(period)) / series.shift(period) * 100

def relative_strength_index(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = -delta.clip(upper=0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def bollinger_bands(series, period=20):
    ma = moving_average(series, period)
    std = series.rolling(window=period).std()
    upper_band = ma + (std * 2)
    lower_band = ma - (std * 2)
    return upper_band, lower_band

def commodity_channel_index(df, period=20):
    tp = (df['high'] + df['low'] + df['close']) / 3
    ma = tp.rolling(window=period).mean()
    mean_dev = tp.rolling(window=period).apply(lambda x: (x - x.mean()).abs().mean())
    cci = (tp - ma) / (0.015 * mean_dev)
    return cci

