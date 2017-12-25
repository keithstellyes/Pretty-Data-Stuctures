import random
from graphviz_tree import *

# Where entries is a finite iterable
# Example input and output:
# [A, A, B] =>
# {
#   A: { A:1 , B:1 }
#   B: { }
# }
# g can be passed to update it
def build_freqtable(entries, g={}):
    entries = [e for e in entries]
    last_entry = entries[0]
    entries = entries[1:]
    for e in entries:
        if last_entry not in g.keys():
            g[last_entry] = {e:1}
            last_entry = e
            continue
        gle = g[last_entry]
        if e not in gle.keys():
            gle[e] = 1
        else:
            gle[e] = gle[e] + 1
        last_entry = e
    return g

# exactly like above, but into ratios
def freqtable2ratiotable(freqtable):
    g = freqtable.copy()
    for s in freqtable.keys():
        g[s] = g[s].copy()
        transitions = [t for t in g[s].keys()]
        if transitions == []:
            continue
        trans_sum = sum([freqtable[s][t] for t in transitions])
        for t in transitions:
            g[s][t] = freqtable[s][t] / trans_sum
    return g

# each value is its probability
# a series of ranges for each item,
# an item is returned if the value is >= its min, and < than its max
def roulette_maker(items):
    def in_range(n, r):
        return r[0] <= n and n < r[1]
    def get_range(n, r):
        for sr in r:
            if in_range(n, sr):
                return sr
        raise Exception('Range not found')

    s = sum([items[k] for k in items.keys()])
    m = 0
    ranges = []
    for i in items.keys():
        ranges.append((m, m+items[i], i))
        m = m + items[i]
    return lambda: get_range(random.uniform(0, s), ranges)[2]

# from a ratiotable, each state gets a functor that returns a new state
def roulette_machine(ratiotable):
    g = {}
    for s in ratiotable:
        g[s] = roulette_maker(ratiotable[s])
    return g

class MarkovChain:
    LIMIT = 5
    # either generate a frequency table, or take in an override
    # iterable is not looked at if a freqtable is passed
    def __init__(self, iterable, seed=None, initstate=None, freqtable=None):
        if freqtable is None:
            self.freqtable = build_freqtable(iterable)
        else:
            self.freqtable = freqtable
        self.ratiotable = freqtable2ratiotable(self.freqtable)
        self._roulette_machine = roulette_machine(self.ratiotable)
        self.seed = random.seed(seed)
        if initstate is None:
            self.currstate = self.random_state()
        else:
            self.currstate = initstate

    def random_state(self):
        return random.choice([k for k in self.freqtable.keys()])

    def next(self, state=None, depth=0):
        if depth == MarkovChain.LIMIT:
            print("WARN: couldn't build transition so used random state")
            self.currstate = self.random_state()
            return self.currstate
        if state is not None:
            try:
                self._roulette_machine[state]
            except KeyError:
                return self.next(state=self.random_state(), depth=depth+1)
            ret = self._roulette_machine[state]()
            try:
                self._roulette_machine[ret]
            except KeyError:
                return self.next(state=self.random_state(), depth=depth+1)
            self.currstate = self._roulette_machine[ret]()
            return ret
        ret = self.currstate
        try:
            self.currstate = self._roulette_machine[self.currstate]()
        except KeyError:
            self.currstate = self.random_state()
        return ret

    def gv_serialize(self):
        gvt = GraphVizTree()
        nodes = {}
        ratiotable = self.ratiotable
        for n in ratiotable.keys():
            if n not in nodes.keys():
                nodes[n] = gvt.add_node(label=n)
            for nn in ratiotable[n]:
                if nn not in nodes:
                    nodes[nn] = gvt.add_node(label=nn)
                gvt.add_edge(nodes=[nodes[n], nodes[nn]], 
                             label=str(round(ratiotable[n][nn], 2)),
                             directed=True)
        return gvt.gv_serialize()

if __name__ == '__main__':
    #t = build_freqtable('AAAB')
    #rt = freqtable2ratiotable(t)
    c = MarkovChain('AAAB')
    print(c.gv_serialize())
    for i in range(100):
        print(c.next(), end='')
    print()
