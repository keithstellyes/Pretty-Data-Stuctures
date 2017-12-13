import sys
from radixtree import *
import string

f = open(sys.argv[1], 'r')
t = RadixTree()

table = str.maketrans({key: None for key in string.punctuation})
word_count = 0

for line in f:
    if line.strip() == '':
        continue
    words = line.split(' ')
    for word in words:
        word = word.translate(table)
        word = word.upper()
        if word.strip() == '':
            continue
        t.add_string(word.strip())
        word_count += 1
print(t.gv_serialize())
print('// word count: {}'.format(str(word_count)))
