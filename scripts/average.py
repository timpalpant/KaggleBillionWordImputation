#!/usr/bin/env python

import sys

if __name__ == '__main__':
    total = 0.0
    n = 0
    for line in sys.stdin:
        total += float(line)
        n += 1
    print total / n