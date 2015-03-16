#!/usr/bin/env python

'''Keep only the n most popular words, replacing all others with <unk>'''

import sys, argparse
from util import tokenize_words, load_vocab

def prune_vocab(vocab, n):
    nwords = sum(v for v in vocab.itervalues())
    nvocab = len(vocab)
    print >>sys.stderr, "Input has nwords = %s, vocab size = %d" \
        % (nwords, nvocab)
    vocab = [(v,k) for k,v in vocab.iteritems()]
    vocab = list(reversed(sorted(vocab)))
    vocab = vocab[:args.n]
    vocab = {k: v for v, k in vocab}
    nremaining = sum(v for v in vocab.itervalues())
    percent_kept = float(len(vocab)) / nvocab
    percent_mass = float(nremaining) / nwords
    print >>sys.stderr, "Keeping %d words (%.2f%% of vocab, %.2f%% of mass)" \
        % (len(vocab), 100*percent_kept, 100*percent_mass)
    return vocab

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
                words[j] = '<unk>'
        print ' '.join(words)
        
        if i % 100000 == 0:
            print >>sys.stderr, i
        
