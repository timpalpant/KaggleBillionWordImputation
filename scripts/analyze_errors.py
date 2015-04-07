#!/usr/bin/env python

'''
Insert missing word predictions in predicted location
'''

import sys, argparse
import numpy as np
from itertools import izip
from util import tokenize_words, Prediction

def opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('golden', type=argparse.FileType('r'),
        help='File with original sentences')
    parser.add_argument('i_removed', type=argparse.FileType('r'),
        help='File with true location of removed word')
    parser.add_argument('predicted', type=argparse.FileType('r'),
        help='Predictions for missing word and location')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    
    print >>sys.stderr, "Loading golden sentences"
    golden = map(tokenize_words, args.golden)
    print >>sys.stderr, "Loading locations of removed words"
    golden_loc = np.asarray(map(int, args.i_removed))
    print >>sys.stderr, "Loading predictions"
    predictions = map(Prediction.parse, args.predicted)
    assert len(golden) == len(golden_loc)
    if len(predictions) < len(golden):
        n = len(predictions)
        golden = golden[:n]
        golden_loc = golden_loc[:n]
        print >>sys.stderr, "Assuming first %d sentences" % n
        
    print >>sys.stderr, "Processing sentences"
    for p, g, gi in izip(predictions, golden, golden_loc):
        if p.locations[0] != gi or p.word != g[gi]: # error
            g[gi] = '***%s***' % g[gi]
            g.insert(p.locations[0], '^^^%s^^^' % p.word)
            print ' '.join(g)
        
