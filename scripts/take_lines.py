#!/usr/bin/env python

'''
Add back empty lines to POS-tagged lines
'''

import sys, argparse, pickle
from collections import defaultdict
from itertools import izip

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lines', type=argparse.FileType('r'),
        help='File with indices lines to extract')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    indices = sorted(int(line.rstrip()) for line in args.lines)
    print >>sys.stderr, "Extracting %d lines" % len(indices)
    
    j = 0
    for i, line in enumerate(sys.stdin):
        if i == indices[j]:
            sys.stdout.write(line)
            j += 1
        if j >= len(indices):
            break