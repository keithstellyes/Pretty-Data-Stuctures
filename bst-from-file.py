import sys
from bst import BST
import string
from common import *

f = open(sys.argv[1], 'r')
t = BST()

table = str.maketrans({key: None for key in string.punctuation})

words = file_to_words(f)
[t.insert(w) for w in words]

print(t.gv_serialize())
