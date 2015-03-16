#!/bin/bash

# Berkeley Parser
cat train_v2.txt | java -server -Xmx6g -jar ~/Documents/Workspace/berkeley-parser/BerkeleyParser-1.7.jar -nThreads 8 -tokenize -kbest 1 -gr ~/Documents/Workspace/berkeley-parser/eng_sm6.gr >> train_v2.berkeley.txt
# Train a new grammar on the trees with one word removed
java -server -Xmx6g -cp ~/Documents/Workspace/berkeley-parser/BerkeleyParser-1.7.jar edu.berkeley.nlp.PCFGLA.GrammarTrainer -out grammar.gr -treebank SINGLEFILE -path train_v2.berkeley.removed.txt -trfr 0.9

# Stanford Parser
cat train_v2.txt | java -server -Xmx12g -cp "/usr/local/Cellar/stanford-parser/3.4/libexec/*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat oneline -maxLength 70 -sentences newline -nthreads -1 edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz - > train_v2.stanford.txt
# Train a new grammar on the trees with one word removed
java -server -Xmx6g -cp "/usr/local/Cellar/stanford-parser/3.4/libexec/*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -wordFunction edu.stanford.nlp.process.AmericanizeFunction -evals "factDA,tsv" -goodPCFG -saveToSerializedFile englishPCFG.ser.gz -maxLength 70 -nthreads -1 -train train_v2.berkeley.txt

# Apache OpenNLP
cat train_v2.txt | ~/Documents/Workspace/apache-opennlp-1.5.3/bin/opennlp Parser -k 1 ~/Documents/Workspace/apache-opennlp-1.5.3/models/en-parser-chunking.bin | pbzip2 -c > train_v2.opennlp.txt.bz2
# Train a new grammar on the trees with one word removed
~/Documents/Workspace/apache-opennlp-1.5.3/bin/opennlp ParserTrainer -headRules head_rules -lang en -parserType CHUNKING -model en-removed-chunking.bin -data train_v2.opennlp.txt

# Stanford CoreNLP
#~/Documents/Workspace/corenlp-python/stanford-corenlp-full-2014-08-27/corenlp.sh -maxLength 70 -sentences newline -nthreads 8 edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz

# Puck
java -server -Xmx4g -cp puck-assembly-0.1.jar puck.parser.CompileGrammar --textGrammarPrefix textGrammars/wsj_1.gr:textGrammars/wsj_6.gr --grammar grammar.grz
pbunzip2 -c train_v2.txt.bz2 | java -server -Xmx12g -cp ~/Documents/Workspace/puck/puck-assembly-0.1.jar puck.parser.RunParser --grammar ~/Documents/Workspace/puck/grammar.grz --maxLength 70 --mem 12g | pbzip2 -c > train_v2.puck.txt.bz2