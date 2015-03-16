#!/usr/bin/env python

import sys, argparse
import ngram

PROGRESS = 500000

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
        print >>outfile, '%d\t%s' % (v, word)
    return v
    
POS = ngram.load_table('pos')
POS_AI = max(POS.itervalues()) if len(POS) > 0 else 0
print >>sys.stderr, "Loaded %d POS. Starting at pos id %d" \
    % (len(POS), POS_AI)
NGRAM_POS = set(['NOUN', 'VERB', 'ADJ', 'ADV', 'PRON', 'DET', 'ADP', 'NUM', 
                 'CONJ', 'PRT', 'X', '.'])
def pos_id(tag, outfile):
    global POS, POS_AI, NGRAM_POS
    if tag not in NGRAM_POS:
        raise ValueError("Not a POS tag")
    v = POS.get(tag, None)
    if v is None:
        POS_AI += 1
        v = POS_AI
        print >>outfile, '%d\t%s' % (v, tag)
    return v

def main(word_file, pos_file, ngram_file, ngram_word_file, ngram_freq_file):
    ngram_id = ngram.max_id('ngram')
    ngram.cur.close()
    ngram.db.close()
    cur_ngram = None
    total_freq = 0
    for line in sys.stdin:
        try:
            entry = line.rstrip().split('\t')
            if entry[0] != cur_ngram: # new n-gram, import words
                # Write previous ngram to file
                if cur_ngram is not None:
                    print >>ngram_file, '%d\t%d\t%d' \
                        % (ngram_id, len(words), total_freq)
                
                cur_ngram = entry[0]
                ngram_id += 1
                total_freq = 0
                words = entry[0].split()
                if ngram_id % PROGRESS == 0:
                    print >>sys.stderr, ngram_id
                
                for i, word in enumerate(words):
                    try: 
                        word, pos = word.split('_')
                        pid = pos_id(pos, pos_file)
                    except: 
                        pid = 'NULL'
                    finally:
                        wid = word_id(word, word_file)
                    print >>ngram_word_file, '%d\t%d\t%d\t%s' \
                        % (ngram_id, i, wid, pid)
                
            #year = entry[1]
            freq = int(entry[2])
            #vol = entry[3]
            #print >>ngram_freq_file, '%d\t%s\t%d\t%s' % (ngram_id, year, freq, vol)
            total_freq += freq
        except Exception, e:
            print >>sys.stderr, e
            print line
            
    # The last ngram
    print >>ngram_file, '%d\t%d\t%d' \
        % (ngram_id, len(words), total_freq)
    
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
    parser.add_argument('ngram_freq_file', type=argparse.FileType('w'),
        help='ngram_freq file')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    main(**vars(args))
