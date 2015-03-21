#!/usr/bin/env python

'''Replace <unk> tags with POS'''

import sys, argparse
from itertools import izip
from util import tokenize_words

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sentences', type=argparse.FileType('r'),
        help='File with sentences with <unk>')
    parser.add_argument('pos', type=argparse.FileType('r'),
        help='File with POS tags')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
        
    for i, (sentence, pos_tags) in enumerate(izip(args.sentences, args.pos)):
        words = tokenize_words(sentence)
        pos = tokenize_words(pos_tags)
        
        if len(words) != len(pos):
            print >>sys.stderr, 'Sentence has %d words, but POS has %d' \
                % (len(words), len(pos))
            print >>sys.stderr, words
            print >>sys.stderr, pos
            print ' '.join(words)
            continue
            
        for j, word in enumerate(words):
            if word == '<unknown>':
                words[j] = pos[j]
        print ' '.join(words)
        
        if i % 500000 == 0:
            print >>sys.stderr, i
        
