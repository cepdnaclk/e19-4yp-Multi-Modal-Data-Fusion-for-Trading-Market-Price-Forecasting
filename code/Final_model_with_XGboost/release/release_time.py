import pandas as pd
from datetime import datetime, timedelta
import re

def parse_date_time(date_str, time_str):
    """Parse date and time strings into a datetime object."""
    # Clean the date string by removing parenthetical suffixes (e.g., '(Apr)')
    date_str = re.sub(r'\s*\([^)]+\)', '', date_str).strip()
    
    # Clean the time string by removing non-breaking spaces and extra whitespace
    time_str = time_str.replace('\xa0', '').strip() if isinstance(time_str, str) else ''
    
    # Try parsing as a full timestamp if date_str contains both date and time
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        pass
    
    # Try different date formats
    try:
        # Try full month name (e.g., 'April 10, 2025')
        date_obj = datetime.strptime(date_str, '%B %d, %Y')
    except ValueError:
        try:
            # Try abbreviated month name (e.g., 'Apr 10, 2025')
            date_obj = datetime.strptime(date_str, '%b %d, %Y')
        except ValueError:
            # Try ISO date format (e.g., '2025-05-07')
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Try parsing time with seconds (HH:MM:SS) or without (HH:MM)
    try:
        time_obj = datetime.strptime(time_str, '%H:%M:%S')
    except ValueError:
        time_obj = datetime.strptime(time_str, '%H:%M')
    
    return datetime.combine(date_obj.date(), time_obj.time())

def get_release_times(macro_file):
    """Read a macroeconomic CSV file and return a list of release datetimes."""
    df = pd.read_csv(macro_file)
    release_times = []
    for _, row in df.iterrows():
        release_time = parse_date_time(row['Release Date'], row['Time'])
        release_times.append(release_time)
    return release_times

def add_macro_factor_column(origin_file, macro_files, output_file):
    # Read origin.csv
    df = pd.read_csv(origin_file)
    df['time'] = pd.to_datetime(df['time'])
    
    # Initialize Macro_factor column with '000000'
    df['Macro_factor'] = '000000'
    
    # Define macroeconomic factors in order for the 6-bit string
    macro_factors = ['CPI', 'GDP', 'NFP', 'PCE', 'PPI', 'Interest_Rate']
    
    # Load release times for each macroeconomic factor
    release_times = {}
    for factor, file in macro_files.items():
        release_times[factor] = get_release_times(file)
    
    # For each row in origin.csv, check for macroeconomic releases
    for idx, row in df.iterrows():
        row_time = row['time']
        # Define the 30-minute window (e.g., 15:30:00 to 15:59:59)
        window_end = row_time + timedelta(minutes=29, seconds=59)
        
        # Initialize the 6-bit string
        bits = ['0'] * 6
        for i, factor in enumerate(macro_factors):
            for release_time in release_times[factor]:
                # Check if release_time falls within the 30-minute window
                if row_time <= release_time <= window_end:
                    bits[i] = '1'
        
        # Update Macro_factor column, ensuring 6-digit string
        df.at[idx, 'Macro_factor'] = ''.join(bits).zfill(6)
    
    # Ensure Macro_factor is treated as a string
    df['Macro_factor'] = df['Macro_factor'].astype(str).str.zfill(6)
    
    # Save to a new CSV file with string formatting
    df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(f"Saved output to {output_file}")

# Example usage
if __name__ == "__main__":
    import csv
    origin_file = 'origin.csv'
    macro_files = {
        'CPI': 'CPI.csv',
        'GDP': 'GDP.csv',
        'NFP': 'NFP.csv',
        'PCE': 'PCE.csv',
        'PPI': 'PPI.csv',
        'Interest_Rate': 'Interest_Rate.csv'
    }
    output_file = 'origin_with_macro.csv'
    
    add_macro_factor_column(origin_file, macro_files, output_file)