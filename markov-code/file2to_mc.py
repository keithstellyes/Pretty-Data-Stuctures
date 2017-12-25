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
words = f.read().replace('\n', ' ').replace('\t', ' ').split(' ')
f.close()

_words = []
for i in range(0, len(words), 2):
    if i == len(words) - 1:
        _words.append(words[i])
        continue
    _words.append(words[i] + '_' + words[i+1])
words = _words

print('Writing generated words to:', finname+'.words')
f = open(finname+'2.words', 'w')
f.write('\n'.join(words))
f.close()

c = MarkovChain(words, initstate=initial_state)
print('Writing DOT file to:', finname+'.dot')
f = open(finname+'2.dot', 'w')
f.write(c.gv_serialize())
f.close()

print('Writing generated data to:', finname+'.out')
f = open(finname+'2.out', 'w')

for i in range(count):
    words = c.next().split('_')
    for w in words:
        f.write(w)
        f.write(' ')

f.close()

print(sorted([k for k in c.ratiotable.keys()]))
