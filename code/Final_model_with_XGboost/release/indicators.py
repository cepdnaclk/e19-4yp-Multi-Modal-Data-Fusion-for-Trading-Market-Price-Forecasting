import pandas as pd
import csv

def calculate_rsi(data, periods=14):
    """Calculate 14-period RSI."""
    delta = data['price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    """Calculate MACD and Signal Line."""
    short_ema = data['price'].ewm(span=short_period, adjust=False).mean()
    long_ema = data['price'].ewm(span=long_period, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    return macd, signal

def add_technical_indicators(input_file, output_file):
    # Read origin_with_macro.csv, ensuring Macro_factor is read as string
    df = pd.read_csv(input_file, dtype={'Macro_factor': str})
    
    # Ensure Macro_factor is padded to 6 digits
    df['Macro_factor'] = df['Macro_factor'].str.zfill(6)
    
    # Ensure 'time' is in datetime format and sorted
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
    df = df.sort_values('time')
    
    # Calculate RSI (14-period)
    df['RSI'] = calculate_rsi(df, periods=14)
    
    # Calculate MACD (12, 26, 9)
    df['MACD'], df['Signal'] = calculate_macd(df, short_period=12, long_period=26, signal_period=9)
    
    # Calculate Simple Moving Averages (50, 200, 280)
    df['SMA_50'] = df['price'].rolling(window=50).mean()
    df['SMA_200'] = df['price'].rolling(window=200).mean()
    df['SMA_280'] = df['price'].rolling(window=280).mean()
    
    # Save to a new CSV file with string quoting to preserve formats
    df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(f"Saved output to {output_file}")

# Example usage
if __name__ == "__main__":
    input_file = 'origin_with_macro.csv'
    output_file = 'origin_with_indicators.csv'
    add_technical_indicators(input_file, output_file)