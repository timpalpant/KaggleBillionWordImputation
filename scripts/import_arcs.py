#!/usr/bin/env python

import sys
import ngram

BATCH_SIZE = 50000
ARC_N = 1 # nodes, biarcs, triarcs, etc.

if __name__ == "__main__":
    ARC_N = int(sys.argv[1])
    print >>sys.stderr, "Importing %d-arcs" % ARC_N

    ngram.cur.execute('SET autocommit=0')
    ngram.cur.execute('SET unique_checks=0')
    ngram.cur.execute('SET foreign_key_checks=0')

    for line_num, line in enumerate(sys.stdin):
        try:
            entry = line.strip().split('\t')
            freq = int(entry[2])
            ngram.cur.execute('INSERT INTO arc (n,freq) VALUES (%s,%s)', (ARC_N,freq))
            arc_id = ngram.cur.lastrowid

            words = entry[1].split()
            arc_words = []
            for i, word in enumerate(words):
                word, pos, dep, head_index = ngram.parse_word(word)
                wid = ngram.word_id(word)
                pid = ngram.pos_id(pos)
                did = ngram.dep_id(dep)
                arc_words.append((arc_id, i, wid, pid, did, head_index))
            ngram.cur.executemany(
                'INSERT INTO arc_word (arc_id, ordinal, word_id, pos_id, dep_id, head_index) ' \
                'VALUES (%s, %s, %s, %s, %s, %s)', arc_words)
            
            arc_freq = [(arc_id,) + tuple(field.split(','))
                        for field in entry[3:]]
            ngram.cur.executemany('INSERT IGNORE INTO arc_freq ' \
                                  'VALUES (%s,%s,%s)', arc_freq)
        except Exception, e:
            ngram.db.rollback()
            print >>sys.stderr, e
            print line
        else:
            ngram.db.commit()
            
        if line_num == BATCH_SIZE:
            print >>sys.stderr, line_num
            ngram.reset_caches()
