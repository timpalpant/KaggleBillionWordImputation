#!/usr/bin/env python

import sys, bz2
sys.path.insert(0, '/Users/timpalpant/Documents/Workspace/corenlp-python')
import nltk
from nltk.tree import Tree
from corenlp import StanfordCoreNLP
from remove_random_word import remove_random_word

print "Booting StanfordCoreNLP"
nlp = StanfordCoreNLP()

print "Initializing train file"
train = bz2.BZ2File('../data/train_v2.txt.bz2')
for line in train:
    rline = remove_random_word(line)
    lparse = nlp.raw_parse(line)
    ltree = Tree.fromstring(lparse['sentences'][0]['parsetree'])
    rparse = nlp.raw_parse(rline)
    rtree = Tree.fromstring(rparse['sentences'][0]['parsetree'])
    print ltree
    print rtree