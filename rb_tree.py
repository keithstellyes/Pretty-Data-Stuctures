from graphviz import Digraph
from graphviz_tree import i2b26

RED = 'RED'
BLACK = 'BLACK'

class RBTree:
    def __init__(self, value, color=BLACK, parent=None):
        if color not in (RED, BLACK):
            raise Exception('Color must be one of:' + str((RED,BLACK)))
        self.value = value
        self.color = color
        self._parent = parent
        self._left = None
        self._right = None
    def is_root(self):
        return self.parent is None
    def get_parent(self):
        return self._parent
    def set_parent(self, parent):
        self._parent = parent
    def get_grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent
    def get_root(self):
        if self.parent is None:
            return self
        return self.parent.root
    def get_left(self):
        return self._left
    def get_right(self):
        return self._right
    def set_left(self, left):
        self._left = left
        left.parent = self
    def set_right(self, right):
        self._right = right
        right.parent = self
    def get_uncle(self):
        if self.grandparent is None:
            return None
        p = self.parent
        if p.parent.left == p:
            return p.parent.right
        else:
            return p.parent.left
    parent = property(get_parent, set_parent)
    grandparent = property(get_grandparent, None)
    root = property(get_root, None)
    left = property(get_left, set_left)
    right = property(get_right, set_right)

    def insert(self, value):
        n = RBTree(value=value, color=RED)
        self.insert_recursive(n)
        n.repair_tree()
        return self.root
    def insert_recursive(self, n):
        t = self
        if t is not None and n.value < t.value:
            if t.left is None:
                t.left = n
            else:
                t.left.insert_recursive(n)
        elif t is not None and n.value > t.value:
            if t.right is None:
                t.right = n
            else:
                t.right.insert_recursive(n)

    def repair_tree(self):
        if self.is_root():
            self._case1()
            print('//case1')
        elif self.parent.color == BLACK:
            self._case2()
            print('//case2')
        elif self.get_uncle() is not None and self.get_uncle().color == RED:
            print('// case 3!')
            self._case3()
        else:
            self._case4()
    # self is root of tree, so we must update it
    def _case1(self):
        if self.parent is None:
            self.color = BLACK
    # The parent is black, and we are red, so it's valid
    def _case2(self):
        return
    def _case3(self):
        self.parent.color = BLACK
        self.get_uncle().color = BLACK
        self.grandparent.color = RED
        self.grandparent.repair_tree()
    def _case4(self):
        if self.parent is None:
            return
        if self.grandparent is None:
            return
        n = None
        if self.grandparent.left is not None and self == self.grandparent.left.right:
            self.parent.rotate_left()
            n = self.left
        elif self.grandparent.right is not None and self == self.grandparent.right.left:
            self.parent.rotate_right()
            n = self.right
        else:
            return
        if n is None:
            return
        # step2
        if n == n.parent.left:
            n.grandparent.rotate_right()
        else:
            n.grandparent.rotate_left()
        n.parent.color = BLACK
        n.grandparent.color = RED
    def rotate_left(self):
        n = self.right
        if n is None or (n.left is None and n.right is None):
            return
        self.right = n.left
        n.left = self
        n.parent = self.parent
        self.parent = n
    def rotate_right(self):
        n = self.left
        if n is None or (n.left is None and n.right is None):
            return
        self.left = n.right
        n.right = self
        n.parent = self.parent
        self.parent = n
    def gv_serialize(self, t=None):
        if t is None:
            t = Digraph()
        t.node(i2b26(id(self)), str(self.value), color=self.color)
        if self.parent is not None:
            t.edge(i2b26(id(self.parent)), i2b26(id(self)))
        if self.left is not None:
            self.left.gv_serialize(t)
        if self.right is not None:
            self.right.gv_serialize(t)
        return t.source
