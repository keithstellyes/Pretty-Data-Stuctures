#!/bin/sh

python3 trie-test.py > trie.dot
dot trie.dot -T png -o trie.png
xdg-open trie.png


