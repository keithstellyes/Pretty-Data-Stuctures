from graphviz_tree import *

t = GraphVizTree()

for i in range(1, 5, 2):
    n0 = t.add_node(label=str(i))
    n1 = t.add_node(label=str(i+1))

    t.add_edge(nodes=[n0, n1], directed=True)

print(t.gv_serialize())
