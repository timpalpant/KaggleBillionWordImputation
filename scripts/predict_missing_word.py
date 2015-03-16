#!/usr/bin/env python

'''
Predict the missing word.
'''

import sys, argparse
from itertools import izip
from util import tokenize_words

def count_quotes(words):
    return sum(word=='"' for word in words)

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sample', type=argparse.FileType('r'),
        help='Sentences with one missing word')
    parser.add_argument('removed', type=argparse.FileType('r'),
        help='File with predicted indices of missing words')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    for sentence, i_missing in izip(args.sample, args.removed):
        words = tokenize_words(sentence)
        if count_quotes(words) % 2 == 1:
            print '"'
            continue
        i_missing = int(i_missing)
        print ''
        
