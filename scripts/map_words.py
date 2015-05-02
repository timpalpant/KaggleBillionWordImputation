#!/usr/bin/env python

'''
Map words -> other words
This is used to replace infrequent words with more common analogues.
'''

import sys, argparse
from itertools import izip
from util import tokenize_words, UNKNOWN

def load_mapping(istream):
    mapping = {}
    for line in istream:
        from_word, to_word = line.rstrip().split()
        mapping[from_word] = to_word
    return mapping

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sentences', type=argparse.FileType('r'),
        help='File with sentences')
    parser.add_argument('mapping', type=argparse.FileType('r'),
        help='File with word map')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    mapping = load_mapping(args.mapping)
    for i, sentence in enumerate(args.sentences):
        words = [mapping.get(w, UNKNOWN) for w in tokenize_words(sentence)]
        print ' '.join(words)
        
        if i % 500000 == 0:
            print >>sys.stderr, i
        
