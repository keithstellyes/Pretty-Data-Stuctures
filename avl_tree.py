from graphviz import Digraph
from graphviz_tree import i2b26

class AVLTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1
    def get_balance(self):
        return self.left_height - self.right_height
    def insert(self, value):
        if value < self.value:
            if self.left is None:
                self.left = AVLTree(value)
            else:
                self.left = self.left.insert(value)
        elif value > self.value:
            if self.right is None:
                self.right = AVLTree(value)
            else:
                self.right = self.right.insert(value)
        else:
            return self
        self.height = 1 + max(self.left_height, self.right_height)
        balance = self.balance
        # LEFT LEFT 
        if balance > 1 and value < self.left.value:
            print('//LEFT LEFT')
            return self.right_rotate()
        # RIGHT RIGHT
        if balance < -1 and value > self.right.value:
            print('//RIGHT RIGHT')
            return self.left_rotate()
        # LEFT RIGHT
        if balance > 1 and value > self.left.value:
            print('//LEFT RIGHT')
            self.left = self.left.left_rotate()
            return self.right_rotate()
        # RIGHT LEFT
        if balance < -1 and value < self.right.value:
            print('//RIGHT LEFT')
            self.right = self.right.right_rotate()
            # I spent 30 MINUTES debugging only to realize I had had this
            # original faulty line, and thus I will leave it here, as a
            # reminder that sometimes your mistake is a simple one:
            # 
            #return self.left.left_rotate()
            return self.left_rotate()
        return self
    def get_left_height(self):
        if self.left is None:
            return 0
        return self.left.height
    def get_right_height(self):
        if self.right is None:
            return 0
        return self.right.height
    def left_rotate(self):
        y = self.right
        new_tree = y.left
        y.left = self
        self.right = new_tree
        self.height = 1 + max(self.left_height, self.right_height)
        y.height =    1 + max(y.left_height, y.right_height)
        return y
    def right_rotate(self):
        y = self.left
        new_tree = y.right
        y.right = self
        self.left = new_tree
        self.height = 1 + max(self.left_height, self.right_height)
        y.height =    1 + max(y.left_height, y.right_height)
        return y
    balance = property(get_balance, None)
    left_height = property(get_left_height, None)
    right_height = property(get_right_height, None)
    def gv_serialize(self, t=None):
        if t is None:
            t = Digraph()
        t.node(str(id(self)), self.value)
        if self.left is not None:
            t.edge(str(id(self)), str(id(self.left)))
            self.left.gv_serialize(t)
        if self.right is not None:
            t.edge(str(id(self)), str(id(self.right)))
            self.right.gv_serialize(t)
        return t.source
