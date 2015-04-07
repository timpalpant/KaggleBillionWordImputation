#!/usr/bin/env python

import argparse
from itertools import izip
import numpy as np
from util import Prediction, tokenize_words, is_punctuation, load_vocab
from util import POS_TAGS, UNKNOWN
import Levenshtein

def any_true(words, f, begin=None, end=None):
    if begin is None or end is None:
        return any(f(w) for w in words)
        
    return any(f(w) for w in words[begin:end])

def any_oov(vocab, words, begin=None, end=None):
    return any_true(words, lambda w: w not in vocab, begin, end)

def any_punctuation(words, begin=None, end=None):
    return any_true(words, is_punctuation, begin, end)

def cost_per_choice(golden, golden_loc, predictions):
    '''
    Return Levenshtein distance for each sentence if:
       1) do nothing
       2) insert a space at predicted location
       3) insert word at predicted location
    '''
    d = np.zeros((len(predictions), 3), dtype=int)
    for i, (g, loc, p) in enumerate(izip(golden, golden_loc, predictions)):
        d[i,0] = len(g[loc]) + 1 # do nothing
        if p.location == loc: # guessed location correctly
            d[i,1] = len(g[loc])
            d[i,2] = Levenshtein.distance(p.word, g[loc])
        else: # didn't guess location correctly
            d[i,1] = len(g[loc]) + 2
            d[i,2] = len(p.word) + len(g[loc]) + 2
    return d

def opts():
    parser = argparse.ArgumentParser(
        description='Find optimal threshold for inserting words')
    parser.add_argument('golden', type=argparse.FileType('r'),
        help='File with original sentences')
    parser.add_argument('i_removed', type=argparse.FileType('r'),
        help='File with true location of removed word')
    parser.add_argument('predicted', type=argparse.FileType('r'),
        help='Predictions for missing word and location')
    parser.add_argument('output', type=argparse.FileType('w'),
        help='X and y data for classifier training')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    print "Loading golden sentences"
    golden = map(tokenize_words, args.golden)
    print "Loading locations of removed words"
    golden_loc = np.asarray(map(int, args.i_removed))
    print "Loading predictions"
    predictions = map(Prediction.parse, args.predicted)
    assert len(golden) == len(golden_loc)
    if len(predictions) < len(golden):
        n = len(predictions)
        golden = golden[:n]
        golden_loc = golden_loc[:n]
        print "Assuming first %d sentences" % n
    
    print "Computing cost for each choice"
    d = cost_per_choice(golden, golden_loc, predictions)
    print "Identifying optimal choices"
    y = np.argmin(d, axis=1)
    best = [di[yi] for di, yi in izip(d,y)]
    dx = np.mean(best)
    error = np.std(best) / np.sqrt(len(best))
    print "Best achievable Levenshtein distance: %.3f +/- %.3f" % (dx, error)
    
    unk = set(('<s>','</s>','<unk>',UNKNOWN))
    unk.update(POS_TAGS)
    
    print "Making data frames"
    order = predictions[0].order
    nfeatures = 7*Prediction.keep_top_n - 2 + 2*order + 10
    print "%d features for each sentence" % nfeatures
    X = np.zeros((len(predictions), nfeatures))
    for i, (p, g, gi) in enumerate(izip(predictions, golden, golden_loc)):
        # log10 probabilities of top N words, and surrounding N-grams
        xs = p.p_at_location + p.p_anywhere + p.p_at_other_location
        row = [10.**(x-p.Z) for x in xs]
        row += [10.**(x-p.p_anywhere[0]) for x in xs[1:]]
        if len(p.p_surrounding) != order: # short sentence, missing p_surrounding
            row += [0 for i in xrange(2*order)]
        else:
            row += [10.**x for x in sorted(p.p_surrounding)]
            row += [10.**x for x in p.p_surrounding]
        # posterior probabilities of best location
        row += [p.location_posterior, 10.**p.location_ratio, 10.**p.word_ratio]
        nwords_in_sentence = len(g) - 1 # b/c these are golden sentences
        # distance of top N words from top location
        row += [abs(x-p.locations[0]) for x in p.locations[1:]]
        # fraction of top N words predicted to be at this location
        try: f = sum(loc==p.locations[0] for loc in p.locations) / float(len(p.locations))
        except ZeroDivisionError: f = 0
        try: f2 = float(p.location)/nwords_in_sentence
        except ZeroDivisionError: f2 = 0
        row += [f, nwords_in_sentence, nwords_in_sentence-p.location, p.location, f2]
        # predicted word is unknown / POS tag
        row.append(p.word in unk)
        # amount of punctuation in the sentence
        npunct = sum(is_punctuation(w) for i, w in enumerate(g) if i != gi)
        # amount of punctuation around the predicted word
        npunct_around_word = sum(is_punctuation(w) for w in g[max(0,i-5):i+5])
        row += [npunct, npunct_around_word]
        X[i] = row
        
    print "Saving data frames to output"
    np.savez(args.output, X=X, y=y, d=d)
    