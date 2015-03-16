#!/usr/bin/env python

'''
Extract and print the removed word in each sentence
'''

import sys, argparse
from itertools import izip
from util import tokenize_words

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('gold', type=argparse.FileType('r'),
        help='Gold-standard (full) sentences')
    parser.add_argument('removed', type=argparse.FileType('r'),
        help='File with indices of removed words')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    for sentence, i_removed in izip(args.gold, args.removed):
        words = tokenize_words(sentence)
        i_removed = int(i_removed)
        print words[i_removed]
        
