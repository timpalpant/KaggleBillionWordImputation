#!/usr/bin/env python

'''
cat train_v2.txt | ../scripts/remove_random_word.py 2> train_v2.i_removed.txt 1> train_v2.removed.txt
'''

import sys, random
from util import is_punctuation, is_number, tokenize_words

def removable_words(words):
    return [i for i, w in enumerate(words)
        if len(w)>0 and not (is_punctuation(w) or is_number(w))]

def remove_random_word(line):
    '''
    Remove a random word from line, attempting to remove
    contractions whole and not punctuation / numbers.
    '''
    words = tokenize_words(line)
    choices = removable_words(words)
    if len(choices) == 0:
        return line
    selected = random.choice(choices)
    if words[selected].startswith("'"): 
        # second part of possessive/contraction
        words.pop(selected)
        words.pop(selected-1)
    elif selected+1 < len(words) and words[selected+1].startswith("'"): 
        # first part of possessive/contraction
        words.pop(selected+1)
        words.pop(selected)
    else: # regular word
        words.pop(selected)
    return ' '.join(words)

def remove_random_token(line, delim=' '):
    '''Remove a random space-delimited token from line'''
    words = line.rstrip().split(delim)
    if len(words) == 1:
        return 0, ''
    elif len(words) == 2:
        i = random.randint(0, 1)
    else:
        i = random.randint(1, len(words)-2)
    words.pop(i)
    return i, ' '.join(words)

if __name__ == '__main__':
    random.seed(123)
    for line in sys.stdin:
        i, s = remove_random_token(line)
        print s
        print >>sys.stderr, i