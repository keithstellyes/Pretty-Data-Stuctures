#https://www.reddit.com/r/dailyprogrammer/comments/3z1cxs/20160101_challenge_247_hard_zombies_on_the/ 
import math, os, sys
from graphviz_tree import *

BLAST = -1

def graph_edge_len(graph, n0, n1):
    for edge in graph:
        if edge[0] == n0 and edge[1] == n1:
            if edge[2] == BLAST:
                return 0
            return edge[2]
        if edge[1] == n0 and edge[0] == n1:
            if edge[2] == BLAST:
                return 0
            return edge[2]

    raise Exception('Distance between {} and {} not found'.format(str(n0),
                                                                str(n1)))
def graph_target(graph):
    mx = graph[0][0]
    for e in graph[1:]:
        if e[0] > mx:
            mx = e[0]
        if e[1] > mx:
            mx = e[1]
    return mx

# a list of edges in format (node0, node1, distance)
# returns (set of (from, to), total)
def dijkstra(graph):
    UNDEFINED = -3
    q = {}
    dist = {}
    prev = {}
    for i in range(graph_target(graph) + 1):
        dist[i] = math.inf
        prev[i] = UNDEFINED
        q[i] = None
    dist[0] = 0

    while len(q.keys()) > 0:
        # get u
        u = None
        u_min = math.inf
        # compute 'u'
        for v in q.keys():
            if u is None:
                u = v
                u_min = math.inf
            else:
                other = dist[v]
                if other == BLAST:
                    other = 0
                if other < u_min:
                    u = v
                    u_min = other
        del q[u]
        # get neighbor vertices
        neighbors = []
        for e in graph:
            if e[0] == u:
                neighbors.append(e[1])
            elif e[1] == u:
                neighbors.append(e[0])
        for v in neighbors:
            alt = dist[u] + graph_edge_len(graph, u, v)
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    # getting the actual path
    p = []
    target = graph_target(graph)
    while prev[target] != UNDEFINED:
        p.insert(0, target)
        target = prev[target]
    p.insert(0, 0)
    zombies_killed = 0
    for i in range(0, len(p) - 1):
        zombies_killed += graph_edge_len(graph, p[i], p[i+1])
    return (p, zombies_killed)

fin = open(sys.argv[1], 'r')
s = fin.read()
tuples = []

# used as magic number to mark where a BLAST has been used
BLAST = -1

curr_tuple = ''
i = 0

while i < len(s):
    if s[i] == '(':
        i += 1
        while i < len(s) and s[i] != ')':
            curr_tuple += s[i]
            i += 1
        i += 1
        curr_tuple = curr_tuple.split(',')
        tuples.append((int(curr_tuple[0]),
                       int(curr_tuple[1]),
                       int(curr_tuple[2])))
        curr_tuple = ''
    elif s[i] == ',' or s[i].strip() == '':
        pass
    else:
        raise Exception('Parse error, unexpected char: %s' % s[i])
    i += 1
fin.close()

gvt = GraphVizTree()
fmap = open('map.dot', 'w')

added_nodes = ()
for t in tuples:
    n0 = 'n' + str(t[0])
    n1 = 'n' + str(t[1])
    if n0 not in added_nodes:
        gvt.add_node(name=n0, label=str(t[0]))
    if n1 not in added_nodes:
        gvt.add_node(name=n1, label=str(t[1]))
    added_nodes += (n0, n1)
    gvt.add_edge(nodes=[n0, n1], label=str(t[2]))
fmap.write(gvt.gv_serialize())
fmap.close()

print('Generating graphviz of map')
p = os.popen('dot map.dot -T png -o map.png')
p.close()

possible_paths = []

for i in range(len(tuples)):
    path = tuples[:i] + [(tuples[i][0], tuples[i][1], BLAST)] + tuples[i+1:]
    possible_paths.append(path)

print('Trying all the possible places we can use BLAST and find', end='')
print(' the minimal zombies encountered with each possible BLAST spot')
# for each possible path, find its shortest path, then min over it all
min_path_size = math.inf
min_path = []
min_graph = []
for p in possible_paths:
    optimal_path = dijkstra(p)
    if optimal_path[1] < min_path_size:
        min_path_size = optimal_path[1]
        min_path = optimal_path[0]
        min_graph = p

foptimal = open('optimalpath.dot', 'w')

gvt = GraphVizTree()
print(min_path)
for edge in min_graph:
    color = 'black'
    label = edge[2]
    if edge[2] == BLAST:
        label = 'BLAST'
    for i in range(len(min_path) - 1):
        mp = min_path[i:i+2]
        if edge[0] == mp[0] and edge[1] == mp[1]:
            color = 'red'
        elif edge[0] == mp[1] and edge[1] == mp[0]:
            color = 'red'
    gvt.add_edge(nodes=[str(edge[0]), str(edge[1])], label=label, color=color)

foptimal.write(gvt.gv_serialize())
foptimal.close()

print('Generating graphviz of optimal path')
p = os.popen('dot optimalpath.dot -T png -o optimalpath.png')
