import turing_machine
import sys

def build_md_table(machine, data):
    data.append({'cols':[machine.state] + machine.tape[0:4], 'ptr':machine.tape.head})

def finalize_md_table(data):
    def s2(s):
        if s.strip() == '':
            return '{empty}'
        return str(s)

    print('|State|0   |1   |2   |3   |')
    print('|-----|----|----|----|----|')
    for datum in data:
        row = [s2(c) for c in datum['cols']]
        try:
            ptr = datum['ptr'] + 1
            row[ptr] = '>>' + row[ptr] + '<<'
        except IndexError:
            pass
        print('|' + '|'.join(row) + '|')

m = turing_machine.load(open('pkmntypes.yml','r'))

if sys.argv[1] == 'gv':
    print(m.gv_serialize())
    sys.exit(0)

watch = None
data = []

if sys.argv[1] == 'watch':
    watch_type = sys.argv[2]
    sys.argv = sys.argv[2:]

    if watch_type == 'md':
        watch = lambda m: build_md_table(m, data=data)

types = sys.argv[1:]


m.run_input(types, monitor_function=watch)

#if watch is not None:
#    def str2(s):
#        if s.strip() == '':
#            return '{empty}'
#        return str(s)
#    s = [[str2(e) for e in row] for row in watch]
#    lens = [max(map(len,col)) for col in zip(*s)]
#    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
#    table = [fmt.format(*row) for row in s]
#    print('\n'.join(table))
finalize_md_table(data)

print(m.tape.read())
