#!/usr/bin/env python

'''Replace words with their word2vec class'''

import sys, argparse
from util import tokenize_words, load_vocab, UNKNOWN

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('classes', type=argparse.FileType('r'),
        help='File with word2vec classes')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    print >>sys.stderr, "Loading word2vec classes"
    vocab = load_vocab(args.classes)
        
    for i, line in enumerate(sys.stdin):
        words = [vocab.get(w, UNKNOWN) for w in tokenize_words(line)]
        print ' '.join(map(str, words))
        
        if i % 100000 == 0:
            print >>sys.stderr, i
        
