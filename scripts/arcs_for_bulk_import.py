#!/usr/bin/env python

import sys, argparse
import ngram

PROGRESS = 1000000

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
    
def cached_lookup(key, cache, outfile):
    v = cache.get(key, None)
    if v is None:
        v = max(cache.itervalues()) + 1
        print >>outfile, '%d\t%s' % (v, ngram.db.escape_string(key))
        cache[key] = v
    return v
    
DEP = ngram.load_table('dep')
DEP[None] = 0
def dep_id(label, outfile):
    return cached_lookup(label, DEP, outfile)
    
POS = ngram.load_table('pos')
POS[None] = 0
def pos_id(tag, outfile):
    return cached_lookup(tag, POS, outfile)

def main(word_file, pos_file, dep_file, arc_file, arc_word_file, n):
    print >>sys.stderr, "Processing %d-arcs" % n

    arc_id = ngram.max_id('arc') + 1
    for line in sys.stdin:
        try:
            entry = line.strip().split('\t', 3)
            freq = entry[2]
            print >>arc_file, '%d\t%d\t%s' % (arc_id, n, freq)

            words = entry[1].split()
            for i, word in enumerate(words):
                word, pos, dep, head_index = ngram.parse_word(word)
                wid = word_id(word, word_file)
                pid = pos_id(pos, pos_file)
                did = dep_id(dep, dep_file)
                print >>arc_word_file, '%d\t%d\t%d\t%d\t%d\t%s' \
                    % (arc_id, i, wid, pid, did, head_index)
            
#            if not skip_years:
#                for field in entry[3].split('\t'):
#                    year, count = field.split(',')
#                    print >>arc_freq_file, '%d\t%s\t%s' % (arc_id, year, count)
        except Exception, e:
            print >>sys.stderr, e
            print line
        else:
            arc_id += 1
            
        if arc_id % PROGRESS == 0:
            print >>sys.stderr, arc_id
    
def opts():
    parser = argparse.ArgumentParser(
        description='Convert syntactic ngrams to DB schema for bulk import')
    parser.add_argument('word_file', type=argparse.FileType('w'),
        help='word file')
    parser.add_argument('pos_file', type=argparse.FileType('w'),
        help='pos file')
    parser.add_argument('dep_file', type=argparse.FileType('w'),
        help='dep file')
    parser.add_argument('arc_file', type=argparse.FileType('w'),
        help='arc file')
    parser.add_argument('arc_word_file', type=argparse.FileType('w'),
        help='arc_word file')
#    parser.add_argument('arc_freq_file', type=argparse.FileType('w'),
#        help='arc_freq file')
    parser.add_argument('-n', type=int, default=1,
        help='Arc length (n-grams)')
#    parser.add_argument('--skip-years', action='store_true',
#        help='Do not produce arc_freq table broken down by years')
    return parser

if __name__ == "__main__":
    args = opts().parse_args()
    main(**vars(args))
