import pandas as pd

# Load the dataset
data_path = 'CPI.xlsx'
df = pd.read_excel(data_path)

# Display basic info about dataset
print(df.info())

# Show first 5 rows to understand columns and data
print(df.head())
