import sys
from avl_tree import AVLTree
from common import *
import string

f = open(sys.argv[1], 'r')

table = str.maketrans({key: None for key in string.punctuation})

words = file_to_words(f)
t = AVLTree(words[0])
words = words[1:]

print('//', t.value)
for word in words:
    print('//', word)
    t = t.insert(word)
print(t.gv_serialize())
