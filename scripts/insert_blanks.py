#!/usr/bin/env python

'''
Insert blanks like madlib in place of removed words
'''

import sys, argparse
from itertools import izip
from util import tokenize_words, Prediction

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sample', type=argparse.FileType('r'),
        help='Sentences with one missing word')
    parser.add_argument('predictions', type=argparse.FileType('r'),
        help='File with predicted indices of missing words')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    for sentence, pred in izip(args.sample, args.predictions):
        words = tokenize_words(sentence)
        p = Prediction.parse(pred)
        i_missing = p.locations[0]
        words.insert(i_missing, '________')
        print ' '.join(words)
        
