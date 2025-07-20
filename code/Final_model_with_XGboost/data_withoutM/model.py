import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

# ----------------------------
# Load training and test data
# ----------------------------
train_df = pd.read_csv("train.csv")             # Must have: date, price
test_df = pd.read_csv("test_single.csv")        # Must have: date, price (for actual comparison)

train_df['date'] = pd.to_datetime(train_df['date'])
test_df['date'] = pd.to_datetime(test_df['date'])

# ----------------------------
# Extract last known row
# ----------------------------
last_row = train_df.iloc[-1]

# Month/year features
train_df['month'] = train_df['date'].dt.month
train_df['year'] = train_df['date'].dt.year
test_df['month'] = test_df['date'].dt.month
test_df['year'] = test_df['date'].dt.year

# ----------------------------
# Lag/change features for training
# ----------------------------
train_df['price_lag_1'] = train_df['price'].shift(1)
train_df['price_change'] = train_df['price'] - train_df['price_lag_1']
train_df.dropna(inplace=True)
train_df.reset_index(drop=True, inplace=True)

# ----------------------------
# Lag/change for test row
# ----------------------------
test_df['price_lag_1'] = last_row['price']
test_df['price_change'] = test_df['price'] - test_df['price_lag_1']

# ----------------------------
# Feature selection (no macro)
# ----------------------------
feature_cols = ['price_lag_1', 'month', 'year']

X_train = train_df[feature_cols]
y_train = train_df['price_change']

X_test = test_df[feature_cols]

# ----------------------------
# Train and Predict
# ----------------------------
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

predicted_change = model.predict(X_test)[0]
price_lag_1 = test_df['price_lag_1'].values[0]
predicted_price = price_lag_1 + predicted_change

# ----------------------------
# Evaluation
# ----------------------------
actual_price = test_df['price'].values[0]
actual_change = actual_price - price_lag_1
abs_error = abs(actual_price - predicted_price)
accuracy = 100 - (abs_error / actual_price * 100)

# Directional Accuracy
direction_correct = np.sign(predicted_change) == np.sign(actual_change)
directional_accuracy = 100.0 if direction_correct else 0.0

# ----------------------------
# Output
# ----------------------------
forecast_date = test_df['date'].iloc[0].strftime('%Y-%m-%d')
print(f"📅 Forecast Date       : {forecast_date}")
print(f"Last Known Price      : {price_lag_1:.2f}")
print(f"Predicted Price       : {predicted_price:.2f}")
print(f"Predicted Change      : {predicted_change:.2f}")
print(f"📌 Actual Price        : {actual_price:.2f}")
print(f"📌 Actual Price Change : {actual_change:.2f}")
print(f"🎯 Accuracy            : {accuracy:.2f}%")
print(f"📊 Directional Accuracy: {directional_accuracy:.2f}%")

# ----------------------------
# Logging
# ----------------------------
log_line = (
    f"\n📅 Forecast Date       : {forecast_date}\n"
    f"Last Known Price      : {price_lag_1:.2f}\n"
    f"Predicted Price       : {predicted_price:.2f}\n"
    f"Predicted Change      : {predicted_change:.2f}\n"
    f"📌 Actual Price        : {actual_price:.2f}\n"
    f"📌 Actual Price Change : {actual_change:.2f}\n"
    f"🎯 Accuracy            : {accuracy:.2f}%\n"
    f"📊 Directional Accuracy: {directional_accuracy:.2f}%\n"
    f"{'-'*50}\n"
)

with open("forecast_log.txt", "a", encoding="utf-8") as f:
    f.write(log_line)
