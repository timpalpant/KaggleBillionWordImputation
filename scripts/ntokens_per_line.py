#!/usr/bin/env python

import sys
from util import tokenize_words

def num_tokens(line):
    words = tokenize_words(line)
    return len(words)

if __name__ == '__main__':
    for line in sys.stdin:
        print num_tokens(line)
