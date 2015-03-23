#!/usr/bin/env python

import argparse
import numpy as np
import Levenshtein
from itertools import izip
from util import tokenize_words, score
import matplotlib.pyplot as plt

KEEP_TOP_N = 5

class Prediction(object):
    def __init__(self, loc, word, Z, Z_location, *args):
        self.location = loc
        self.word = word
        self.Z = Z
        self.Z_location = Z_location
        self.p_anywhere = args[:KEEP_TOP_N]
        self.p_at_location = args[KEEP_TOP_N:2*KEEP_TOP_N]
        self.p_at_other_location = args[2*KEEP_TOP_N:3*KEEP_TOP_N]
        self.p_surrounding = args[3*KEEP_TOP_N:]
        
    @property
    def location_posterior(self):
        return 10.**(self.Z_location - self.Z)
        
    @property
    def word_posterior(self):
        return 10.**(self.p_anywhere[0] - self.Z)
        
    @classmethod
    def parse(cls, line):
        entry = line.rstrip().split('\t')
        entry[0] = int(entry[0])
        for i in xrange(2, len(entry)):
            entry[i] = float(entry[i])
        return cls(*entry)

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
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    print "Loading golden sentences"
    golden = [line.rstrip() for line in args.golden]
    print "Loading locations of removed words"
    golden_loc = np.asarray(map(int, args.i_removed))
    print "Generating sentences with removed word"
    removed = map(tokenize_words, golden)
    removed = [remove_word(words, loc) for words, loc in izip(removed, golden_loc)]
    print "Loading predictions"
    predictions = map(Prediction.parse, args.predicted)
    assert len(golden) == len(golden_loc)
    #assert len(golden) == len(predictions)
    if len(predictions) < len(golden):
        n = len(predictions)
        golden = golden[:n]
        golden_loc = golden_loc[:n]
        removed = removed[:n]

    orig = [' '.join(words) for words in removed]
    s = score(golden, orig)
    print "Score if no predictions are inserted: %s" % s
    
    best = None
    best_score = s
    loc_thresholds = (0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.)
    word_thresholds = (0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.)
    loss_surface = np.zeros((len(loc_thresholds), len(word_thresholds)))
    for i, loc_threshold in enumerate(loc_thresholds):
        for j, word_threshold in enumerate(word_thresholds):
            print "loc_threshold=%s, word_threshold=%s:" \
                % (loc_threshold, word_threshold)
            predicted = []
            for words, p in izip(removed, predictions):
                if p.ll_location > loc_threshold:
                    if p.ll_word > word_threshold: # insert predicted word
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
    plt.savefig('loss_surface.pdf')