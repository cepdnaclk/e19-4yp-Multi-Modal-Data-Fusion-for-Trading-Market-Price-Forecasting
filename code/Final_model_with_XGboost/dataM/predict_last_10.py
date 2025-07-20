import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error

# Use non-GUI backend for headless plotting
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ----------------------------
# Load training and test data
# ----------------------------
train_df = pd.read_csv("monthly_macro_gold_dataset copy.csv")
test_df = pd.read_csv("test.csv")

train_df['date'] = pd.to_datetime(train_df['date'])
test_df['date'] = pd.to_datetime(test_df['date'])

# ----------------------------
# Feature Engineering
# ----------------------------
for df in [train_df, test_df]:
    for col in ['price', 'CPI', 'GDP', 'I_R', 'NFP', 'PCE', 'PPI']:
        df[f'{col}_lag_1'] = df[col].shift(1)
        df[f'{col}_change'] = df[col] - df[f'{col}_lag_1']
    df['price_change'] = df['price'] - df['price_lag_1']
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

# ----------------------------
# Feature Selection
# ----------------------------
feature_cols = [col for col in train_df.columns if '_change' in col or col in ['month', 'year']]

X_train = train_df[feature_cols]
y_train = train_df['price_change']

X_test = test_df[feature_cols]
y_test = test_df['price']
price_lag_1_test = test_df['price_lag_1'].values

# ----------------------------
# Train XGBoost Regressor
# ----------------------------
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# ----------------------------
# Predict and Reconstruct Price
# ----------------------------
predicted_change = model.predict(X_test)
predicted_price = price_lag_1_test + predicted_change

# ----------------------------
# Evaluation
# ----------------------------
mae = mean_absolute_error(y_test, predicted_price)
rmse = np.sqrt(mean_squared_error(y_test, predicted_price))
r2 = r2_score(y_test, predicted_price)
mape = mean_absolute_percentage_error(y_test, predicted_price) * 100
accuracy = 100 - mape

# Directional Accuracy
correct_direction = np.sum(
    (np.diff(y_test.values) > 0) == (np.diff(predicted_price) > 0)
)
directional_accuracy = correct_direction / (len(y_test) - 1)

# Print metrics
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.4f}")
print(f"MAPE: {mape:.2f}% → Accuracy: {accuracy:.2f}%")
print(f"Directional Accuracy: {directional_accuracy:.2%}")

# ----------------------------
# Save predictions and plot
# ----------------------------
test_df['predicted_price'] = predicted_price
test_df.to_csv("test_with_predictions.csv", index=False)

plt.figure(figsize=(10, 5))
plt.plot(test_df['date'], y_test, label='Actual', marker='o')
plt.plot(test_df['date'], predicted_price, label='Predicted', marker='x')
plt.title("Gold Price Prediction on Last 10 Records")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("prediction_vs_actual_last_10.png")

print("✅ Saved: test_with_predictions.csv")
print("✅ Saved: prediction_vs_actual_last_10.png")
