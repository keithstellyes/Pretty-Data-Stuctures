#!/bin/sh

# basic trie example
python3 trie-test.py > trie.dot
dot trie.dot -T png -o trie.png

# trie of Call of Cthulhu
python3 trie-from-file.py call-of-cthulhu.txt > coc.dot
dot coc.dot -T svg -o coc_trie.svg

xdg-open trie.png
xdg-open coc_trie.svg
