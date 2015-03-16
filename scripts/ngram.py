import MySQLdb

db = MySQLdb.connect(host='localhost',
                     user='timpalpant',
                     passwd='JScript',
                     db='ngram')
cur = db.cursor()

def cached_query(stmt, value, cache):
    v = cache.get(value, None)
    if v is None:
        cur.execute(stmt, (value,))
        id = cur.fetchone()
        if id is not None: id = id[0]
        cache[value] = id
        return id
    return v

WORDS = {}
def word_id(word):
    id = cached_query('SELECT id FROM word WHERE word=%s', word[:45], WORDS)
    if id is None:
        cur.execute('INSERT INTO word (word) VALUES (%s)', (word,))
        id = cur.lastrowid
    return id
        
POS = {}
def pos_id(tag):
    id = cached_query('SELECT id FROM pos WHERE tag=%s', tag, POS)
    if id is None:
        cur.execute('INSERT INTO pos (tag) VALUES (%s)', (tag,))
        id = cur.lastrowid
    return id

DEP = {}    
def dep_id(label):
    id = cached_query('SELECT id FROM dep WHERE label=%s', label, DEP)
    if id is None:
        cur.execute('INSERT INTO dep (label) VALUES (%s)', (label,))
        id = cur.lastrowid
    return id
    
def reset_caches():
    WORDS.clear()
    
def parse_word(w):
    parts = w.rsplit('/', 3)
    word = parts[0] # word may contain /
    pos = parts[1]
    dep = parts[2]
    head_index = parts[3]
    return word, pos, dep, head_index

def max_id(table):
    cur.execute('SELECT MAX(id) FROM %s' % table)
    r = cur.fetchone()[0]
    if r is None: return 0
    else: return r
    
def load_table(table):
    cur.execute('SELECT * FROM %s' % table)
    return {r[1]: r[0] for r in cur}
    
def frequency(*words):
    '''Return the frequency of the given ngram @words'''
    stmt = ['SELECT ngram.freq FROM ngram']
    stmt += ['INNER JOIN ngram_word nw%d ' \
             'ON nw%d.ngram_id=ngram.id ' \
             'AND nw%d.ordinal=%d' % (i,i,i,i)
             for i, w in enumerate(words)]
    stmt += ['INNER JOIN word w%d ' \
             'ON w%d.id=nw%d.word_id ' \
             'AND w%d.word="%s"' % (i,i,i,i,w)
             for i, w in enumerate(words)]
    stmt += ['WHERE n=%d' % len(words)]
    #print '\n'.join(stmt)
    cur.execute(' '.join(stmt))
    result = cur.fetchone()
    if result is None:
        return 0
    return result[0]