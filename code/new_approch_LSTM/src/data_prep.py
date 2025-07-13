# src/data_prep.py

from pathlib import Path
import pandas as pd

def load_data() -> pd.DataFrame:
    """
    Load 30-minute XAUUSD CSV (with columns time, open, high, low, close, tick_volume)
    from the project’s data/ folder, parse the 'time' column as datetime index,
    and rename columns to OHLCV.
    """
    csv_path = Path(__file__).resolve().parent.parent / 'data' / 'XAUUSD_30m_from_2018.csv'
    df = pd.read_csv(
        csv_path,
        parse_dates=['time'],      # parse the 'time' column
        index_col='time'           # set it as index
    )
    # Rename to match our pipeline
    df.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'tick_volume': 'Volume'
    }, inplace=True)
    return df[['Open', 'High', 'Low', 'Close', 'Volume']]

if __name__ == '__main__':
    df = load_data()
    print(df.head())
