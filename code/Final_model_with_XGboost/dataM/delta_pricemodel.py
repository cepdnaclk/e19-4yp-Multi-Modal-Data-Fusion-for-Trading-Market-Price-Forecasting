import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Use non-GUI backend for matplotlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ----------------------------
# Load dataset
# ----------------------------
df = pd.read_csv("monthly_macro_gold_dataset.csv")
df['date'] = pd.to_datetime(df['date'])

# ----------------------------
# Feature Engineering
# ----------------------------
# Lag + Change features for all macro indicators + price
for col in ['price', 'CPI', 'GDP', 'I_R', 'NFP', 'PCE', 'PPI']:
    df[f'{col}_lag_1'] = df[col].shift(1)
    df[f'{col}_change'] = df[col] - df[f'{col}_lag_1']

# Target: monthly price change
df['price_change'] = df['price'] - df['price_lag_1']

# Time-based features
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Drop rows with NaNs created from lagging
df = df.dropna().reset_index(drop=True)

# ----------------------------
# Feature/Target Setup
# ----------------------------
# Use only change features + month/year
feature_cols = [col for col in df.columns if '_change' in col or col in ['month', 'year']]
X = df[feature_cols]
y = df['price_change']

# ----------------------------
# TimeSeriesSplit for evaluation
# ----------------------------
tscv = TimeSeriesSplit(n_splits=5)
last_train_index, last_test_index = list(tscv.split(X))[-1]
X_train, X_test = X.iloc[last_train_index], X.iloc[last_test_index]
y_train, y_test = y.iloc[last_train_index], y.iloc[last_test_index]

# ----------------------------
# Train XGBoost Model
# ----------------------------
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Predict Δprice, then reconstruct actual price
predicted_change = model.predict(X_test)
price_lag_1_test = df['price_lag_1'].iloc[last_test_index].values
predicted_price = price_lag_1_test + predicted_change
true_price = df['price'].iloc[last_test_index].values

# ----------------------------
# Evaluation
# ----------------------------
mae = mean_absolute_error(true_price, predicted_price)
rmse = np.sqrt(mean_squared_error(true_price, predicted_price))
r2 = r2_score(true_price, predicted_price)

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R^2 Score: {r2:.4f}")

# Feature Importance
importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
print("\nTop Features:\n", importances.head(10))

# ----------------------------
# Save Predictions
# ----------------------------
df.loc[df.index[last_test_index], 'predicted_price'] = predicted_price
df.to_csv("monthly_macro_gold_with_price_change_predictions.csv", index=False)
print("✅ Saved predictions to: monthly_macro_gold_with_price_change_predictions.csv")

# ----------------------------
# Plot: Actual vs Predicted
# ----------------------------
plt.figure(figsize=(10, 5))
plt.plot(df['date'].iloc[last_test_index], true_price, label='Actual', marker='o')
plt.plot(df['date'].iloc[last_test_index], predicted_price, label='Predicted', marker='x')
plt.title("Gold Price: Actual vs Predicted (Price Change Model)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("predicted_vs_actual_price_change_model.png")
print("✅ Saved plot to: predicted_vs_actual_price_change_model.png")


from sklearn.metrics import mean_absolute_percentage_error

# 1. MAPE and Accuracy from MAPE
mape = mean_absolute_percentage_error(true_price, predicted_price) * 100
mape_accuracy = 100 - mape

# 2. Accuracy from R^2
r2_accuracy = r2 * 100

# 3. Accuracy from MAE relative to mean price
mean_price = np.mean(true_price)
mae_accuracy = 100 - (mae / mean_price * 100)

# Print
print(f"MAPE: {mape:.2f}% → Accuracy: {mape_accuracy:.2f}%")
print(f"R² Accuracy: {r2_accuracy:.2f}%")
print(f"MAE-Based Accuracy: {mae_accuracy:.2f}%")
