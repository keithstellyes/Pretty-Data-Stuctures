# generates an adjacency graph from a text file

from graphviz_tree import *
import sys, string

table = str.maketrans({key: None for key in string.punctuation})

fin = open(sys.argv[1], 'r')
lines = fin.readlines()
fin.close()

gvt = GraphVizTree()

label_edge_opts = ['false', 'b10', 'b16']
label_edges = 'false'
label_edge_ctr = 0

if len(sys.argv) > 2:
    sys.argv[2] = sys.argv[2].lower()
    if sys.argv[2] not in label_edge_opts:
        raise Exception('Invalid label edge option: %s' % sys.argv[2])
    label_edges = sys.argv[2]

words = file_to_words(fin)
last_word = words[0]
words = words[1:]

for word in words:
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
