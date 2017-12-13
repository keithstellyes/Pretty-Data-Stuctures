import sys
from trie import Trie
import string

f = open(sys.argv[1], 'r')
t = Trie()

table = str.maketrans({key: None for key in string.punctuation})

for line in f:
    if line.strip() == '':
        continue
    words = line.split(' ')
    for word in words:
        word = word.translate(table)
        word = word.upper()
        if word.strip() == '':
            continue
        t.add_string(word)
print(t.gv_serialize())
