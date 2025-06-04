import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout, Concatenate
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from data_preparation import calculate_technical_indicators, label_data
from utils import profit_accuracy, plot_history, print_classification_report
from tensorflow.keras.optimizers import Adam

def process_macro_data(df, macro_cols, window=3):
    """
    Compute macroeconomic "surprise" features and generate lagged windows around each release.
    """
    # Compute surprise = Actual - Forecast for each macro
    surprise_cols = []
    for name in ['CPI', 'GDP', 'Interest_Rate', 'PCE', 'PPI']:
        act = f"{name}_Actual"
        fc  = f"{name}_Forecast"
        if act in df.columns and fc in df.columns:
            sur = f"{name}_Surprise"
            df[sur] = df[act] - df[fc]
            surprise_cols.append(sur)
            # Add lagged surprise windows
            for k in range(-window, window+1):
                if k == 0:
                    continue
                df[f"{sur}_lag{k}"] = df[sur].shift(k)
    return df


def create_sequences(df, tech_features, macro_features, target_col, time_steps):
    """
    Build overlapping sequences for technical and macro branches efficiently,
    without reallocating large arrays in each loop.
    Returns:
      X_tech: (n_samples, time_steps, len(tech_features))
      X_macro: (n_samples, time_steps, len(macro_features))
      y: (n_samples,)
    """
    # Pre-extract full arrays once
    arr_tech  = df[tech_features].values
    arr_macro = df[macro_features].values
    y_all     = df[target_col].values

    X_tech, X_macro, y = [], [], []
    for i in range(time_steps, len(df)):
        seq_tech  = arr_tech[i-time_steps:i]
        seq_macro = arr_macro[i-time_steps:i]
        label     = y_all[i]
        # skip if any missing values
        if np.isnan(seq_tech).any() or np.isnan(seq_macro).any():
            continue
        X_tech.append(seq_tech)
        X_macro.append(seq_macro)
        y.append(label)

    return np.array(X_tech), np.array(X_macro), np.array(y)


def scale_features(X_train, X_test):
    """
    Fit a scaler on flattened samples per feature, then transform back to sequences.
    """
    n_train, t, f = X_train.shape
    n_test  = X_test.shape[0]

    flat_train = X_train.reshape(-1, f)
    flat_test  = X_test.reshape(-1, f)

    scaler = StandardScaler()
    scaler.fit(flat_train)
    scaled_train = scaler.transform(flat_train).reshape(n_train, t, f)
    scaled_test  = scaler.transform(flat_test).reshape(n_test, t, f)

    return scaled_train, scaled_test


def build_multi_input_lstm(time_steps, n_tech, n_macro):
    """
    Two-branch LSTM: one for technical indicators, one for macro data.
    """
    tech_in   = Input(shape=(time_steps, n_tech),  name='tech_input')
    tech_out  = LSTM(64, name='tech_lstm')(tech_in)

    macro_in  = Input(shape=(time_steps, n_macro), name='macro_input')
    macro_out = LSTM(32 , name='macro_lstm')(macro_in)

    merged = Concatenate(name='concat')([tech_out, macro_out])
    x = Dropout(0.2, name='dropout')(merged)
    out = Dense(3, activation='softmax', name='output')(x)

    model = Model(inputs=[tech_in, macro_in], outputs=out)
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout, Concatenate
from tensorflow.keras.optimizers import Adam

def build_multi_input_5_layer_lstm(time_steps, n_tech, n_macro, learning_rate=0.001):
    # Technical branch
    tech_in = Input(shape=(time_steps, n_tech), name='tech_input')
    tech_lstm_1 = LSTM(128, return_sequences=True, name='tech_lstm_1')(tech_in)  # Layer 1
    tech_lstm_2 = LSTM(128, return_sequences=False, name='tech_lstm_2')(tech_lstm_1)  # Layer 2
    tech_dense = Dense(128, activation='relu', name='tech_dense')(tech_lstm_2)  # Layer 3
    tech_dropout = Dropout(0.5, name='tech_dropout')(tech_dense)  # Layer 4

    # Macro branch
    macro_in = Input(shape=(time_steps, n_macro), name='macro_input')
    macro_lstm_1 = LSTM(64, return_sequences=True, name='macro_lstm_1')(macro_in)  # Layer 1
    macro_lstm_2 = LSTM(64, return_sequences=False, name='macro_lstm_2')(macro_lstm_1)  # Layer 2
    macro_dense = Dense(64, activation='relu', name='macro_dense')(macro_lstm_2)  # Layer 3
    macro_dropout = Dropout(0.5, name='macro_dropout')(macro_dense)  # Layer 4

    # Merge branches
    merged = Concatenate(name='concat')([tech_dropout, macro_dropout])

    # Final output layer (3 classes)
    out = Dense(3, activation='softmax', name='output')(merged)  # Layer 5

    model = Model(inputs=[tech_in, macro_in], outputs=out)
    
    # Compile with manual learning rate
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def build_multi_input_stacked_lstm(time_steps, n_tech, n_macro):
    # Technical branch: stack two LSTM layers
    tech_in = Input(shape=(time_steps, n_tech), name='tech_input')
    tech_lstm_1 = LSTM(64, return_sequences=True, name='tech_lstm_1')(tech_in)
    tech_lstm_2 = LSTM(64, name='tech_lstm_2')(tech_lstm_1)

    # Macro branch: stack two LSTM layers
    macro_in = Input(shape=(time_steps, n_macro), name='macro_input')
    macro_lstm_1 = LSTM(32, return_sequences=True, name='macro_lstm_1')(macro_in)
    macro_lstm_2 = LSTM(32, name='macro_lstm_2')(macro_lstm_1)

    # Concatenate branches
    merged = Concatenate(name='concat')([tech_lstm_2, macro_lstm_2])
    x = Dropout(0.2, name='dropout')(merged)
    out = Dense(3, activation='softmax', name='output')(x)

    model = Model(inputs=[tech_in, macro_in], outputs=out)
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import plotly.graph_objects as go

def plot_trading_predictions_interactive(df, y_true, y_pred, price_col='close', time_col=None):
    if time_col and time_col in df.columns:
        df = df.set_index(time_col)
    
    fig = go.Figure()
    
    # Price line
    fig.add_trace(go.Scatter(
        x=df.index, y=df[price_col], mode='lines', name='Price', line=dict(color='black')))
    
    # Buy signals (predicted up)
    up_idx = (y_pred == 2)
    fig.add_trace(go.Scatter(
        x=df.index[up_idx], y=df[price_col].iloc[up_idx], mode='markers',
        marker=dict(symbol='triangle-up', color='green', size=10), name='Predicted Up (Buy)'))
    
    # Sell signals (predicted down)
    down_idx = (y_pred == 1)
    fig.add_trace(go.Scatter(
        x=df.index[down_idx], y=df[price_col].iloc[down_idx], mode='markers',
        marker=dict(symbol='triangle-down', color='red', size=10), name='Predicted Down (Sell)'))
    
    # Neutral signals
    neutral_idx = (y_pred == 0)
    fig.add_trace(go.Scatter(
        x=df.index[neutral_idx], y=df[price_col].iloc[neutral_idx], mode='markers',
        marker=dict(symbol='circle', color='gray', size=6), name='Predicted Neutral (Hold)'))
    
    # Correct predictions highlighted
    correct_idx = (y_true == y_pred)
    fig.add_trace(go.Scatter(
        x=df.index[correct_idx], y=df[price_col].iloc[correct_idx], mode='markers',
        marker=dict(symbol='circle-open', color='blue', size=14), name='Correct Prediction'))
    
    fig.update_layout(title='Trading View Style Interactive Predictions',
                      xaxis_title='Time',
                      yaxis_title='Price',
                      hovermode='x unified')
    
    # fig.show()
    
    # To save as HTML file:
    fig.write_html('trading_predictions.html')


def main():
    # Path to merged Forex+macro file
    merged_path = './data/forex_with_all_macros.xlsx'
    df = pd.read_excel(merged_path, parse_dates=['time']).set_index('time')

    # 1) Technical indicators
    df = calculate_technical_indicators(df)
    df.to_excel('./indicator_data.xlsx', index=True)
    print("indicator data done")


    # 2) Macro surprises & lag windows (no fill/shift required)
    macro_cols = [
        'CPI_Actual', 'CPI_Forecast', 'CPI_Previous',
        'GDP_Actual', 'GDP_Forecast', 'GDP_Previous',
        'Interest_Rate_Actual', 'Interest_Rate_Forecast', 'Interest_Rate_Previous',
        'PCE_Actual', 'PCE_Forecast', 'PCE_Previous',
        'PPI_Actual', 'PPI_Forecast', 'PPI_Previous'
    ]
    df = process_macro_data(df, macro_cols, window=3)

    # 3) Label target
    df = label_data(df)
    df.to_excel('./labeld_data_all_macros.xlsx', index=False)

    # Features
    tech_features   = ['open','high','low','close','tick_volume',
                        'MA_50','MA_200','MACD','RSI_14',
                        'BB_upper','BB_lower']
    # tech_features   = ['open','high','low','close','tick_volume',
    #                     'MA_10','MACD','Momentum_4','ROC_2','RSI_14',
    #                     'BB_upper','BB_lower','CCI_20']



    # All raw macro cols + computed surprise and their lags
    macro_features  = macro_cols + [c for c in df.columns if 'Surprise' in c]

    time_steps = 30
    X_tech, X_macro, y = create_sequences(df, tech_features,
                                         macro_features, 'label', time_steps)

    # Split
    split_idx = int(0.8 * len(X_tech))
    X_tr_tech, X_te_tech = X_tech[:split_idx], X_tech[split_idx:]
    X_tr_macro, X_te_macro = X_macro[:split_idx], X_macro[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Scale
    X_tr_tech_s, X_te_tech_s = scale_features(X_tr_tech, X_te_tech)
    X_tr_macro_s, X_te_macro_s = scale_features(X_tr_macro, X_te_macro)

    # Build & train
    model = build_multi_input_5_layer_lstm(time_steps,
                                        len(tech_features),
                                        len(macro_features),
                                        learning_rate=0.0005)  # Set your desired LR here

    model.summary()

    es = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    rl = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3)

    history = model.fit(
        {'tech_input': X_tr_tech_s, 'macro_input': X_tr_macro_s}, y_train,
        validation_data=(
            {'tech_input': X_te_tech_s, 'macro_input': X_te_macro_s}, y_test
        ),
        epochs=50,
        batch_size=32,
        callbacks=[es, rl]
    )

    # Evaluate
    y_pred_prob = model.predict({'tech_input': X_te_tech_s,
                                 'macro_input': X_te_macro_s})
    y_pred = np.argmax(y_pred_prob, axis=1)

    # DEBUG: Print predicted and true class distribution
    print("Predicted class distribution:")
    unique, counts = np.unique(y_pred, return_counts=True)
    for cls, cnt in zip(unique, counts):
        print(f"Class {cls}: {cnt} samples")

    print("True class distribution:")
    unique_true, counts_true = np.unique(y_test, return_counts=True)
    for cls, cnt in zip(unique_true, counts_true):
        print(f"Class {cls}: {cnt} samples")

    print_classification_report(y_test, y_pred)
    prof_acc = profit_accuracy(y_test, y_pred)
    print(f"Profit Accuracy: {prof_acc:.4f}")
    plot_history(history)

    # Align df_test properly with y_test and y_pred (important for correct plotting)
    df_test = df.iloc[time_steps + split_idx : time_steps + split_idx + len(y_test)].copy()
    df_test.reset_index(inplace=True)  # reset index so plotting uses integer index or time column

    # DEBUG: check shapes alignment
    print(f"df_test shape: {df_test.shape}")
    print(f"y_test shape: {y_test.shape}")
    print(f"y_pred shape: {y_pred.shape}")

    # Plot interactive trading predictions
    plot_trading_predictions_interactive(df_test, y_test, y_pred, price_col='close', time_col='time')

if __name__ == "__main__":
    main()