import sys
from trie import Trie
from common import *
import string

f = open(sys.argv[1], 'r')
t = Trie()

table = str.maketrans({key: None for key in string.punctuation})

words = file_to_words(f)
[t.add_string(word) for word in words]

print(t.gv_serialize())
