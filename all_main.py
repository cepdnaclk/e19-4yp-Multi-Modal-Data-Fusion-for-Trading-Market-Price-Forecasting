import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
from data_preparation import *
from model import build_lstm_model, train_model
from utils import profit_accuracy, plot_history, print_classification_report
from load_macro import load_all_macro

def main():
    merged_path = './data/forex_with_all_macros.xlsx'  # Use the merged file directly

    print("Loading merged Forex and macroeconomic data...")
    # Load merged data with time parsed as datetime index
    df = pd.read_excel(merged_path, parse_dates=['time'])
    df.set_index('time', inplace=True)

    print("Calculating technical indicators...")
    df = calculate_technical_indicators(df)

    print("Labeling data...")
    df = label_data(df)

    features = [
        'open', 'high', 'low', 'close', 'tick_volume',
        'MA_10', 'MACD', 'Momentum_4', 'ROC_2', 'RSI_14',
        'BB_upper', 'BB_lower', 'CCI_20',
        'CPI_Actual', 'CPI_Forecast', 'CPI_Previous',
        'GDP_Actual', 'GDP_Forecast', 'GDP_Previous',
        'Interest_Rate_Actual', 'Interest_Rate_Forecast', 'Interest_Rate_Previous',
        # 'NFP_Actual', 'NFP_Forecast', 'NFP_Previous',
        'PCE_Actual', 'PCE_Forecast', 'PCE_Previous',
        'PPI_Actual', 'PPI_Forecast', 'PPI_Previous'
    ]


    time_steps = 30
    print("Creating sequences...")
    X, y = create_sequences(df, features, 'label', time_steps)

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    print("Scaling features...")
    X_train_scaled, X_test_scaled = scale_features(X_train, X_test)

    print("Building model...")
    model = build_lstm_model(time_steps, X_train.shape[2])
    model.summary()

    print("Training model...")
    history = train_model(model, X_train_scaled, y_train, X_test_scaled, y_test, epochs=20, batch_size=32)

    print("Evaluating model...")
    y_pred_prob = model.predict(X_test_scaled)
    y_pred = np.argmax(y_pred_prob, axis=1)

    print_classification_report(y_test, y_pred)
    prof_acc = profit_accuracy(y_test, y_pred)
    print(f"Profit Accuracy: {prof_acc:.4f}")

    plot_history(history)

if __name__ == "__main__":
    main()
