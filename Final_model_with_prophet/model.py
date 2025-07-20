import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error

# ----------------------------
# Load data
# ----------------------------
train_df = pd.read_csv("train.csv")  # contains 69 rows with 'price'
test_df = pd.read_csv("test_single.csv")  # 1 row with new data and 'price' column for actual comparison

train_df['ds'] = pd.to_datetime(train_df['date'])
train_df['y'] = train_df['price']
test_df['ds'] = pd.to_datetime(test_df['date'])

# ----------------------------
# Build and Train Prophet Model
# ----------------------------
model = Prophet()
regressors = ['CPI', 'GDP', 'I_R', 'NFP', 'PCE', 'PPI']
for reg in regressors:
    model.add_regressor(reg)

model.fit(train_df[['ds', 'y'] + regressors])

# ----------------------------
# Predict
# ----------------------------
forecast = model.predict(test_df[['ds'] + regressors])
predicted_price = forecast['yhat'].values[0]
price_lag_1 = train_df.iloc[-1]['price']
predicted_change = predicted_price - price_lag_1

# ----------------------------
# Evaluation
# ----------------------------
actual_price = test_df['price'].values[0]
actual_change = actual_price - price_lag_1
mae = mean_absolute_error([actual_price], [predicted_price])
accuracy = 100 - (mae / actual_price * 100)

# Directional Accuracy
direction_correct = (predicted_change * actual_change) > 0
directional_accuracy = 100.0 if direction_correct else 0.0

# ----------------------------
# Output
# ----------------------------
forecast_date = test_df['ds'].iloc[0].strftime('%Y-%m-%d')

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
    f"{'-'*60}\n"
)

with open("forecast_log.txt", "a", encoding="utf-8") as f:
    f.write(log_line)
