import sys

from bs4 import BeautifulSoup as BS
from markover import *
import statistics

html_files = None

# we never write BEGIN/END to the output file, and these could be any
# arbitrary values, but for this we opt to simply use these strings
BEGIN = '<begin>'
END = '<end>'

if len(sys.argv) == 1:
    html_files = []
    while True:
        try:
            html_files.append(input())
        except EOFError:
            break
else:
    html_files = sys.argv[1:]

freq_table = {}

tc_to_tagname = {}
# indexed by tag.name
string_lists = {}

closer_map = {}

def tag_caret(t):
    return t[:t.find('>') + 1]

def soup_to_l(l, soup):
    for tag in soup.descendants:
        tc = tag_caret(str(tag))
        try:
            tag.name
            tag.children
        except AttributeError:
            continue
        l.append(tc)
        tc_to_tagname[tc] = tag.name
        if tag.name not in string_lists.keys():
            string_lists[tag.name] = []
        if tag.string is None:
            string_lists[tag.name].append((''))
        else:
            split = tag.string.replace('\n', ' ').replace('\t', ' ').split(' ')
            for i in range(0, len(split), 2):
                if i == len(split) - 1:
                    string_lists[tag.name].append((split[i],))
                else:
                    string_lists[tag.name].append((split[i], split[i+1]))
        closer_map[tc] = '</' + tag.name +'>'
for fname in html_files:
    l = [BEGIN]
    f = open(fname, 'r')
    s = f.read()
    f.close()
    soup = BS(s, 'html.parser')
    soup_to_l(l=l, soup=soup)
    l.append(END)
    build_freqtable(entries=l, g=freq_table)

print('Frequency table done building')

avg_strlen = int(statistics.mean([len(s) for s in string_lists]))
randstr_lowbound = avg_strlen // 2
randstr_uppbound = avg_strlen * 10
chain = MarkovChain(iterable=None, freqtable=freq_table, initstate=BEGIN)

string_chains = {}
for tc in tc_to_tagname.keys():
    tn = tc_to_tagname[tc]
    if tn in string_chains.keys():
        continue
    try:
        string_chains[tn] = MarkovChain(string_lists[tn])
    except IndexError:
        string_chains[tn] = None

print('String chains done generating')
dot_file = open('out.dot', 'w')
dot_file.write(chain.gv_serialize())
dot_file.close()
print('dot file done generating')
html_file = open('out.html', 'w')
count = 1000
i = 0
while i < count:
    tag = chain.next()
    if tag == END:
        break
    if tag == BEGIN:
        continue
    html_file.write(tag)
    #s = random.choice(strings[tag])
    #if s is not None:
    #    html_file.write(s)
    r = 0
    sc_key = tc_to_tagname[tag]
    if string_chains[sc_key] is not None:
        string_chains[sc_key].next(string_chains[sc_key].random_state())
        r = random.randint(randstr_lowbound, randstr_uppbound)
    for i in range(r):
        html_file.write(' '.join(string_chains[sc_key].next()))
        html_file.write(' ')
    html_file.write(closer_map[tag])
    i += 1
if i >= count:
    print('did not hit END')
else:
    print('hit END did', i, 'iterations')
html_file.close()
