#!/usr/bin/env python

import argparse
import numpy as np
        
def load(fd):
    d = np.load(fd)
    return d['X']

def opts():
    parser = argparse.ArgumentParser(
        description='Find optimal threshold for inserting words')
    parser.add_argument('features', nargs='+', type=argparse.FileType('r'),
        help='npz files with training data')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    print >>sys.stderr, "Loading data"
    X = map(load, args.features)
    X = np.hstack(X)
    np.savez(sys.stdout, X=X)