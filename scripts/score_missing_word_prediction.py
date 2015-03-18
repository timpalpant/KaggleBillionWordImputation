#!/usr/bin/env python

import argparse, sys
from itertools import izip, repeat
import numpy as np
import kenlm
from util import tokenize_words

def load(istream):
    data = []
    for line in istream:
        entry = line.rstrip().split()
        i = int(entry[0])
        data.append(i)
    return np.asarray(data)

def opts():
    parser = argparse.ArgumentParser(
        description='Compute fraction of correctly predicted missing words')
    parser.add_argument('golden', type=argparse.FileType('r'),
        help='File with reference missing positions')
    parser.add_argument('predicted', type=argparse.FileType('r'),
        help='File with predicted missing positions')
    parser.add_argument('--guessed-words', type=argparse.FileType('r'), 
        nargs='?', const=repeat('___'),
        help='File with predicted missing positions')
    parser.add_argument('--real-words', type=argparse.FileType('r'),
        help='File with actual missing words')
    parser.add_argument('--model',
        help='KenLM n-gram model file (ARPA or binary)')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    golden = load(args.golden)
    pred = load(args.predicted)
    if len(golden) != len(pred):
        print >>sys.stderr, "WARNING: %d golden positions != %d predicted positions" \
            % (len(golden), len(pred))
        n = min(len(golden), len(pred))
        golden = golden[:n]
        pred = pred[:n]
    print np.mean(golden == pred)

    if args.guessed_words or args.real_words:
        if args.model:
            print >>sys.stderr, "Loading language model"
            model = kenlm.LanguageModel(args.model)
            
        print >>sys.stderr, "Annotating sentences"
        for i, (sentence, guessed, actual) in enumerate(izip(sys.stdin, args.guessed_words, args.real_words)):
            if golden[i] != pred[i]: # errors
                sentence = sentence.rstrip()
                words = tokenize_words(sentence)
                
                if args.model: # add probability annotations
                    for j, (w, (p, _, _)) in enumerate(izip(words, model.full_scores(sentence))):
                        words[j] = '%s{%.2f}' % (w, p)
                
                # insert missing and correct word
                words.insert(pred[i], '__%s__' % guessed.strip())
                loc = golden[i]
                if golden[i] > pred[i]: loc += 1
                words.insert(loc, '**%s**' % actual.strip())
                
                print ' '.join(words)
