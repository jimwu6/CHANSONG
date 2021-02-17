import tensorflow as tf
from tensorflow import keras

class ModelOne(keras.Model):
    def __init__(self, vocab_size, embedding_dim, rnn_units):
        super().__init__(self)
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.gru = tf.keras.layers.GRU(rnn_units,
                                       return_sequences=True,
                                       return_state=True,
                                       )
        self.dense = tf.keras.layers.Dense(vocab_size)

    def call(self, inputs, states=None, return_state=False, training=False):
        x = inputs
        x = self.embedding(x, training=training)
        if states is None:
            states = self.gru.get_initial_state(x)
        x, states = self.gru(x, initial_state=states, training=training)
        x = self.dense(x, training=training)

        if return_state:
            return x, states
        else:
            return x


class ModelTwo(keras.Model):
    def __init__(self, vocab_size, embedding_dim, rnn_units):
        super().__init__(self)
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.gru_one = tf.keras.layers.GRU(rnn_units,
                                           return_sequences=True,
                                           return_state=True)
        self.gru_two = tf.keras.layers.GRU(rnn_units,
                                           return_sequences=True,
                                           return_state=True
                                           )
        self.dense = tf.keras.layers.Dense(vocab_size)

    def call(self, inputs, states=None, return_state=False, training=False):
        x = inputs
        x = self.embedding(x, training=training)
        if states is None:
            states = [self.gru_one.get_initial_state(x), self.gru_two.get_initial_state(x)]
        x, states[0] = self.gru_one(x, initial_state=states[0], training=training)
        x, states[1] = self.gru_two(x, initial_state=states[1], training=training)
        x = self.dense(x, training=training)

        if return_state:
            return x, states
        else:
            return x


class ModelThree(keras.Model):
    def __init__(self, vocab_size, embedding_dim, rnn_units):
        super().__init__(self)
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.lstm = tf.keras.layers.LSTM(rnn_units,
                                         return_sequences=True,
                                         return_state=True,
                                         )
        self.dense = tf.keras.layers.Dense(vocab_size)

    def call(self, inputs, states=None, return_state=False, training=False):
        x = inputs
        x = self.embedding(x, training=training)
        x, h, c = self.lstm(x, initial_state=states, training=training)
        states = [h, c]
        x = self.dense(x, training=training)

        if return_state:
            return x, states
        else:
            return x


class ModelFour(keras.Model):
    def __init__(self, vocab_size, embedding_dim, rnn_units):
        super().__init__(self)
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.lstm_one = tf.keras.layers.LSTM(rnn_units,
                                             return_sequences=True,
                                             return_state=True,
                                             )
        self.lstm_two = tf.keras.layers.LSTM(rnn_units,
                                             return_sequences=True,
                                             return_state=True,
                                             )
        self.dense = tf.keras.layers.Dense(vocab_size)

    def call(self, inputs, states=None, return_state=False, training=False):
        x = inputs
        x = self.embedding(x, training=training)
        if states is None:
            states = [None, None]
        x, h, c = self.lstm_one(x, initial_state=states[0], training=training)
        states[0] = [h, c]
        x, h, c = self.lstm_two(x, initial_state=states[1], training=training)
        states[1] = [h, c]
        x = self.dense(x, training=training)

        if return_state:
            return x, states
        else:
            return x


def get_model(model_num, vocab_size, embedding_dim, rnn_units):
    loss = tf.losses.SparseCategoricalCrossentropy(from_logits=True)

    if model_num == 1:
        model = ModelOne(vocab_size, embedding_dim, rnn_units)
    elif model_num == 2:
        model = ModelTwo(vocab_size, embedding_dim, rnn_units)
    elif model_num == 3:
        model = ModelThree(vocab_size, embedding_dim, rnn_units)
    else:
        model = ModelFour(vocab_size, embedding_dim, rnn_units)

    model.compile(optimizer='adam', loss=loss)

    return model
