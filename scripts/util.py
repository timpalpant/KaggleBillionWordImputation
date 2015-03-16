import sys
from collections import defaultdict
from itertools import islice
import numpy as np
from scipy.misc import logsumexp

PUNCTUATION = set(("'", '"', ',', '.', '!', '?', ';', ':', '-', '--', '(', ')', 
                   '/', '_', '\\', '+', '<', '>', '|', '@', '#', '$', '%', '^', 
                   '&', '*', '[', ']', '{', '}'))

def is_punctuation(word):
    return (word in PUNCTUATION)
    
def is_number(word):
    try: 
        x = float(word)
        return True
    except: 
        return False

def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result    
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def tokenize_words(line, delim=' '):
    return line.rstrip().split(delim)
    
def pos_tag(word):
    return word.rsplit('_', 1)[-1]
    
def normalize_ngrams(ngrams):
    for k, v in ngrams.iteritems():
        ngrams[k] = np.log10(v)
    total = logsumexp(ngrams.values())
    for k, v in ngrams.iteritems():
        ngrams[k] -= total
    return ngrams
    
def ngram_frequencies(istream, n=1):
    counts = defaultdict(int)
    for i, line in enumerate(istream):
        if i % 100000 == 0:
            print >>sys.stderr, i
        words = tokenize_words(line)
        for ngram in window(words, n):
            counts[ngram] += 1
    return counts
    
def words2ids(words, idmap):
    ids = []
    for word in words:
        if word not in idmap:
            idmap[word] = len(idmap)
        ids.append(idmap[word])
    return ids
    
def ngram_frequencies2(istream, n=1):
    unigrams = dict()
    counts = defaultdict(int)
    for i, line in enumerate(istream):
        if i % 100000 == 0:
            print >>sys.stderr, "Line %d (%d 1-grams, %d %d-grams)" \
                % (i, len(unigrams), len(counts), n)
        words = tokenize_words(line)
        ids = words2ids(words, unigrams)
        for ngram in window(ids, n):
            counts[ngram] += 1
    id2word = {v: k for k, v in unigrams.iteritems()}
    del unigrams
    return counts, id2word
    
def load_vocab(vocab_file):
    vocab = {}
    for line in vocab_file:
        word, freq = line.strip().split()
        freq = int(freq)
        vocab[word] = freq
    return vocab