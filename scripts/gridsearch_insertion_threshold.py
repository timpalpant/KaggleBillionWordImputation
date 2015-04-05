#!/usr/bin/env python

import argparse
import numpy as np
import Levenshtein
from itertools import izip
from util import tokenize_words, score, Prediction
import matplotlib.pyplot as plt

def remove_word(words, loc):
    removed = words[:loc] + words[loc+1:]
    return removed

def insert_word(words, word, loc):
    predicted = words[:loc] + [word] + words[loc:]
    return ' '.join(predicted)

def opts():
    parser = argparse.ArgumentParser(
        description='Find optimal threshold for inserting words')
    parser.add_argument('golden', type=argparse.FileType('r'),
        help='File with original sentences')
    parser.add_argument('i_removed', type=argparse.FileType('r'),
        help='File with true location of removed word')
    parser.add_argument('predicted', type=argparse.FileType('r'),
        help='Predictions for missing word and location')
    parser.add_argument('output',
        help='Output PDF with loss surface')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    print "Loading golden sentences"
    golden = [line.rstrip() for line in args.golden]
    print "Loading locations of removed words"
    golden_loc = np.asarray(map(int, args.i_removed))
    print "Loading predictions"
    predictions = map(Prediction.parse, args.predicted)
    assert len(golden) == len(golden_loc)
    #assert len(golden) == len(predictions)
    if len(predictions) < len(golden):
        n = len(predictions)
        golden = golden[:n]
        golden_loc = golden_loc[:n]
        
    print "Generating sentences with removed word"
    removed = map(tokenize_words, golden)
    removed = [remove_word(words, loc) for words, loc in izip(removed, golden_loc)]

    orig = [' '.join(words) for words in removed]
    s = score(golden, orig)
    print "Score if no predictions are inserted: %s" % s
    
    best = None
    best_score = s
    loc_thresholds = np.linspace(0, 1, 21)
    word_thresholds = np.linspace(0, 1, 21)
    loss_surface = np.zeros((len(loc_thresholds), len(word_thresholds)))
    for i, loc_threshold in enumerate(loc_thresholds):
        for j, word_threshold in enumerate(word_thresholds):
            print "loc_threshold=%s, word_threshold=%s:" \
                % (loc_threshold, word_threshold)
            predicted = []
            for words, p in izip(removed, predictions):
                if p.location_posterior > loc_threshold:
                    if p.word_posterior > word_threshold: # insert predicted word
                        predicted.append(insert_word(words, p.word, p.location))
                    else: # insert space at predicted location
                        predicted.append(insert_word(words, ' ', p.location))
                else: # do nothing
                    predicted.append(' '.join(words))
            s = score(golden, predicted)
            print "...score = %s" % s
            loss_surface[i,j] = s
            if s < best_score:
                best = (loc_threshold, word_threshold)
                best_score = s
    print "Best: loc_threshold=%s, word_threshold=%s" % best
    
    plt.imshow(loss_surface, interpolation='nearest')
    plt.colorbar()
    plt.ylabel('Location Threshold')
    plt.xlabel('Word Threshold')
    plt.yticks(np.arange(len(loc_thresholds)), loc_thresholds)
    plt.xticks(np.arange(len(word_thresholds)), word_thresholds)
    plt.tight_layout()
    plt.savefig(args.output)