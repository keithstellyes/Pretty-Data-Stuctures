from graphviz_tree import *

class RadixTree:
    def __init__(self, leaf=False, value=''):
        self.children = {}
        self.leaf = leaf
        self.value = value
    def add_string(self, s):
        if len(s) == 0:
            self.leaf = True
        else:
            for ck in self.children.keys():
                if ck == s:
                    self.children[ck].leaf = True
                    return
                elif s.startswith(ck):
                    print('//adding:' + s[len(ck):])
                    self.children[ck].add_string(s[len(ck):])
                    return
            # we can't progress further. Either:
            # A) we add this as a new node entirely
            # B) another string can be split up to be the prefix for this and
            #    that.
            for ck in self.children.keys():
                if ck[0] == s[0]:
                    # split up...
                    i = 0
                    while i < min(len(ck), len(s)):
                        if ck[i] != s[i]:
                            break
                        i += 1
                    # shared prefix of ck and s
                    pfix = ck[:i]
                    ck_sfix = ck[i:]
                    s_sfix = s[i:]
                    
                    # sometimes the new parent should be a leaf,
                    # and we must check for this, otherwise we fail cases
                    # like {orange, or} but pass {or, orange}
                    # basically, failing cases where a string that exists
                    # is a _prefix_ of the string trying to be added, s
                    np_isleaf = ck.startswith(s)
                    # whatever node ck was at, replace with this
                    new_parent = RadixTree(leaf=np_isleaf, value=pfix)

                    ck_node = self.children[ck]
                    ck_node.value = ck_sfix

                    s_node = RadixTree(leaf=True, value=s_sfix)

                    if ck_sfix != '':
                        new_parent.children[ck_sfix] = ck_node
                    if s_sfix != '':
                        new_parent.children[s_sfix] = s_node

                    del self.children[ck]
                    self.children[pfix] = new_parent
                    print('//' + str(self.children))
                    return
            self.children[s] = RadixTree(leaf=True, value=s)
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
