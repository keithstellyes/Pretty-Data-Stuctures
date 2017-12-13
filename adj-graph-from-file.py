# generates an adjacency graph from a text file

from graphviz_tree import *
import sys, string

table = str.maketrans({key: None for key in string.punctuation})

fin = open(sys.argv[1], 'r')
lines = fin.readlines()
fin.close()

last_word = None
gvt = GraphVizTree()

for line in lines:
    line = line.strip()
    line = line.translate(table)
    words = line.split(' ')
    words = [w.upper().strip() for w in words]
    if last_word is None:
        last_word = words[0]
        words = words[1:]
    for word in words:
        if word.strip() == '':
            continue
        gvt.add_edge(nodes=[last_word, word], directed=True)
        last_word = word

print(gvt.gv_serialize())
