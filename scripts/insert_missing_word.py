#!/usr/bin/env python

'''
Insert missing word predictions into predicted missing location.
'''

import sys, argparse
from itertools import izip
from util import tokenize_words

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sample', type=argparse.FileType('r'),
        help='Sentences with one missing word')
    parser.add_argument('removed', type=argparse.FileType('r'),
        help='File with predicted indices of missing words')
    parser.add_argument('predicted', type=argparse.FileType('r'),
        help='File with predicted missing words')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    for sentence, i_missing, predicted in izip(args.sample, args.removed, args.predicted):
        i_missing = int(i_missing)
        if i_missing < 0: 
            print sentence.rstrip()
            continue
        words = tokenize_words(sentence)
        words.insert(i_missing, predicted.strip())
        print ' '.join(words)
        
