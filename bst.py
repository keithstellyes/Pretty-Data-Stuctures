from graphviz_tree import *

class BST:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = None
        self.right = None
    def has_value(self, value):
        if self.value == value:
            return True
        if self.value > value:
            if self.left is None:
                return False
            return self.left.has_value(value)
        if self.right is None:
            return False
        return self.right.has_value(value)
    def insert(self, value):
        if self.value is None:
            self.value = value
        if self.value == value:
            return
        elif self.value > value:
            if self.left is None:
                self.left = BST(value=value)
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.right = BST(value=value)
            else:
                self.right.insert(value)
    def gv_serialize(self):
        gvt = GraphVizTree()
        self._gvs(gvt)
        return gvt.gv_serialize()
    def _gvs(self, gvt):
        label = ''
        if self.value is not None:
            label = str(self.value)
        n = gvt.add_node(label=label)
        if self.left is not None:
            gvt.add_edge(nodes=[n, self.left._gvs(gvt)],
                         directed=True)
        if self.right is not None:
            gvt.add_edge(nodes=[n, self.right._gvs(gvt)],
                         directed=True)
        return n 
