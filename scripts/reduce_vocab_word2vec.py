#!/usr/bin/env python

'''
Create a word mapping that keeps only the n most common words,
and maps all others to their closest analogue in the top n
based on word2vec vectors.
'''

import sys, argparse
from util import tokenize_words, load_vocab, prune_vocab, Word2Vec, UNKNOWN

def find_nearest_word_in(word, w2v, kept_ids):
    for analogue in w2v.nearest(word, kept_ids):
        return analogue
    raise ValueError("No analogues for %s in Word2Vec" % word)

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('word2vec', type=argparse.FileType('r'),
        help='File with word2vec vectors')
    parser.add_argument('vocab', type=argparse.FileType('r'),
        help='File with vocabulary')
    parser.add_argument('-n', type=int, required=True, 
        help='Desired vocab size')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    print >>sys.stderr, "Loading vocab"
    vocab = load_vocab(args.vocab)
    reduced_vocab = prune_vocab(vocab, args.n)
    
    print >>sys.stderr, "Loading word2vec"
    w2v = Word2Vec.load(args.word2vec)
    kept_ids = [w2v.word_to_id[w] for w in reduced_vocab]
    
    # For all words not in kept vocab, find nearest word
    print >>sys.stderr, "Generating word mapping"
    for word in vocab.iterkeys():
        if word in reduced_vocab: # word is kept
            nearest = word
        else: # word is not kept
            try: nearest = find_nearest_word_in(word, w2v, kept_ids)
            except: nearest = UNKNOWN
        print '%s\t%s' % (word, nearest)
        
