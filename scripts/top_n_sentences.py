#!/usr/bin/env python

'''
Identify the location of a missing word in a sentence
using an n-gram model. Print the top N most probable
sentences.
'''

import sys, argparse, pickle
from itertools import islice
import numpy as np
import kenlm
from util import tokenize_words, load_vocab, TopK

def max_prob_word_at(words, i, vocab, n):
    '''
    Return the word that maximizes the sentence probability 
    if inserted at position i
    '''
    top_n = TopK(n)
    for candidate in vocab:
        inserted = words[:i] + [candidate] + words[i:]
        p = model.score(' '.join(inserted))
        top_n.add((words, i, candidate), p)
    return top_n

def find_missing_word(model, vocab, line, n):
    '''
    Return the location and word that maximizes the sentence probability
    if that word is inserted at that location
    '''
    words = tokenize_words(line)
    if len(words) <= 2: 
        return max_prob_word_at(words, 1, vocab)
    
    # missing word cannot be the first or last
    top_n = TopK(n)
    for i in xrange(1, len(words)-1):
        #print >>sys.stderr, "Considering words inserted at %d:" % i
        top_n_i = max_prob_word_at(words, i, vocab, n)
        #print_top_n(top_n_i)
        top_n.update(top_n_i)
        #print >>sys.stderr, "Current best:"
        #print_top_n(top_n)
    return top_n

def print_top_n(top_n):
    for k, ((words, i, candidate), prob) in enumerate(top_n):
        inserted = words[:i] + ['***%s***' % candidate] + words[i:]
        prediction = ' '.join(inserted)
        print "%d) P = %.3f: %s" % (k, -prob, prediction)

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model',
        help='KenLM n-gram model file (ARPA or binary)')
    parser.add_argument('vocab', type=argparse.FileType('r'),
        help='Vocab file')
    parser.add_argument('-n', type=int, default=5,
        help='Number of best sentences to report')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    print >>sys.stderr, "Loading vocab"
    vocab = load_vocab(args.vocab)
    print >>sys.stderr, "%d words in vocab" % len(vocab)
    print >>sys.stderr, "Loading language model"
    model = kenlm.LanguageModel(args.model)
    
    print >>sys.stderr, "Processing sentences"
    for line in sys.stdin:
        top_n = find_missing_word(model, vocab, line, args.n)
        print_top_n(top_n)