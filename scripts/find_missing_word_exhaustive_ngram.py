#!/usr/bin/env python

'''
Identify the location of a missing word in a sentence
using an n-gram model.
'''

import sys, argparse, pickle
from itertools import islice
import numpy as np
import kenlm
from util import tokenize_words

def load_vocab(istream):
    vocab = []
    for line in istream:
        word = line.rstrip().split()[0]
        vocab.append(word)
    return vocab

def max_prob_word_at(words, i, vocab):
    '''
    Return the word that maximizes the sentence probability 
    if inserted at position i
    '''
    max_p = -float('inf')
    best = None
    for candidate in vocab:
        inserted = words[:i] + [candidate] + words[i:]
        p = model.score(' '.join(inserted))
        if p > max_p:
            max_p = p
            best = candidate
    return best, max_p

def find_missing_word(model, vocab, line):
    '''
    Return the location and word that maximizes the sentence probability
    if that word is inserted at that location
    '''
    words = tokenize_words(line)
    if len(words) <= 2: 
        best, _ = max_prob_word_at(words, 1, vocab)
        return 1, best
    
    # missing word cannot be the first or last
    max_p = -float('inf')
    best = None
    for i in xrange(1, len(words)-1):
        i_best, i_max_p = max_prob_word_at(words, i, vocab)
        if i_max_p > max_p:
            max_p = i_max_p
            best = (i, i_best)
    return best

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model',
        help='KenLM n-gram model file (ARPA or binary)')
    parser.add_argument('vocab', type=argparse.FileType('r'),
        help='Vocab file')
    parser.add_argument('guessed_position', type=argparse.FileType('w'),
        help='File with guessed position of missing word')
    parser.add_argument('guessed_word', type=argparse.FileType('w'),
        help='File with guessed position of missing word')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    print >>sys.stderr, "Loading vocab"
    vocab = load_vocab(args.vocab)
    print >>sys.stderr, "%d words in vocab" % len(vocab)
    print >>sys.stderr, "Loading language model"
    model = kenlm.LanguageModel(args.model)
    
    print >>sys.stderr, "Processing sentences"
    for line_num, line in enumerate(sys.stdin):
        try:
            i, guess = find_missing_word(model, vocab, line)
            print >>args.guessed_position, i
            print >>args.guessed_word, guess
        except Exception, e: 
            print >>sys.stderr, "ERROR: %s" % line.rstrip()
            print >>sys.stderr, e
            print >>args.guessed_position, 0
            print >>args.guessed_word, ' '
            
        if line_num % 100 == 0:
            print >>sys.stderr, line_num