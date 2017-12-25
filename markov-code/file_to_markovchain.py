import sys
from common import *
from markover import *

finname = sys.argv[1]
print('Input file:', finname)
f = open(sys.argv[1], 'r')
count = int(sys.argv[2])
print('Going for', count, 'iterations')
initial_state = None

try:
    initial_state = sys.argv[3].upper().strip()
except:
    print('Using random initial state')
words = file_to_words(f)
print('Writing generated words to:', finname+'.words')
f = open(finname+'.words', 'w')
f.write('\n'.join(words))
f.close()

c = MarkovChain(words, initstate=initial_state)
print('Writing DOT file to:', finname+'.dot')
f = open(finname+'.dot', 'w')
f.write(c.gv_serialize())
f.close()

print('Writing generated data to:', finname+'.out')
f = open(finname+'.out', 'w')
f.write('\n'.join([c.next() for i in range(count)]))
f.close()

print(sorted([k for k in c.ratiotable.keys()]))
