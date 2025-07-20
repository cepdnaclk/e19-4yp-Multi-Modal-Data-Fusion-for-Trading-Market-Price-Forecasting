import pandas as pd
import matplotlib
matplotlib.use('Agg')  # ← ADD THIS LINE
import matplotlib.pyplot as plt
import re

# --- FILEPATHS ---
with_micro_path = "forecast_log.txt"
with_indicators_path = "forecast_log_withouM.txt"

# --- PARSE FORECAST LOG FILE ---
def parse_forecast_log(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    records = []
    temp = {}

    for line in lines:
        if "Forecast Date" in line:
            temp = {}
            temp["date"] = pd.to_datetime(line.split(":")[1].strip())
        elif "Predicted Price" in line:
            temp["predicted_price"] = float(re.findall(r"[-+]?\d*\.\d+|\d+", line)[0])
        elif "Actual Price" in line and "Change" not in line:
            temp["actual_price"] = float(re.findall(r"[-+]?\d*\.\d+|\d+", line)[0])
        elif "Directional Accuracy" in line:
            if all(k in temp for k in ["date", "predicted_price", "actual_price"]):
                records.append(temp)

    return pd.DataFrame(records)

# --- LOAD AND MERGE ---
df_with = parse_forecast_log(with_micro_path)
df_without = parse_forecast_log(with_indicators_path)

df_merged = df_with[['date', 'actual_price']].copy()
df_merged['predicted_with_micro'] = df_with['predicted_price']
df_merged['predicted_with_indicators'] = df_without['predicted_price']

# --- PLOT ---
plt.figure(figsize=(12, 6))
plt.plot(df_merged['date'], df_merged['actual_price'], label='Actual Price', marker='o', color='blue')
plt.plot(df_merged['date'], df_merged['predicted_with_micro'], label='Predicted (With Macro)', marker='x', color='green')
plt.plot(df_merged['date'], df_merged['predicted_with_indicators'], label='Predicted (With Indicators)', marker='s', color='orange')

plt.title("Gold Price Forecast Comparison")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("forecast_comparison_plot_green.png")

print("✅ Plot saved as 'forecast_comparison_plot_green.png'")
