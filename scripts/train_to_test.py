#!/usr/bin/env python

'''Convert train file format to test file format'''

import sys

if __name__ == '__main__':
    print '"id","sentence"'
    for i, line in enumerate(sys.stdin):
        line = line.rstrip().replace('"', '""')
        print '%d,"%s"' % (i+1, line)