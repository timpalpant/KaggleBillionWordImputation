#!/usr/bin/env python

'''Convert test file format to train file format'''

import sys

if __name__ == '__main__':
    header = sys.stdin.readline()
    for line in sys.stdin:
        i, sentence = line.rstrip().split(',', 1)
        print sentence[1:-1].replace('""', '"')