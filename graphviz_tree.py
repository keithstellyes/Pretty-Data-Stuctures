from string import ascii_lowercase

# converts an integer to base 26 representation
def i2b26(i:int):
    if i < 26:
        return ascii_lowercase[i]
    else:
        return i2b26(i//26) + ascii_lowercase[i%26]

class GraphVizTree: 
    def __init__(self, name=''):
        self.output = 'digraph {}'.format(name) + '{\n'
        self.next_node = 0
        self.declarations = []
        self.edges = []

    # adds a node to this graph and returns the placed name
    def add_node(self, label, shape=None, name=None):
        node_name = None
        if name is None:
            node_name = i2b26(self.next_node)
            self.next_node += 1
        else:
            node_name = name
        label = label.replace('"', '\\"')
        out = '    {n} [label="{l}"'.format(n=node_name, l=label)
        if shape is not None:
            out += ', shape={}'.format(shape)
        self.declarations.append(out + '];')
        return node_name

    def add_edge(self, nodes, directed=False):
        line = None
        if directed:
            line = ' -> '
        else:
            line = ' -- '
        self.edges.append('    ' + line.join(nodes) + ';')

    def gv_serialize(self):
        return self.output + '\n'.join(self.declarations) + '\n' +\
                             '\n'.join(self.edges) + '\n}'
