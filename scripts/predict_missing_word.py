#!/usr/bin/env python

'''
Predict the missing word.
'''

import sys, argparse
import cPickle as pickle
from itertools import izip
from util import tokenize_words, Prediction

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sample', type=argparse.FileType('r'),
        help='Sentences with one missing word')
    parser.add_argument('predictions', type=argparse.FileType('r'),
        help='File with predictions')
    parser.add_argument('clf', type=argparse.FileType('r'),
        help='Pickle file with classifier')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    clf = pickle.load(args.clf)
    
    for sentence, i_missing in izip(args.sample, args.removed):
        words = tokenize_words(sentence)
        if count_quotes(words) % 2 == 1:
            print '"'
            continue
        i_missing = int(i_missing)
        print ''
        
