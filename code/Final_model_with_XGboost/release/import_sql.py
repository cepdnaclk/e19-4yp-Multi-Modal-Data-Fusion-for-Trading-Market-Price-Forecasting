import pandas as pd
from sqlalchemy import create_engine, types

def import_csv_to_sqlite(csv_file, db_file, table_name):
    # Read the CSV, ensuring Macro_factor is read as string
    df = pd.read_csv(csv_file, dtype={'Macro_factor': str})
    
    # Ensure Macro_factor is padded to 6 digits
    df['Macro_factor'] = df['Macro_factor'].str.zfill(6)
    
    # Convert time column to datetime
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
    
    # Define SQL data types for each column to preserve formats
    dtype_dict = {
        'time': types.DateTime,
        'price': types.Float,
        'candletype': types.Integer,
        'candlebody': types.Float,
        'candleupperwick': types.Float,
        'candlelowerwick': types.Float,
        'tick_volume': types.Integer,
        'CPI_Actual': types.Float,
        'CPI_Forecast': types.Float,
        'CPI_Previous': types.Float,
        'GDP_Actual': types.Float,
        'GDP_Forecast': types.Float,
        'GDP_Previous': types.Float,
        'Interest_Rate_Actual': types.Float,
        'Interest_Rate_Forecast': types.Float,
        'Interest_Rate_Previous': types.Float,
        'PCE_Actual': types.Float,
        'PCE_Forecast': types.Float,
        'PCE_Previous': types.Float,
        'PPI_Actual': types.Float,
        'PPI_Forecast': types.Float,
        'PPI_Previous': types.Float,
        'Macro_factor': types.String(6),  # Enforce 6-character string
        'RSI': types.Float,
        'MACD': types.Float,
        'Signal': types.Float,
        'SMA_50': types.Float,
        'SMA_200': types.Float,
        'SMA_280': types.Float
    }
    
    # Create SQLite database connection
    engine = create_engine(f'sqlite:///{db_file}')
    
    # Import DataFrame to SQLite
    df.to_sql(table_name, engine, if_exists='replace', index=False, dtype=dtype_dict)
    
    print(f"Imported {len(df)} rows from {csv_file} to SQLite database {db_file}, table {table_name}")

# Example usage
if __name__ == "__main__":
    csv_file = 'origin_with_indicators.csv'
    db_file = 'financial_data.db'
    table_name = 'financial_data'
    import_csv_to_sqlite(csv_file, db_file, table_name)