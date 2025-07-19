import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Fix backend error for headless plotting
import matplotlib
matplotlib.use('Agg')

# Load the preprocessed dataset (you already generated this)
df = pd.read_csv("monthly_macro_gold_dataset.csv")
df['date'] = pd.to_datetime(df['date'])

# ----------------------------
# Feature Engineering
# ----------------------------

# Create lag features for price and macro indicators
for col in ['price', 'CPI', 'GDP', 'I_R', 'NFP', 'PCE', 'PPI']:
    df[f'{col}_lag_1'] = df[col].shift(1)

# Create change features
df['NFP_change'] = df['NFP'] - df['NFP_lag_1']

# Add temporal features
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Drop rows with NaNs from lag creation
df = df.dropna().reset_index(drop=True)

# ----------------------------
# Train/Test Preparation
# ----------------------------

# Features and target
feature_cols = [col for col in df.columns if col not in ['date', 'price']]
X = df[feature_cols]
y = df['price']

# TimeSeries split
tscv = TimeSeriesSplit(n_splits=5)
last_train_index, last_test_index = list(tscv.split(X))[-1]
X_train, X_test = X.iloc[last_train_index], X.iloc[last_test_index]
y_train, y_test = y.iloc[last_train_index], y.iloc[last_test_index]

# ----------------------------
# Train XGBoost Model
# ----------------------------

model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# ----------------------------
# Evaluation
# ----------------------------

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R^2 Score: {r2:.2f}")

# ----------------------------
# Feature Importance
# ----------------------------

importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
print("\nTop Features:\n", importances.head(10))

# ----------------------------
# Plot Results
# ----------------------------

# plt.figure(figsize=(10, 5))
# plt.plot(df['date'].iloc[last_test_index], y_test.values, label='Actual')
# plt.plot(df['date'].iloc[last_test_index], y_pred, label='Predicted')
# plt.title("Gold Price: Actual vs Predicted")
# plt.xlabel("Date")
# plt.ylabel("Price (USD)")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()


# Plot actual vs predicted
plt.figure(figsize=(10, 5))
plt.plot(df['date'].iloc[last_test_index], y_test.values, label='Actual')
plt.plot(df['date'].iloc[last_test_index], y_pred, label='Predicted')
plt.title("Gold Price: Actual vs Predicted")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("prediction_plot.png")
print("✅ Plot saved as prediction_plot.png")

# Save predictions to the CSV
df.loc[df.index[last_test_index], 'predicted_price'] = y_pred
df.to_csv("monthly_macro_gold_with_predictions.csv", index=False)
print("✅ Predictions added to CSV: monthly_macro_gold_with_predictions.csv")