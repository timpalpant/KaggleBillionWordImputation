#!/usr/bin/env python

'''
Count frequency of each syntactic n-gram and save to Pickle file.
The n-gram frequencies are held in an in-memory dict, so this script
can only be used if the vocab is small (e.g. POS tags).
'''

import sys, argparse
from collections import defaultdict
from util import ngram_frequencies
from nltk.tree import Tree

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lexical', action='store_true',
        help='Count lexical as well as non-lexical productions')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    counts = defaultdict(lambda: 0)
    for line in sys.stdin:
        t = Tree.fromstring(line)
        for p in t.productions():
            if args.lexical or p.is_nonlexical():
                counts[str(p)] += 1
                
    for ngram, freq in counts.iteritems():
        print '%s\t%s' % (ngram, freq)