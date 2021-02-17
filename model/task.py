import argparse
from . import models
import os
import tensorflow as tf
from tensorflow import keras
import numpy as np

from tensorflow.keras.layers.experimental import preprocessing


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--job-dir',
        type=str,
        required=False,  # CHANGE THIS TO TRUE WHEN USING
        help='local or GCS location for writing checkpoints and exporting models'
    )

    parser.add_argument(
        '--num-epochs',
        type=int,
        default=30,
        help='number of times to go through the data, default=30'
    )

    parser.add_argument(
        '--batch-size',
        type=int,
        default=64,
        help='number of sequences to use during each training step, default=64'
    )

    parser.add_argument(
        '--model-num',
        type=int,
        required=True,
        help='number of model to use to train'
    )

    parser.add_argument(
        '--rnn-units',
        type=int,
        default=1024,
        help='number of RNN units per layer, default=1024'
    )

    parser.add_argument(
        '--embedding-dim',
        type=int,
        default=256,
        help='size of embedding layer, default=256'
    )

    parser.add_argument(
        '--seq-len',
        type=int,
        default=200,
        help='length of each sequence, default=200'
    )

    parser.add_argument(
        '--dataset-num',
        type=int,
        required=True,
        help='number of dataset to use, from 1-2'
    )

    args, _ = parser.parse_known_args()
    return args


def train_and_eval(args):
    SEQ_LENGTH = args.seq_len
    BATCH_SIZE = args.batch_size
    BUFFER_SIZE = 10000

    EMBEDDING_DIM = args.embedding_dim
    RNN_UNITS = args.rnn_units

    EPOCHS = args.num_epochs

    # get the data file

    if args.dataset_num == 1:
        # dataset_file = args.job_dir + '/DS_1.txt'
        # dataset_file = 'https://console.cloud.google.com/storage/browser/rnn-genius-bucket-model16/DS_1.txt'
        dataset_file = tf.keras.utils.get_file('DS_1.txt',
                                               'https://storage.googleapis.com/rnn-genius-bucket-model16/DS_1.txt')
    else:
        # dataset_file = args.job_dir + '/DS_2.txt'
        dataset_file = tf.keras.utils.get_file('DS_2.txt',
                                               'https://storage.googleapis.com/rnn-genius-bucket-model16/DS_2.txt')

    text = open(dataset_file, 'rb').read().decode(encoding='utf-8')
    print(dataset_file)
    print('Length of text: {} characters'.format(len(text)))

    vocab = sorted(set(text))
    print('{} unique characters'.format(len(vocab)))
    print(vocab)

    VOCAB_SIZE = len(vocab)

    chars = tf.strings.unicode_split(text, input_encoding='UTF-8')
    ids_from_chars = preprocessing.StringLookup(vocabulary=list(vocab))
    ids = ids_from_chars(chars)

    chars_from_ids = preprocessing.StringLookup(vocabulary=ids_from_chars.get_vocabulary(), invert=True)

    def text_from_ids(ids):
        return tf.strings.reduce_join(chars_from_ids(ids), axis=-1)

    def split_input_target(sequence):
        input_text = sequence[:-1]
        target_text = sequence[1:]
        return input_text, target_text

    ids_dataset = tf.data.Dataset.from_tensor_slices(ids)
    sequences = ids_dataset.batch(SEQ_LENGTH + 1, drop_remainder=True)
    dataset = sequences.map(split_input_target)

    dataset = (
        dataset
        .shuffle(BUFFER_SIZE)
        .batch(BATCH_SIZE, drop_remainder=True)
        .prefetch(tf.data.experimental.AUTOTUNE))

    model = models.get_model(args.model_num,
                             vocab_size=len(ids_from_chars.get_vocabulary()),
                             embedding_dim=EMBEDDING_DIM,
                             rnn_units=RNN_UNITS)

    # checkpoint_dir = args.job_dir + '/training_checkpoints'
    checkpoint_dir = os.path.join(args.job_dir, 'training_checkpoints')
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")
    checkpoint_callback = keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_prefix,
        save_weights_only=True,
        save_freq=5 * (len(sequences) // BATCH_SIZE),
        verbose=1
    )  # save_freq for how many checkpoints (every 5 epochs)

    
    print("Fitting")
    history = model.fit(dataset, epochs=EPOCHS, callbacks=[checkpoint_callback])
    print(model.summary())
    loss_file = 'loss.txt'
    losses = history.history['loss']
    numpy_losses = np.array(losses)
    np.savetxt(loss_file, X=numpy_losses, delimiter=',')

    print('Completed')


if __name__ == '__main__':
    args = get_args()
    train_and_eval(args)
