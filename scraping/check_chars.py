path_to_file = "./DS_2.txt"
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

# CHECK TEXT
print('Length of text: {} characters'.format(len(text)))
#print(text[:1000])

# CHECK UNIQUE CHARS
vocab = sorted(set(text))
print('{} unique characters'.format(len(vocab)))
print(vocab)
# print(text.index(vocab[-1]))
# print(text[1572670:1572700])
print()