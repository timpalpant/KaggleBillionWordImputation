#!/usr/bin/env python

'''Try to guess cased word from lowercase'''

import sys, argparse
from collections import defaultdict
from util import tokenize_words, load_vocab

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('vocab', type=argparse.FileType('r'),
        help='File with vocabulary')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    print >>sys.stderr, "Loading vocab"
    vocab = load_vocab(args.vocab)
    print >>sys.stderr, "Determining best-guess case for each word"
    lower_to_case = {}
    for word, freq in vocab.iteritems():
        lowercase = word.lower()
        if lowercase in lower_to_case:
            prev_freq = lower_to_case[lowercase][1]
            if freq > prev_freq:
                lower_to_case[lowercase] = (word, freq)
        else:
            lower_to_case[lowercase] = (word, freq)
    del vocab
    for k in lower_to_case.keys():
        lower_to_case[k] = lower_to_case[k][0]
        
    print >>sys.stderr, "Processing predictions"
    for line in sys.stdin:
        entry = line.rstrip().split()
        predicted_word = entry[0]
        entry[0] = lower_to_case.get(predicted_word, predicted_word)
        print '\t'.join(entry)
        
