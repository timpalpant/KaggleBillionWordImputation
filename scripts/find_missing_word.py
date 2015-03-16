#!/usr/bin/env python

'''
Find the missing word in each sentence by comparing
to a gold standard.

../scripts/find_missing_word.py train_v2.txt train_v2.removed.txt > train_v2.i_removed.txt
'''

import sys, argparse
from itertools import izip
from util import tokenize_words

def missing_word_index(sentence, ref_sentence, lo=0, hi=None):
    '''
    Use bisection search to find the location of the missing word
    in @sentence with respect to @ref_sentence. Return the index
    of the missing word in @ref_sentence.
    '''
    words = tokenize_words(sentence)
    ref_words = tokenize_words(ref_sentence)
    assert len(words) == len(ref_words) - 1
    lo = lo if lo is not None else 0
    hi = hi if hi is not None else len(ref_words)
    i = (lo + hi) / 2
    while lo+1 < hi:
        if words[i] == ref_words[i]:
            lo = i
        else:
            hi = i
        i = (lo + hi) / 2
        
    if i < len(words) and words[i] == ref_words[i]: i += 1
    assert words[i-1] == ref_words[i-1]
    assert words[i] != ref_words[i] or i == len(words)
    return i

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('gold', type=argparse.FileType('r'),
        help='Gold-standard sentences')
    parser.add_argument('removed', type=argparse.FileType('r'),
        help='Sentences with one missing word')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    for sentence, ref_sentence in izip(args.removed, args.gold):
        print missing_word_index(sentence, ref_sentence)
        