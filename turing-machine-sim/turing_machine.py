import yaml
from graphviz import Digraph

class TuringMachine:
    def __init__(self, init, accept, reject, alphabet, states, \
                 state_transitions):
        self.init = init
        self.accept = accept
        self.reject = reject
        self.alphabet = alphabet
        self.state_transitions = state_transitions
        self.default_letter = alphabet[len(alphabet)-1]
        self.state = init
        self.states = states
        self.ftable = functional_statetrans_table(state_transitions)

    def run_input(self, t, monitor_function=None):
        t = TuringMachineTape(iterable=t, default_letter=self.default_letter)
        self.state = self.init
        # in case someone wants to use this later :)
        self.tape = t
        while True:
            if monitor_function is not None:
                monitor_function(self)
            if self.state in self.accept:
                return True
            if self.state in self.reject:
                return False
            self.state = self.ftable[self.state][t.read()](t=t, m=self)
        # safe if someone wants to peep
    def gv_serialize(self):
        dg = Digraph()
        for s in self.states:
            if s in self.accept:
                dg.node(str(s), color='green', shape='triangle')
            elif s in self.reject:
                dg.node(str(s), color='red', shape='triangle')
            else:
                dg.node(str(s))
        for t in self.state_transitions.keys():
            for dst in self.state_transitions[t]:
                label_parts = [str(dst['if'])]
                if dst['if'] == self.default_letter:
                    if 'BLANK' not in self.alphabet:
                        label_parts = ['{empty}']
                try:
                    if dst['wr'].strip() != '':
                        label_parts.append('WR({})'.format(str(dst['wr'])))
                except KeyError:
                    pass
                try:
                    label_parts.append(dst['tape'])
                except KeyError:
                    pass
                dg.edge(t, dst['to'], ';'.join(label_parts))
        return dg.source

class TuringMachineTape:
    def __init__(self, iterable, default_letter, head=0):
        self.d = {}
        self.default_letter = default_letter
        self.head = head
        index = 0
        for i in iterable:
            self.d[index] = i
            index += 1
    def __getitem__(self, key):
        if type(key) == slice:
            l = []
            r = None
            try:
                r = range(key.start, key.stop, key.step)
            except TypeError:
                r = range(key.start, key.stop)
            for i in r:
                l.append(self[i])
            return l
        if type(key) != int:
            raise TypeError('TuringMachineTape can only be indexed with int')
        try:
            return self.d[key]
        except KeyError:
            self.d[key] = self.default_letter
            return self.default_letter
    def __setitem__(self, key, value):
        if type(key) != int:
            raise TypeError('TuringMachineTape can only be indexed with int')
        self.d[key] = str(value)
    def right(self):
        self.head = self.head + 1
    def left(self):
        self.head = self.head - 1
    def write(self, value):
        self[self.head] = value
    def read(self):
        return self[self.head]

# a lambda of form: (machine, tape)
def build_trans_lambda(to_state, wr=None, tape_move=None):
    move_functions = {'left':lambda t:t.left(),
                      'right':lambda t: t.right(),
                      None: lambda t: None}
    move_function = move_functions[tape_move]
    write_function = lambda t: None
    if wr is not None:
        wr = str(wr)
        write_function = lambda t: t.write(wr)
    return lambda m, t: (to_state, write_function(t), move_function(t))[0]

def functional_statetrans_table(state_trans):
    states = {}
    for state in state_trans.keys():
        states[state] = {}
        for t in state_trans[state]:
            headval = str(t['if'])
            wr = None
            tape_move = None
            to_state = t['to']
            try:
                wr = t['wr']
            except KeyError:
                pass
            try:
                tape_move = t['tape'].lower()
            except KeyError:
                pass
            states[state][headval] = build_trans_lambda(to_state=to_state,
                                                        wr=wr, 
                                                        tape_move=tape_move)
    return states
# a state-transition table for running should be:
# STATE : { ON-TAPE0:ON-TAPE0FUNCT, ...
def load(fp):
    d = yaml.load(fp)
    init = str(d['init'])
    accept = [str(el) for el in d['accept'].split(' ')]
    reject = [str(el) for el in d['reject'].split(' ')]
    alphabet = [str(l) for l in d['alphabet']]
    states = []
    state_trans = {}
    for k in d.keys():
        if k not in ('init', 'accept', 'reject', 'alphabet'):
            states.append(k)
            state_trans[k] = d[k]
    for k in accept + reject:
        if k not in states:
            states.append(k)
    return TuringMachine(init=init, accept=accept, reject=reject, 
                         alphabet=alphabet, states=states,
                         state_transitions=state_trans)
