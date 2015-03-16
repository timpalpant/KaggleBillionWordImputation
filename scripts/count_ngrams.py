#!/usr/bin/env python

'''
Count frequency of each n-gram and save to Pickle file.
The n-gram frequencies are held in an in-memory dict, so this script
can only be used if the vocab is small (e.g. POS tags).

For unigrams, see also: BillionWordImputation/build/Release/count_unigrams
'''

import sys, argparse
from util import ngram_frequencies

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-n', '--order', type=int, required=True,
        help='Order of model to count')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    counts = ngram_frequencies(sys.stdin, args.order)
    for ngram, freq in counts.iteritems():
        print '%s\t%s' % (' '.join(ngram), freq)