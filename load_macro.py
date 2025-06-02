import pandas as pd

def load_and_process_macro(file_path, date_col, value_cols, prefix):
    """
    Load and preprocess a single macroeconomic Excel file.

    Args:
        file_path (str): Path to the Excel file.
        date_col (str): Name of the date column.
        value_cols (list of str): List of columns with actual/forecast/previous values.
        prefix (str): Prefix to add to column names to avoid clashes.

    Returns:
        pd.DataFrame: Daily frequency DataFrame with date index and renamed columns.
    """
    df = pd.read_excel(file_path)

    # Extract date part (handles formats like "Apr 10, 2025 (Mar)")
    df[date_col] = df[date_col].astype(str).str.extract(r'([A-Za-z]{3,9}\s\d{1,2},\s\d{4})')[0]
    
    # Parse datetime, drop rows where parsing fails
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    
    # Set date as index and sort
    df = df.set_index(date_col).sort_index()
    
    # Select and rename columns with prefix
    df = df[value_cols].rename(columns=lambda x: f"{prefix}_{x}")
    
    # Resample to daily and forward fill missing values
    df_daily = df.resample('D').ffill()
    
    return df_daily

def load_all_macro(data_folder):
    """
    Load all macroeconomic data files from the data folder, process, and combine.

    Args:
        data_folder (str): Folder path containing macro files named exactly.

    Returns:
        pd.DataFrame: Combined daily macroeconomic DataFrame.
    """
    files_info = [
        ('GDP.xlsx', 'Release Date', ['Actual', 'Forecast', 'Previous'], 'GDP'),
        ('Interest Rate.xlsx', 'Release Date', ['Actual', 'Forecast', 'Previous'], 'InterestRate'),
        ('NFP.xlsx', 'Release Date', ['Actual', 'Forecast', 'Previous'], 'NFP'),
        ('PCE.xlsx', 'Release Date', ['Actual', 'Forecast', 'Previous'], 'PCE'),
        ('PPI.xlsx', 'Release Date', ['Actual', 'Forecast', 'Previous'], 'PPI'),
    ]
    
    macro_dfs = []
    for filename, date_col, val_cols, prefix in files_info:
        path = f"{data_folder}/{filename}"
        print(f"Loading and processing {filename}...")
        df_macro = load_and_process_macro(path, date_col, val_cols, prefix)
        macro_dfs.append(df_macro)
    
    # Combine all macro datasets on date index
    combined_macro = pd.concat(macro_dfs, axis=1).sort_index()
    combined_macro = combined_macro.ffill()
    
    return combined_macro
