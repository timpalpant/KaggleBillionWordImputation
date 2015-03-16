#!/usr/bin/env python

import sys, argparse
import ngram

PROGRESS = 100000

WORD = ngram.load_table('word')
WORD_AI = max(WORD.itervalues()) if len(WORD) > 0 else 0
print >>sys.stderr, "Loaded %d words. Starting at word id %d" \
    % (len(WORD), WORD_AI)
def word_id(word, outfile):
    global WORD, WORD_AI
    word = word[:45]
    v = WORD.get(word, None)
    if v is None:
        WORD_AI += 1
        v = WORD_AI
        WORD[word] = v
        print >>outfile, '%d\t%s' % (v, ngram.db.escape_string(word))
    return v
    
POS = ngram.load_table('pos')
POS_AI = max(POS.itervalues()) if len(POS) > 0 else 0
print >>sys.stderr, "Loaded %d POS. Starting at pos id %d" \
    % (len(POS), POS_AI)
NGRAM_POS = ['NOUN', 'VERB', 'ADJ', 'ADV', 'PRON', 'DET', 'ADP', 'NUM', 
             'CONJ', 'PRT', 'X', '.']
             
def init_pos_key(pos_file):
    global NGRAM_POS, POS, POS_AI
    pos_key = {}
    for pos in NGRAM_POS:
        if pos in POS:
            pos_key[pos] = POS[pos]
        else:
            POS_AI += 1
            pos_key[pos] = POS_AI
            print >>pos_file, '%d\t%s' % (POS_AI, pos)
    return pos_key

def main(word_file, pos_file, ngram_file, ngram_word_file, ngram_ai=None):
    if ngram_ai is None:
        ngram_id = ngram.max_id('ngram')
    else: ngram_id = ngram_ai
    pos_key = init_pos_key(pos_file)
    pos_file.close()
    for line in sys.stdin:
        try:
            words, freq = line.rstrip().split('\t')
            ngram_id += 1
            words = words.split()
            print >>ngram_file, '%d\t%d\t%s' \
                % (ngram_id, len(words), freq)
                
            for i, word in enumerate(words):
                try:
                    w, pos = word.rsplit('_', 1)
                    pid = pos_key[pos]
                    wid = word_id(w, word_file)
                except: # no POS tag or invalid POS tag
                    wid = word_id(word, word_file)
                    pid = '\\N'
                print >>ngram_word_file, '%d\t%d\t%d\t%s' \
                    % (ngram_id, i, wid, pid)
            
            if ngram_id % PROGRESS == 0:
                print >>sys.stderr, ngram_id
        except Exception, e:
            print >>sys.stderr, e
            print line
    
def opts():
    parser = argparse.ArgumentParser(
        description='Convert ngrams to DB schema for bulk import')
    parser.add_argument('word_file', type=argparse.FileType('w'),
        help='word file')
    parser.add_argument('pos_file', type=argparse.FileType('w'),
        help='pos file')
    parser.add_argument('ngram_file', type=argparse.FileType('w'),
        help='ngram file')
    parser.add_argument('ngram_word_file', type=argparse.FileType('w'),
        help='ngram_word file')
    parser.add_argument('--ngram-ai', type=int,
        help='Autoincrement ID for first ngram')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    main(**vars(args))
