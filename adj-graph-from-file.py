# generates an adjacency graph from a text file

from graphviz_tree import *
import sys, string

table = str.maketrans({key: None for key in string.punctuation})

fin = open(sys.argv[1], 'r')
lines = fin.readlines()
fin.close()

last_word = None
gvt = GraphVizTree()

label_edge_opts = ['false', 'b10', 'b16']
label_edges = 'false'
label_edge_ctr = 0

if len(sys.argv) > 2:
    sys.argv[2] = sys.argv[2].lower()
    if sys.argv[2] not in label_edge_opts:
        raise Exception('Invalid label edge option: %s' % sys.argv[2])
    label_edges = sys.argv[2]

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
        if label_edges == 'false':
            gvt.add_edge(nodes=[last_word, word], directed=True)
        elif label_edges == 'b10':
            gvt.add_edge(nodes=[last_word, word], directed=True, 
                         label=str(label_edge_ctr))
            label_edge_ctr += 1
        elif label_edges == 'b16':
            gvt.add_edge(nodes=[last_word, word], directed=True,
                         label=str(label_edge_ctr))
            label_edge_ctr += 1
        last_word = word

print(gvt.gv_serialize())
