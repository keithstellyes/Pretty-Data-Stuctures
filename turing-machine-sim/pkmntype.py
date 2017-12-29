import turing_machine
import sys

m = turing_machine.load(open('pkmntypes.yml','r'))

if sys.argv[1] == 'GV':
    print(m.gv_serialize())
    sys.exit(0)

types = sys.argv[1:]

m.run_input(types)

print(m.tape.read())
