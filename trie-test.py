from trie import Trie

strings = ['apple', 'ape', 'or', 'orange', 'oppa']

t = Trie()

for s in strings:
    t.add_string(s)

print('// to compile this try dot trie.dot -T png -o trie.png\n')
print('// don\'t forget to pipe this to a file :)\n')
print(t.gv_serialize())
