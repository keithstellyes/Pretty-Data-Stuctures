import sys
from radixtree import *
from common import *
import string

f = open(sys.argv[1], 'r')
t = RadixTree()

words = file_to_words(f)
[t.add_string(word) for word in words]

print(t.gv_serialize())
