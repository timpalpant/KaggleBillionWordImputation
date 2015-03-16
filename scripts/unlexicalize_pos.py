#!/usr/bin/env python

'''
Unlexicalize POS-tagged sentences to train a POS ngram model.
'''

import sys
from util import tokenize_words, pos_tag

PROGRESS = 1000000

if __name__ == "__main__":
    for i, line in enumerate(sys.stdin):
        words = tokenize_words(line)
        pos = map(pos_tag, words)
        print ' '.join(pos)
        
        if i % PROGRESS == 0:
            print >>sys.stderr, i