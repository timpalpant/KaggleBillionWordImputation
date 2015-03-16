#!/usr/bin/env python

'''
Count frequency of each n-gram and save to Pickle file.
The n-gram frequencies are held in an in-memory dict, so this script
can only be used if the vocab is small (e.g. POS tags).
'''

import sys, argparse, pickle
from collections import defaultdict
from util import window, tokenize_words

PROGRESS = 1000000

def letter_frequencies(istream, n=1):
    counts = defaultdict(int)
    nwords = 0
    for i, line in enumerate(istream):
        words = tokenize_words(line)
        nwords += len(words)
        for word in words:
            #for letter in set(window(word,n)):
            for letter in set(word):
                counts[letter] += 1
        if i % PROGRESS == 0:
            print >>sys.stderr, i
            
    # Normalize counts to total number of words
    for k in counts.keys():
        counts[k] /= float(nwords)
    return counts

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=argparse.FileType('w'),
        help='Pickle file with n-gram counts')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    p = letter_frequencies(sys.stdin)
    most_common = list(v[1] for v in sorted((pl,l) for l, pl in p.iteritems()))[-1]
    print >>sys.stderr, "The most common letter is: %s" % most_common
    pickle.dump(p, args.output)