from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.utils import class_weight
import numpy as np

def build_lstm_model(time_steps, num_features):
    model = Sequential()
    model.add(LSTM(64, input_shape=(time_steps, num_features), return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def train_model(model, X_train, y_train, X_val, y_val, epochs=20, batch_size=32):
    from tensorflow.keras.utils import to_categorical

    # Compute class weights
    class_weights = class_weight.compute_class_weight(
        class_weight='balanced',
        classes=np.unique(y_train),
        y=y_train
    )
    class_weights = dict(enumerate(class_weights))

    y_train_cat = to_categorical(y_train, num_classes=3)
    y_val_cat = to_categorical(y_val, num_classes=3)

    history = model.fit(
        X_train, y_train_cat,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_val, y_val_cat),
        class_weight=class_weights
    )
    return history
