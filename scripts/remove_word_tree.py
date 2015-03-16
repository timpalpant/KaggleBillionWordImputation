#!/usr/bin/env python

import sys, random
from nltk.tree import Tree

def remove_random_word(tree):
    '''Removes a random word in syntax tree'''
    nleaves = len(tree.leaves())
    leaf = random.randint(1, nleaves-1)
    tp = tree.leaf_treeposition(leaf)
    tree[tp[:-2]].pop(tp[-2])
    return tree

if __name__ == '__main__':
    for line in sys.stdin:
        try:
            tree = Tree.fromstring(line)
            tree = remove_random_word(tree)
            print " ".join(str(tree).split())
        except Exception, e:
            print >>sys.stderr, "Error parsing tree: %s" % line
            print >>sys.stderr, e