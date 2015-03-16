#!/usr/bin/env python

'''
Add back empty lines to POS-tagged lines
'''

import sys, argparse, pickle
from collections import defaultdict
from itertools import izip

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('empty', type=argparse.FileType('r'),
        help='File with indices of one-word lines')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    empty = [int(e)-i for i,e in enumerate(args.empty)]
    
    j = 0
    for i, line in enumerate(sys.stdin):
        if j < len(empty) and i == empty[j]:
            print ''
            j += 1
        sys.stdout.write(line)