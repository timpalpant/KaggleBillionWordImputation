import sys
from collections import defaultdict
from itertools import islice, izip
import numpy as np
from scipy.misc import logsumexp
import Levenshtein

PUNCTUATION = set(("'", '"', ',', '.', '!', '?', ';', ':', '-', '--', '(', ')', 
                   '/', '_', '\\', '+', '<', '>', '|', '@', '#', '$', '%', '^', 
                   '&', '*', '[', ']', '{', '}'))

POS_TAGS = set(('UH','WP$','PDT','RBS','LS','EX','WP','$','SYM','RP','CC','RBR','VBG','NNS','CD','PRP$','MD','DT','NNPS','VBD','IN','JJS','WRB','VBN','JJR','WDT','POS','TO','NNP','JJ','RB','VB','FW','PRP','VBZ','NN','VBP'))

UNKNOWN = '<unknown>'

def is_punctuation(word):
    return (word in PUNCTUATION)
    
def is_number(word):
    try: 
        x = float(word)
        return True
    except: 
        return False

def is_pos_tag(word):
    return (word in POS_TAGS)

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
    
def prune_vocab(vocab, n):
    nwords = sum(v for v in vocab.itervalues())
    nvocab = len(vocab)
    print >>sys.stderr, "Input has nwords = %s, vocab size = %d" \
        % (nwords, nvocab)
    vocab = [(v,k) for k,v in vocab.iteritems()]
    vocab = list(reversed(sorted(vocab)))
    vocab = vocab[:n]
    vocab = {k: v for v, k in vocab}
    nremaining = sum(v for v in vocab.itervalues())
    percent_kept = float(len(vocab)) / nvocab
    percent_mass = float(nremaining) / nwords
    print >>sys.stderr, "Keeping %d words (%.2f%% of vocab, %.2f%% of mass)" \
        % (len(vocab), 100*percent_kept, 100*percent_mass)
    return vocab
    
def score(golden, predicted):
    total_d = 0.0
    n = 0
    for ref, pred in izip(golden, predicted):
        total_d += Levenshtein.distance(ref, pred)
        n += 1
    return total_d / n
    
class Prediction(object):
    keep_top_n = 5
    
    def __init__(self, word, locations, Z, Z_location, *args):
        self.word = word
        self.locations = locations
        self.Z = Z
        self.Z_location = Z_location
        self.p_anywhere = args[:self.keep_top_n]
        self.p_at_location = args[self.keep_top_n:2*self.keep_top_n]
        self.p_at_other_location = args[2*self.keep_top_n:3*self.keep_top_n]
        self.p_surrounding = args[3*self.keep_top_n:]
        #assert self.p_anywhere[0] == self.p_at_location[0]
        #assert self.p_at_location[0] != self.p_at_other_location[0]
        
    @property
    def location(self):
        return self.locations[0]
        
    @property
    def order(self):
        return len(self.p_surrounding)
        
    @property
    def location_posterior(self):
        return 10.**(self.Z_location - self.Z)
        
    @property
    def word_posterior(self):
        return 10.**(self.p_at_location[0] - self.Z)
        
    @property
    def location_ratio(self):
        return self.p_at_location[0] - self.p_at_other_location[0]
        
    @property
    def word_ratio(self):
        return self.p_at_location[0] - self.p_at_location[1]
        
    @classmethod
    def parse(cls, line):
        entry = line.rstrip().split('\t')
        word = entry[0]
        # locations
        loc = map(int, entry[1:cls.keep_top_n])
        # probabilities
        for i in xrange(cls.keep_top_n+1, len(entry)):
            entry[i] = float(entry[i])
        return cls(word, loc, *entry[cls.keep_top_n+1:])