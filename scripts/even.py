#!/usr/bin/env python

'''
Print 1 if even, 0 if odd
'''

import sys

for line in sys.stdin:
    i = int(line.rstrip())
    print int(i % 2 == 0)