import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt

# ----------------------------
# Load and Normalize
# ----------------------------
without_macro_df = pd.read_csv("xauusd_M1_full_predictions.csv")  # Must have: time, actual_price, predicted_price
macro_df = pd.read_csv("test_with_predictions.csv")               # Must have: date, predicted_price

# Fix column names and parse dates
without_macro_df.rename(columns={'time': 'date'}, inplace=True)
without_macro_df['date'] = pd.to_datetime(without_macro_df['date'])
macro_df['date'] = pd.to_datetime(macro_df['date'])

# ----------------------------
# Merge and Align
# ----------------------------
df_merged = without_macro_df[['date', 'actual_price', 'predicted_price']].rename(
    columns={'predicted_price': 'predicted_without_macro'}
)
df_merged = df_merged.merge(
    macro_df[['date', 'predicted_price']].rename(columns={'predicted_price': 'predicted_with_macro'}),
    on='date',
    how='inner'
)

# ----------------------------
# Plot 1: Actual vs Predicted WITH Macro
# ----------------------------
plt.figure(figsize=(12, 6))
plt.plot(df_merged['date'], df_merged['actual_price'], label='Actual Price', marker='o', color='blue')
plt.plot(df_merged['date'], df_merged['predicted_with_macro'], label='Predicted (With Macro)', marker='x', color='green')
plt.title("Gold Price Forecast: Actual vs Predicted (With Macro)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("forecast_with_macro.png")
print("✅ Saved: forecast_with_macro.png")

# ----------------------------
# Plot 2: Actual vs Predicted WITHOUT Macro
# ----------------------------
plt.figure(figsize=(12, 6))
plt.plot(df_merged['date'], df_merged['actual_price'], label='Actual Price', marker='o', color='blue')
plt.plot(df_merged['date'], df_merged['predicted_without_macro'], label='Predicted (Without Macro)', marker='s', color='orange')
plt.title("Gold Price Forecast: Actual vs Predicted (Without Macro)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("forecast_without_macro.png")
print("✅ Saved: forecast_without_macro.png")
