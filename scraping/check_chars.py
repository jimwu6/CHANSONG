path_to_file = "./DS_2.txt"
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

# CHECK TEXT
print('Length of text: {} characters'.format(len(text)))

# CHECK UNIQUE CHARS
vocab = sorted(set(text))
print('{} unique characters'.format(len(vocab)))
print(vocab)
