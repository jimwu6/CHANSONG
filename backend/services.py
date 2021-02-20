import json
import requests

import numpy as np
import os
import time

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

from . import models

path_to_file = "./DS_2.txt"
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

vocab = sorted(set(text))
VOCAB_SIZE = len(vocab)

# CHAR ENCODING TO ID
chars = tf.strings.unicode_split(text, input_encoding='UTF-8')
ids_from_chars = preprocessing.StringLookup(vocabulary=list(vocab))
ids = ids_from_chars(chars)

# INVERSION TO CHAR
chars_from_ids = preprocessing.StringLookup(vocabulary=ids_from_chars.get_vocabulary(), invert=True)

with open('./model_arch.json') as f:
    model_archs = json.load(f)

def text_from_ids(ids):
    return tf.strings.reduce_join(chars_from_ids(ids), axis=-1)

def generate_lyrics(model_name, temp, length, input_text):
    _, num, finetune = model_name.split("_")

    start_time = time.time()

    model_arch = model_archs["model_"+num]
    arch_num = model_arch['model_arch']
    rnn_units = model_arch['rnn_units']
    model = models.get_model(arch_num, len(ids_from_chars.get_vocabulary()), 256, rnn_units)

    checkpoint_dir = './models/model'+num
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_30")
    model.load_weights(checkpoint_prefix)
    one_step_model = models.OneStep(model, chars_from_ids, ids_from_chars, temp)

    states = None
    if arch_num == '2' or arch_num == '4':
        states = [None, None]

    next_char = tf.constant([input_text])
    result = [next_char]

    for n in range(length):
        next_char, states = one_step_model.generate_one_step(next_char, states=states)
        result.append(next_char)

    result = tf.strings.join(result)

    text = result[0].numpy().decode('utf-8')
    print(time.time()-start_time)
    return text
