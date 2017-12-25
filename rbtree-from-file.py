import sys
from rb_tree import RBTree
from common import *
import string

f = open(sys.argv[1], 'r')

table = str.maketrans({key: None for key in string.punctuation})

words = file_to_words(f)
t = RBTree(words[0])
words = words[1:]
#for word in words:
#    t = t.insert(word)

#print(t.gv_serialize())

i = 0
f = open(str(i) + '.dot', 'w')
f.write(t.gv_serialize())
f.close()
i += 1
for word in words:
    t.insert(word)
    f = open(str(i) + '.dot', 'w')
    i += 1
    f.write(t.gv_serialize())
    f.close()
def print_t_colors(t):
    print('//', t.color, str(t.value))
    if t.left is not None:
        print_t_colors(t.left)
    if t.right is not None:
        print_t_colors(t.right)

print_t_colors(t)
