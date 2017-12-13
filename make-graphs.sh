#!/bin/sh

# basic trie example
python3 trie-from-file.py basicstrings > trie.dot
dot trie.dot -T png -o trie.png

# trie of Call of Cthulhu
# This takes a while, so commented out
# python3 trie-from-file.py call-of-cthulhu.txt > coc.dot
# dot coc.dot -T svg -o coc_trie.svg

# basic radix tree example
python3 rtree-from-file.py basicstrings > bs_rt.dot
dot bs_rt.dot -T png -o bs_rt.png

xdg-open trie.png
xdg-open bs_rt.png
# xdg-open coc_trie.svg
