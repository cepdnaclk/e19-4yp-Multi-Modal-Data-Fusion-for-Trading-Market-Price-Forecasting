import pandas as pd
import os

def convert_xlsx_to_csv(xlsx_file):
    # Read the XLSX file
    df = pd.read_excel(xlsx_file)
    
    # Create CSV filename by replacing .xlsx with .csv
    csv_file = os.path.splitext(xlsx_file)[0] + '.csv'
    
    # Save to CSV without modifying the original XLSX
    df.to_csv(csv_file, index=False)
    print(f"Converted {xlsx_file} to {csv_file}")

# Example usage
if __name__ == "__main__":
    # Replace 'input.xlsx' with your file path
    input_file = 'PPI.xlsx'
    if os.path.exists(input_file):
        convert_xlsx_to_csv(input_file)
    else:
        print(f"File {input_file} not found")