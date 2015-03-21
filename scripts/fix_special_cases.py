#!/usr/bin/env python

import argparse, sys
from itertools import izip
from util import POS_TAGS

def opts():
    parser = argparse.ArgumentParser(
        description='Manual patches for special cases')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    unk = set(('<s>','</s>','<unk>'))
    unk.update(POS_TAGS)
    for line in sys.stdin:
        entry = line.rstrip().split()
        predicted_word = entry[2]
        if predicted_word in unk:
            entry[2] = ' ' # just insert a space
        if predicted_word == 'i':
            entry[2] = 'I'
        print '\t'.join(entry)
