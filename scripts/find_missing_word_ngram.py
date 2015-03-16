#!/usr/bin/env python

'''
Identify the location of a missing word in a sentence
using an n-gram model.
'''

import sys, argparse, pickle
from itertools import islice
import numpy as np
import kenlm
from util import tokenize_words

def find_missing_word(model, line):
    words = tokenize_words(line)
    if len(words) <= 2: 
        return 1
    scores = list(p for p, _, _ in model.full_scores(line))
    # missing word cannot be the first or last, per rules
    idx = np.argmin(scores[1:-2]) + 1
    return idx

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model',
        help='KenLM n-gram model file (ARPA or binary)')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    print >>sys.stderr, "Loading language model"
    model = kenlm.LanguageModel(args.model)
    for line in sys.stdin:
        try: print find_missing_word(model, line)
        except Exception, e: 
            print >>sys.stderr, "ERROR: %s" % line.rstrip()
            print >>sys.stderr, e
            print 0