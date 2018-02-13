'''
Author: Keith Stellyes
2018

Does the following:

1. Read a regex from stdin
2. Compiles the regex to an NFA
3. Converts the NFA to a DFA
4. Generates a Verilog chip to out.v w/ testbench (reading from test-bench.v)
'''
from graphviz import Digraph

EPSILON = 'ε'
LITERAL = 'LITERAL'
CONCAT = 'CONCAT'
UNION = '|'
STAR = '*'

class FiniteAutomaton:
    def __init__(self):
        self.ctr = 0
        self.nodes = []
        self.transitions = {}
        self.accept_states = []

    def add_node(self, val=None):
        if val is None:
            val = self.ctr
            self.ctr += 1
        if val in self.nodes:
            return
        self.nodes.append(val)
        self.transitions[val] = []

        return val
    def add_transition(self, _from, to, on_val):
        if to not in self.nodes:
            raise Exception('Tried to target node not yet in added nodes')
        to_add = (to, on_val)
        if to_add in self.transitions[_from]:
            return
        self.transitions[_from].append(to_add)

    def is_final_accept_state(self, n):
        if n not in self.nodes:
            raise Exception('Tried to check if the node, {}, is final, but it\
                    it is not a recognized node.'.format(str(n)))
        return n in self.accept_states and \
                (self.transitions[n] is None or len(self.transitions[n]) == 0)

    def trans_strings(self, n):
        if n not in self.transitions.keys():
            return []
        return sorted([t[1] for t in self.transitions[n]])

    def copy_into(self, other):
        other.ctr = self.ctr
        other.nodes = self.nodes.copy()
        other.transitions = self.transitions.copy()
        other.accept_states = self.accept_states.copy()

    def add_accept_state(self, node):
        if node not in self.accept_states:
            self.accept_states.append(node)

    def distinguishable(self, a, b):
        return self.trans_strings(a) == self.trans_strings(b) and\
                a in self.accept_states == b in self.accept_states

    @property
    def get_alphabet(self):
        alphabet = set()
        for n in self.nodes:
            for t in self.transitions[n]:
                alphabet = alphabet | set(t[1])
        return alphabet

    def gv_serialize(self):
        g = Digraph()
        for n in self.nodes:
            if n not in self.accept_states:
                g.node(str(n), str(n))
            else:
                g.node(str(n), str(n), color='green', shape='doublecircle')
        for _from in self.transitions.keys():
            for to_tuple in self.transitions[_from]:
                to = str(to_tuple[0])
                transcond = str(to_tuple[1])
                g.edge(str(_from), to, label=transcond)
        return g.source

    def has_epsilon(self):
        for src in self.transitions.keys():
            for trans in self.transitions[src]:
                if trans[1] == EPSILON:
                    return True
        return False

    def epsilon_reachable(self, node, s=None):
        if s is None:
            s = tuple()
        for t in self.transitions[node]:
            if t[0] in s:
                continue
            if t[1] == EPSILON and t[0] not in s:
                s += (t[0],)
                s_to_add = self.epsilon_reachable(t[0], s)
                for el in s_to_add:
                    if el not in s:
                        s += (el,)
        return s
    
    def get_orphans(self):
        orphans = set(self.nodes) - set([0])
        for n in self.nodes:
            if n in self.transitions.keys():
                for t in self.transitions[n]:
                    orphans = orphans - set([t[0]])
        print('//orphans:', orphans)
        return orphans

    orphans = property(get_orphans, None)

    def kill_orphans(self):
        for orphan in self.orphans:
            del self.nodes[self.nodes.index(orphan)]

class Scanner:
    def __init__(self, string):
        self.string = string
        self.index = 0
    def next(self):
        if self.index == len(self.string):
            return None
        c = self.string[self.index]
        self.index += 1
        return c
    def curr(self):
        if self.index == len(self.string):
            return None
        return self.string[self.index]
    def prev(self):
        return self.string[self.index - 1]

class Re:
    def __init__(self, op, args):
        if op not in (LITERAL, STAR, CONCAT, UNION):
            raise Exception('Unsupported regex op')
        self.op = op
        self.args = args
    def __str__(self):
        if self.op == LITERAL:
            return str(self.args[0])
        elif self.op == STAR:
            return str(self.args[0]) + '*'
        elif self.op == UNION:
            return '|'.join([str(self.args[0]), str(self.args[1])])
        elif self.op == CONCAT:
            return '(' + ''.join([str(a) for a in self.args]) + ')'
        else:
            raise Exception('Unrecognized op:' + self.op)

# tokens are one-of:
# (STRING, <string>) A literal string to be matched
# (UNION, (<re1>, <re2>)
def scan_re(s, scanner=None, re=None, expect=None):
    if re is None:
        re = Re(CONCAT, [])
    init_entry = False
    if scanner is None:
        scanner = Scanner(s)
        init_entry = True
    while scanner.curr() is not None:
        if expect is not None and scanner.curr() == expect:
            break
        if scanner.curr() not in '()*|':
            t = Re(LITERAL, (scanner.next(),))
            print('//append token:', t)
            re.args.append(t)
        elif scanner.curr() == '(':
            scanner.next()
            re.args.append(scan_re(None, scanner=scanner, expect=')', re=Re(CONCAT, [])))
            scanner.next()
        elif scanner.curr() == '*':
            scanner.next()
            #tokens[-1] = (STAR, tokens[-1])
            re.args[-1] = Re(STAR, (re.args[-1],))
        elif scanner.curr() == '|':
            scanner.next()
            #re.args[].op = UNION
            re.args = re.args[:len(re.args)-1] + [Re(UNION, None)] + [re.args[len(re.args)-1]]
    _re = Re(CONCAT, [])
    i = 0
    while i < len(re.args):
        if re.args[i].op == UNION:
            #_tokens.args.append(Re(UNION, ((STRING, tokens[i][1]), (STRING, tokens[i+1][1]))))
            #_re.args.append(Re(UNION, (re.args[i], re.args[i+1])))
            #i += 1
            _re.args.append(Re(UNION, (re.args[i + 1], re.args[i + 2])))
            i += 2
        else:
            _re.args.append(re.args[i])
        i += 1
    return _re

def nfa2dfa(fa):
    if not fa.has_epsilon():
        return fa
    new_fa = FiniteAutomaton()
    unused_nodes = fa.nodes.copy()
    for n in fa.nodes:
        if n not in unused_nodes:
            continue
        #if n in new_fa.nodes:
        #    continue
        new_fa.add_node(n)
        other_nodes = fa.epsilon_reachable(n)
        print('//', n, 'may reach', other_nodes)
        for t in fa.transitions[n]:
            if t[1] != EPSILON:
                if t[0] not in new_fa.nodes:
                    new_fa.add_node(t[0])
                    if t[0] in fa.accept_states:
                        new_fa.add_accept_state(t[0])
                new_fa.add_transition(n, t[0], t[1])
        for on in other_nodes:
            if on in unused_nodes:
                del unused_nodes[unused_nodes.index(on)]
            ### inherit the traits of the other nodes we're absorbing
            # inherit their transitions
            for t in fa.transitions[on]:
                if t[1] == EPSILON:
                    continue
                    #raise AssertionError()
                if t[0] not in new_fa.nodes:
                    new_fa.add_node(t[0])
                    if t[0] in fa.accept_states:
                        new_fa.add_accept_state(t[0])
                new_fa.add_transition(n, t[0], t[1])
            # inherit if it's an accept state
            if on in fa.accept_states:
                new_fa.add_accept_state(n)
    return new_fa

def thompson(re, fa, start=None, prev=None, is_initentry=True):
    print('//thompson entry, re_tokens:', re_tokens)
    if start is None:
        start = fa.add_node()
    if prev is None:
        prev = start
    ret = {'start':start, 'end':prev}
    if re is None or len(re.args) == 0:
        return ret
    if re.op == CONCAT:
        #tok = re_tokens[0]
        for t in re.args:
            prev = thompson(t, fa, start=prev, prev=prev, is_initentry=False)['end']
        if is_initentry:
            fa.add_accept_state(prev)
        return {'start':start, 'end':prev}
    if re.op == LITERAL:
        prev = fa.add_node()
        fa.add_transition(start, prev, re.args[0])
        return {'start':start, 'end':prev}
    elif re.op == UNION:
        a_result = thompson(re.args[0], fa, is_initentry=False)
        b_result = thompson(re.args[1], fa, is_initentry=False)
        a_start = a_result['start']
        a_dest  = a_result['end']
        b_start = b_result['start']
        b_dest  = b_result['end']
        #prev = fa.add_node()
        fa.add_transition(prev, a_start, EPSILON)
        fa.add_transition(prev, b_start, EPSILON)
        prev = fa.add_node()
        fa.add_transition(a_dest, prev, EPSILON)
        fa.add_transition(b_dest, prev, EPSILON)

        return {'start':start, 'end':prev}
    elif re.op == STAR:
        m = thompson(re.args[0], fa, is_initentry=False)
        fa.add_transition(prev, m['start'], EPSILON)
        f = fa.add_node()
        fa.add_transition(m['end'], f, EPSILON)
        fa.add_transition(prev, f, EPSILON)
        fa.add_transition(m['end'], m['start'], EPSILON)
        return {'start':start, 'end':f}

#using Myhill-Nerode
def min_dfa(fa):
#    distinguishable_pairs = []
#    for F in fa.nodes:
#        if F not in fa.nodes.accept_states:
#            continue
#        for n in fa.nodes:
#            if n in fa.nodes.accept_states:
#                continue
#            distinguishable_pairs.append(set((n,F)))
#    for a in fa.alphabet:
    def groups_can_be_merged(a, b):
        #return False
        for la in a:
            for lb in b:
                if fa.is_final_accept_state(la) and fa.is_final_accept_state(lb):
                    return True
                if not fa.distinguishable(la, lb):
                    return False
        return True
    fa.kill_orphans()
    groups = [[n] for n in fa.nodes]
    print('//initial groups:', groups)
    distinguishments_made = True
    while distinguishments_made:
        distinguishments_made = False
        new_groups = []
        while len(groups):
            did_merge = False
            for i in range(1, len(groups)):
                if groups_can_be_merged(groups[0], groups[i]):
                    new_groups.append(groups[0] + groups[i])
                    distinguishments_made = True
                    print('//MERGING:', groups[i], groups[0])
                    del groups[i]
                    del groups[0]
                    did_merge = True
                    break
            if not did_merge:
                new_groups.append(groups[0])
                del groups[0]
        groups = new_groups
    print('//groups:', groups)
    new_fa = FiniteAutomaton()
    for i in range(len(groups)):
        new_fa.add_node(i)
    for i in range(len(groups)):
        for n in groups[i]:
            if n in fa.accept_states:
                new_fa.add_accept_state(i)
            if n in fa.transitions.keys():
                for t in fa.transitions[n]:
                    # find which group it's in
                    target_group = None
                    for j in range(len(groups)):
                        if t[0] in groups[j]:
                            target_group = j
                            break
                    if target_group == None:
                        raise AssertionError()
                    new_fa.add_transition(i, j, t[1])
    return new_fa

##### VERILOG SERIALIZATION #####

# generates a Verilog representation of an integer with x bits
def verilogbin(i, bitcount):
    s = bin(i).lstrip('0b')
    return "{}'b{}".format(bitcount, '0' * (bitcount - len(s)) + s)

# A wrapper around file-writing with various convenince functions
class Writer:
    def __init__(self, f):
        self.file = f
        self._indent = 0
    def write(self, s):
        self.file.write(self._indent*' ' + s)
    def indent(self):
        self._indent += 4
    def dedent(self):
        if self._indent == 0:
            raise Exception('Cannot decrease indent from 0.')
        self._indent -= 4
    def end(self):
        self.dedent()
        self.write('end\n')
    def define(self, a, b):
        self.file.write("`define {} {}\n".format(a, b))
    def reg(self, l):
        arg = ' '.join(l)
        if type(l) == str:
            arg = l
        self.write('reg ' + arg + ';\n')

# Writes out Verilog source for this DFA.
# This verilog chip has 3 states:
#
# WAIT   (00) => the DFA has not yet rejected, and it may accept or reject
#
# ACCEPT (01) => the DFA accepts the string up to this point, and may accept
#                the current string with additional characters added.
#
# REJECT (10) => the DFA rejects the string, and it therefore rejects any
#                further chars added, too. This is permanent until chip is
#                reset.
def dfa2verilog(dfa, out_file, module_name='DFA', \
        re='<none given during codegen>'):
    if dfa.has_epsilon():
        raise Exception('May only translate DFA to verilog.')
    state_bit_count = len(bin(len(dfa.nodes)).lstrip('0b'))
    out = Writer(out_file)
    out.define("WAIT", "2'b00")
    out.define("ACCEPT", "2'b01")
    out.define("REJECT", "2'b10")
    out.write('module {} (\n'.format(module_name))
    # accept one-of 0: WAIT 1: ACCEPT 2: REJECT
    out.indent()
    out.write('input clk,\n')
    out.write('input [7:0] data,\n')
    out.write('output reg[1:0] accept);\n\n')
    out.dedent()
    out.reg('[{}:0]'.format(state_bit_count-1) + ' state = {}'.format(verilogbin(0, state_bit_count)))
    init_accept = '`ACCEPT'
    if dfa.nodes[0] not in dfa.accept_states:
        init_accept = '`WAIT'
    out.reg('[1:0] accept_state = {}'.format(init_accept))
    out.write('always@(posedge clk) begin\n')
    out.indent()
    out.write('if(accept_state != `REJECT) begin\n')
    out.indent()
    for n in dfa.nodes:
        out.write('if(state == {}) begin\n'
                .format(verilogbin(n, state_bit_count)))
        out.indent()
        if n in dfa.transitions.keys():
            elsif = ''
            for t in dfa.transitions[n]:
                out.write('{}if(data == {}) /* {} */ begin\n'.format(elsif, verilogbin(ord(t[1]), 8), t[1]))
                out.indent()
                out.write('state <= {};\n'.format(verilogbin(t[0], state_bit_count))) 
                new_accept_state = '`WAIT'
                if t[0] in dfa.accept_states:
                    new_accept_state = '`ACCEPT'
                out.write('accept_state <= {};\n'.format(new_accept_state))
                out.end()
                elsif = 'else '

            els_accept = '`REJECT'

            out.write('else begin accept_state <= `REJECT; end\n')
        out.end()
    out.write('assign accept = accept_state;\n')
    out.end()
    out.end()
    out.write('endmodule')
    f = open('test-bench.v', 'r')
    out.file.write('\n')
    out.file.write(f.read().format(module_name, re))
    f.close()

##### END VERILOG SERIALIZATION #####

if __name__ == '__main__':
    fa = FiniteAutomaton()
    re_tokens = scan_re(input())
    print('//tokens are:', re_tokens)
    thompson(re_tokens, fa)
    dfa = nfa2dfa(fa)
    #dfa.kill_orphans()
    dfa = min_dfa(dfa)
    print(dfa.gv_serialize())
    dfa2verilog(dfa, open('out.v', 'w'), re=str(re_tokens))
