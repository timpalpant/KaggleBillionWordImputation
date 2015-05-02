#!/usr/bin/env python

'''Keep only the n most popular words, replacing all others with <unk>'''

import sys, argparse
from util import tokenize_words, load_vocab, prune_vocab, UNKNOWN

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('vocab', type=argparse.FileType('r'),
        help='File with vocabulary')
    parser.add_argument('-n', type=int, required=True, 
        help='Desired vocab size')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    print >>sys.stderr, "Loading vocab"
    vocab = load_vocab(args.vocab)
    vocab = prune_vocab(vocab, args.n)
        
    for i, line in enumerate(sys.stdin):
        words = tokenize_words(line)
        for j, word in enumerate(words):
            if word not in vocab:
                words[j] = UNKNOWN
        print ' '.join(words)
        
        if i % 100000 == 0:
            print >>sys.stderr, i
        
