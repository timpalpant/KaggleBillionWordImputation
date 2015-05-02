#!/usr/bin/env python

'''
Insert empty trees for empty sentences
'''

import sys, argparse
from util import tokenize_words
from itertools import izip
from nltk.tree import Tree

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trees', type=argparse.FileType('r'),
        help='File with parse trees')
    parser.add_argument('sentences', type=argparse.FileType('r'),
        help='File with original sentences')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    for tree, sentence in izip(args.trees, args.sentences):
        parse = Tree.fromstring(tree)
        words = tokenize_words(sentence)
        if len(parse.leaves()) != len(words):
            print "Parse tree does not match sentence!"
            print parse.leaves()
            print words