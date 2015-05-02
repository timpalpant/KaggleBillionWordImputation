#!/usr/bin/env python

'''
Insert missing word predictions in predicted location
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
    parser.add_argument('--location-threshold', type=float,
        default=0, help='Threshold for whether to insert anything')
    parser.add_argument('--word-threshold', type=float, default=0,
        help='Threshold for whether to insert word or space')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    for sentence, pred in izip(args.sample, args.predictions):
        words = tokenize_words(sentence)
        p = Prediction.parse(pred)
        if p.location_posterior > args.location_threshold:
            if p.word_posterior > args.word_threshold:
                words.insert(p.location, p.word)
            else:
                words.insert(p.location, ' ')
        print ' '.join(words)
        
