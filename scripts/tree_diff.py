#!/usr/bin/env python

import sys, argparse
from itertools import izip
from nltk.tree import Tree

def tree_diff(tree1, tree2):
    if tree1.leaves() != tree2.leaves():
        raise ValueError, "Trees are not of the same sentence"
    for i in xrange(len(tree1.leaves())):
        tp1 = tree1.leaf_treeposition(i)
        tp2 = tree2.leaf_treeposition(i)
        if tp1 != tp2:
            print tp1, tp2
            return False
    return True

def main(tree_file1, tree_file2):
    same = 0
    different = 0
    for line1, line2 in izip(tree_file1, tree_file2):
        try:
            tree1 = Tree.fromstring(line1)
            tree2 = Tree.fromstring(line2)
            d = tree_diff(tree1, tree2)
            if d:
                different += 1
                print tree1
                print tree2
            else: same += 1
        except Exception, e:
            print e
            print line1
            print line2
    
    print "Same = %d, different = %d" % (same, different)
    
def opts():
    parser = argparse.ArgumentParser(
        description='Compare parse trees')
    parser.add_argument('file1', type=argparse.FileType('r'),
        help='File with parse trees')
    parser.add_argument('file2', type=argparse.FileType('r'),
        help='File with parse trees')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    main(args.file1, args.file2)
