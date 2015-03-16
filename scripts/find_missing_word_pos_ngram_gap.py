#!/usr/bin/env python

'''
Identify the location of a missing word in a sentence
using a POS-tag n-gram model. Computes gap likelihood
as:

P(gap) = P(a, *, b) / P(a, b)
'''

import sys, argparse, pickle
from collections import defaultdict
import numpy as np
from scipy.misc import logsumexp
from util import window, tokenize_words, normalize_ngrams

def marginalize(trigrams):
    gapgrams = defaultdict(list)
    for k, v in trigrams.iteritems():
        gapgrams[(k[0], k[2])].append(v)
    gapgrams = {k: logsumexp(v) for k, v in gapgrams.iteritems()}
    return gapgrams

def find_missing_word(words, bigrams, gapgrams):
    if len(words) < 2: return 0
    gapscore = []
    #words = ['<s>'] + words + ['</s>']
    for ngram in window(words, 2):
        try:
            score = gapgrams[ngram] - bigrams[ngram]
        except: 
            score = float('-inf')
        gapscore.append(score)
    idx = np.argmax(gapscore) + 1
    return idx

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bigrams', type=argparse.FileType('r'),
        help='Pickle file with POS bi-grams')
    parser.add_argument('trigrams', type=argparse.FileType('r'),
        help='Pickle file with POS tri-grams')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    print >>sys.stderr, "Loading bi-gram counts"
    bigrams = normalize_ngrams(pickle.load(args.bigrams))
    print >>sys.stderr, "Loading tri-gram counts"
    trigrams = normalize_ngrams(pickle.load(args.trigrams))
    print >>sys.stderr, "Marginalizing tri-grams over gaps"
    gapgrams = marginalize(trigrams)
    del trigrams

    for line in sys.stdin:
        try: 
            words = tokenize_words(line)
            print find_missing_word(words, bigrams, gapgrams)
        except Exception, e: 
            print >>sys.stderr, "ERROR: %s" % line.rstrip()
            print >>sys.stderr, e
            print 0
