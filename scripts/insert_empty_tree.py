#!/usr/bin/env python

'''
Insert empty trees for empty sentences
'''

import sys, argparse

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('insert_indices', type=argparse.FileType('r'),
        help='File with line indices to insert')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    insert_indices = sorted(int(line.rstrip()) for line in args.insert_indices)
    print >>sys.stderr, "Will insert %d empty trees" % len(insert_indices)
    
    i = 0
    for line in sys.stdin:
        while insert_indices and insert_indices[0] == i:
            print >>sys.stderr, "Inserting tree at line %d" % i
            print "(())"
            i += 1
            insert_indices.pop(0)
            
        sys.stdout.write(line)
        i += 1