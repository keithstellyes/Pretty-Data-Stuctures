import sys
from hash_table import *
from common import *
import string

f = open(sys.argv[1], 'r')
t = HashTable(max_load_factor=2/3, hash_function=djb2_hash)

table = str.maketrans({key: None for key in string.punctuation})

words = file_to_words(f)
[t.insert(word) for word in words]

for b in t.buckets:
    for e in b:
        if e.value is not None:
            print('//', e.value)
            print('//[next]', e.next)
            if e.next is not None:
                print('//[next:value]', e.next.value)
print(t.gv_serialize())
