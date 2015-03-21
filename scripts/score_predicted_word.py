#!/usr/bin/env python

import argparse, sys
import numpy as np
import Levenshtein
from itertools import izip

def opts():
    parser = argparse.ArgumentParser(
        description='Compute fraction of correctly predicted missing words')
    parser.add_argument('golden', type=argparse.FileType('r'),
        help='File with reference words or sentences')
    parser.add_argument('predicted', type=argparse.FileType('r'),
        help='File with predicted words or sentences')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    d = []
    matched = []
    for p, r in izip(args.predicted, args.golden):
        matched.append(r == p)
        edit = Levenshtein.distance(r, p)
        d.append(edit)
        print edit
    d = np.asarray(d)
    d_mean = d.mean()
    d_sem = d.std() / np.sqrt(len(d))
    matched = np.asarray(matched)
    matched_mean = matched.mean()
    matched_sem = matched.std() / np.sqrt(len(matched))
    print >>sys.stderr, "Percent exact matches: %f +/- %f" \
        % (matched_mean, matched_sem)
    print >>sys.stderr, "Mean Levenshtein distance: %f +/- %f" \
        % (d_mean, d_sem)
