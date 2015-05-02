#!/usr/bin/env python

import sys
from nltk.tree import Tree

print r"\documentclass[10pt]{article}"
print r"\usepackage[landscape]{geometry}"
print r"\usepackage{tikz-qtree}"
print r"\begin{document}"

for line in sys.stdin:
    tree = Tree.fromstring(line.rstrip())
    print r"\begin{tikzpicture}[scale=.5]"
    print tree.pprint_latex_qtree()
    print r"\end{tikzpicture}"
    print ""
    
print r"\end{document}"