#!/usr/bin/env python

import argparse
from itertools import izip
import Levenshtein
    
def main(golden, predicted):
    total_d = 0
    n = 0
    for ref, pred in izip(golden, predicted):
        d = Levenshtein.distance(ref, pred)
        total_d += d
        n += 1
    return n, total_d
    
def opts():
    parser = argparse.ArgumentParser(
        description='Compute Levenshtein distance between sentences')
    parser.add_argument('golden', type=argparse.FileType('r'),
        help='File with reference sentences')
    parser.add_argument('predicted', type=argparse.FileType('r'),
        help='File with predicted sentences')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    n_sentences, total_d = main(args.golden, args.predicted)
    print "Processed %d sentences" % n_sentences
    avg = float(total_d) / n_sentences
    print "Mean Levenshtein distance: %f" % avg