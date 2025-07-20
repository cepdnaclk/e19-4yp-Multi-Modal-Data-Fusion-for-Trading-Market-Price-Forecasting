import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ----------------------------
# Load Data
# ----------------------------
df = pd.read_csv("financial_data.csv")  # Replace with your file
df['time'] = pd.to_datetime(df['time'])
df.sort_values('time', inplace=True)

# ----------------------------
# Feature Engineering
# ----------------------------
df['price_change'] = df['price'].shift(-1) - df['price']
df['price_lag_1'] = df['price'].shift(1)
df['price_lag_2'] = df['price'].shift(2)
df['price_lag_3'] = df['price'].shift(3)
df['price_mean_3'] = df['price'].rolling(3).mean().shift(1)
df['price_mean_5'] = df['price'].rolling(5).mean().shift(1)
df['price_std_5'] = df['price'].rolling(5).std().shift(1)
df['price_diff_1'] = df['price_lag_1'] - df['price_lag_2']
df['price_diff_2'] = df['price_lag_2'] - df['price_lag_3']
df['hour'] = df['time'].dt.hour
df['dayofweek'] = df['time'].dt.dayofweek
df.dropna(inplace=True)

# ----------------------------
# Define Features & Target
# ----------------------------
features = [
    'price', 'RSI', 'MACD', 'Signal', 'SMA_50', 'tick_volume',
    'CPI_Actual', 'GDP_Actual', 'hour', 'dayofweek',
    'price_lag_1', 'price_lag_2', 'price_lag_3',
    'price_mean_3', 'price_mean_5', 'price_std_5',
    'price_diff_1', 'price_diff_2'
]
X = df[features]
y = df['price_change']

# ----------------------------
# Train/Test Split
# ----------------------------
split_index = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]

# ----------------------------
# Train Model
# ----------------------------
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)
predicted_change = model.predict(X_test)

# ----------------------------
# Reconstruct Predicted Prices
# ----------------------------
aligned_df = df[['time', 'price']].copy()
aligned_df['actual_price'] = df['price'].shift(-1)
aligned_df = aligned_df.iloc[split_index:split_index + len(predicted_change)].reset_index(drop=True)
aligned_df.dropna(inplace=True)

actual_price = aligned_df['actual_price'].values
price_base = aligned_df['price'].values
predicted_price = price_base + predicted_change[:len(actual_price)]
time_slice = aligned_df['time'].values

# ----------------------------
# Evaluate
# ----------------------------
mae = mean_absolute_error(actual_price, predicted_price)
rmse = np.sqrt(mean_squared_error(actual_price, predicted_price))
r2 = r2_score(actual_price, predicted_price)

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.4f}")

# ----------------------------
# Save Forecast CSV
# ----------------------------
forecast_df = pd.DataFrame({
    'time': time_slice,
    'actual_price': actual_price,
    'predicted_price': predicted_price
})
forecast_df.to_csv("forecast_output.csv", index=False)
print("✅ Saved forecast_output.csv")

# ----------------------------
# Plot
# ----------------------------
plt.figure(figsize=(12, 6))
plt.plot(time_slice, actual_price, label='Actual Price', marker='o')
plt.plot(time_slice, predicted_price, label='Predicted Price (from Δ)', marker='x')
plt.title("Gold Price Forecast (XGBoost Δprice)")
plt.xlabel("Time")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("price_change_forecast_plot.png")
print("✅ Saved plot: price_change_forecast_plot.png")
