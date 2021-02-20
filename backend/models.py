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


class OneStep(keras.Model):
    def __init__(self, model, chars_from_ids, ids_from_chars, temperature=1):
        super().__init__()
        self.temperature = temperature
        self.model = model
        self.chars_from_ids = chars_from_ids
        self.ids_from_chars = ids_from_chars

        # Create mask to prevent "" and "[UNK]"
        skip_ids = self.ids_from_chars(['','[UNK]'])[:, None]
        sparse_mask = tf.SparseTensor(
            values = [-float('inf')] * len(skip_ids),
            indices = skip_ids,
            dense_shape = [len(ids_from_chars.get_vocabulary())]
        )
        self.prediction_mask = tf.sparse.to_dense(sparse_mask)

    @tf.function
    def generate_one_step(self, inputs, states=None):
        # Convert strings to tokens
        input_chars = tf.strings.unicode_split(inputs, 'UTF-8')
        input_ids = self.ids_from_chars(input_chars).to_tensor()
        # Run model
        if type(states) == type([]):
            predicted_logits, states = self.model(inputs=input_ids, states=states[:], return_state=True)
        else:
            predicted_logits, states = self.model(inputs=input_ids, states=states, return_state=True)

        # Only use the last prediction
        predicted_logits = predicted_logits[:, -1, :]
        predicted_logits = predicted_logits / self.temperature
        # Apply prediction mask
        predicted_logits = predicted_logits + self.prediction_mask

        # Generate IDs
        predicted_ids = tf.random.categorical(predicted_logits, num_samples=1)
        predicted_ids = tf.squeeze(predicted_ids, axis=-1)

        # Convert to chars
        predicted_chars = self.chars_from_ids(predicted_ids)

        # Return chars, model state
        return predicted_chars, states