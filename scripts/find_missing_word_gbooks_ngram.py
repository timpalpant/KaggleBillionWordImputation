#!/usr/bin/env python

'''
Identify the location of a missing word in a sentence
using an n-gram model.
'''

import sys, argparse, pickle
import numpy as np
import ngram
from util import window, tokenize_words
    
freq = ngram.frequency

def find_missing_word(line):
    # For each pair of words, compute ln [ P(2-gram) / P(1-gram)*P(1-gram) ]
    # = ln P(2-gram) - ln P(1-gram) - ln P(1-gram)
    words = tokenize_words(line)
    if len(words) < 2: print >>sys.stderr, line + ' _______'
    gapscore = []
    for pair in window(pos_tags, 2):
        bi = float(freq(*pair))
        uni = freq(pair[0]) * freq(pair[1])
        try: score = bi / uni
        except: score = float('inf')
        gapscore.append(score)
    idx = np.argmin(gapscore) + 1
    print >>sys.stderr, np.log10(gapscore)
    print >>sys.stderr, ' '.join(words[:idx]) + ' _______ ' + ' '.join(words[idx:])
    return idx

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    for line in sys.stdin:
        try: 
            print find_missing_word(line)
        except Exception, e: 
            print >>sys.stderr, "ERROR: %s" % line.rstrip()
            print >>sys.stderr, e
            print 0