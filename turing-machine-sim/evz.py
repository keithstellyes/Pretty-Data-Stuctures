# Merely parses the even-zeros turing machine and then prints its DOT

import turing_machine

print(turing_machine.load(open('even-zeros.yml','r')).gv_serialize())
