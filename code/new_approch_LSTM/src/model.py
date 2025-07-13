import tensorflow as tf
from tensorflow.keras import layers, models

# Module-level function for custom_objects

def sum_time(inputs):
    """
    Custom function for Lambda layer: sum over time axis.
    """
    return tf.reduce_sum(inputs, axis=1)


def lstm_attention_model(
    window: int, feature_dim: int,
    lstm_units=64, dropout=0.2
) -> tf.keras.Model:
    """
    Bidirectional LSTM + attention + dense head.
    """
    inp = layers.Input(shape=(window, feature_dim))

    # 1D-CNN pre-block
    x = layers.Conv1D(32, 3, padding='same', activation='relu')(inp)
    x = layers.MaxPooling1D(2)(x)

    # Bi-LSTM
    x = layers.Bidirectional(
        layers.LSTM(lstm_units, return_sequences=True)
    )(x)
    x = layers.Dropout(dropout)(x)

    # Attention
    scores = layers.Dense(1, activation='tanh')(x)               # [batch, time, 1]
    weights = layers.Softmax(axis=1)(scores)                     # normalize
    context_mul = layers.Multiply()([x, weights])               # apply weights
    context = layers.Lambda(sum_time, output_shape=lambda shp: (shp[0], shp[2]))(context_mul)

    # Dense head
    x = layers.Dense(32, activation='relu')(context)
    x = layers.Dropout(dropout)(x)
    out = layers.Dense(1, activation='sigmoid')(x)

    model = models.Model(inputs=inp, outputs=out)
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return model