#!/bin/bash

# Stanford POS Tagger
CORENLP=/Users/timpalpant/Documents/Workspace/corenlp-python/stanford-corenlp-full-2014-08-27
CORENLP_MODELS=${CORENLP}/edu/stanford/nlp/models
POS_MODEL=${CORENLP_MODELS}/pos-tagger/english-left3words/english-left3words-distsim.tagger
java -server -Xmx4g -cp ${CORENLP}/stanford-corenlp-3.4.1.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model ${POS_MODEL} -textFile train_v2.txt -tokenize false -nthreads 8 > train_v2.pos.txt

java -server -Xmx4g -cp ${CORENLP}/stanford-corenlp-3.4.1.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model ${POS_MODEL} -textFile train_v2.removed.txt -tokenize false -nthreads 8 > train_v2.pos.removed.txt

# The Stanford Tagger skips empty lines; add them back
grep -e '^$' -n train_v2.removed.txt | cut -f 1 -d : > train_v2.removed.i_empty.txt
cat train_v2.pos.removed.txt | ../scripts/add_empty_lines.py train_v2.removed.i_empty.txt > tmp
mv tmp train_v2.pos.removed.txt

java -server -Xmx4g -cp ${CORENLP}/stanford-corenlp-3.4.1.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model ${POS_MODEL} -textFile test_v2.trainfmt.txt -tokenize false -nthreads 8 > test_v2.pos.txt

# The Stanford Tagger skips empty lines; add them back
grep -e '^$' -n test_v2.txt | cut -f 1 -d : > test_v2.i_empty.txt
cat test_v2.pos.txt | ../scripts/add_empty_lines.py test_v2.i_empty.txt > tmp
mv tmp test_v2.pos.txt