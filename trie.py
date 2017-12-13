from graphviz_tree import *

class Trie:
    def __init__(self, leaf=False, value=''):
        self.children = {}
        self.leaf = leaf
        self.value = value
    def add_string(self, s):
        if len(s) == 0:
            self.leaf = True
        else:
            try:
                self.children[s[0]]
                if len(s) == 1:
                    self.children[s[0]].leaf = True
                else:
                    self.children[s[0]].add_string(s[1:])
            except KeyError:
                if len(s) == 1:
                    self.children[s[0]] = Trie(value=s[0], leaf=True)
                else:
                    self.children[s[0]] = Trie(value=s[0])
                    self.children[s[0]].add_string(s[1:])
    
    def gv_serialize(self):
        gvt = GraphVizTree()
        self._gvs(gvt)
        return gvt.gv_serialize()

    # returns its assigned GraphViz Node vlaue
    def _gvs(self, gvt):
        shape = None
        if self.leaf:
            shape = 'box'
        my_node = gvt.add_node(label=self.value, shape=shape)
        for child_key in self.children.keys():
            child_node = self.children[child_key]._gvs(gvt)
            gvt.add_edge([my_node, child_node], directed=True)
        return my_node
