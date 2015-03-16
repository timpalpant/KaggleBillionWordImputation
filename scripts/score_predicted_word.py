#!/usr/bin/env python

import argparse
import numpy as np
import Levenshtein
from itertools import izip

def opts():
    parser = argparse.ArgumentParser(
        description='Compute fraction of correctly predicted missing words')
    parser.add_argument('golden', type=argparse.FileType('r'),
        help='File with reference missing positions')
    parser.add_argument('predicted', type=argparse.FileType('r'),
        help='File with predicted missing positions')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    d = []
    matched = []
    for p, r in izip(args.predicted, args.golden):
        matched.append(r == p)
        d.append(Levenshtein.distance(r, p))
    d = np.asarray(d)
    d_mean = d.mean()
    d_sem = d.std() / (len(d)-1)
    matched = np.asarray(matched)
    matched_mean = matched.mean()
    matched_sem = matched.std() / (len(matched)-1)
    print "Percent exact matches: %f +/- %f" \
        % (matched_mean, matched_sem)
    print "Mean Levenshtein distance: %f +/- %f" \
        % (d_mean, d_sem)
