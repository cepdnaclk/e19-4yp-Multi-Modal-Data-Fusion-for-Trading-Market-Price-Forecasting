import tensorflow as tf
from tensorflow.keras import layers, models, regularizers
from tensorflow.keras.utils import register_keras_serializable

@register_keras_serializable(package='Custom', name='sum_time')
def sum_time(inputs):
    """
    Custom Lambda function: sum over time axis.
    Registered for model serialization.
    """
    return tf.reduce_sum(inputs, axis=1)


def build_event_model(
    lookback: int,
    feat_dim: int,
    lstm_units: int = 64,
    dropout: float = 0.3,
    l2_reg: float = 1e-4
) -> tf.keras.Model:
    """
    Build an LSTM + attention model for event-based inputs.
    """
    inp = layers.Input(shape=(lookback, feat_dim))
    x = layers.GaussianNoise(0.01)(inp)

    x = layers.Conv1D(
        filters=32,
        kernel_size=3,
        padding='same',
        activation='relu',
        kernel_regularizer=regularizers.l2(l2_reg)
    )(x)
    x = layers.SpatialDropout1D(rate=0.2)(x)

    x = layers.Bidirectional(
        layers.LSTM(
            units=lstm_units,
            return_sequences=True,
            kernel_regularizer=regularizers.l2(l2_reg)
        )
    )(x)
    x = layers.LayerNormalization()(x)

    scores = layers.Dense(1, activation='tanh')(x)
    weights = layers.Softmax(axis=1)(scores)
    context = layers.Lambda(
        sum_time,
        output_shape=lambda s: (s[0], s[2])
    )(layers.Multiply()([x, weights]))

    h = layers.Dense(
        units=32,
        activation='relu',
        kernel_regularizer=regularizers.l2(l2_reg)
    )(context)
    h = layers.Dropout(rate=dropout)(h)
    out = layers.Dense(units=1, activation='sigmoid')(h)

    model = models.Model(inputs=inp, outputs=out)
    return model

if __name__ == '__main__':
    m = build_event_model(50, 7)
    m.summary()
