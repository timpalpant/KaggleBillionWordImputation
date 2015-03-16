export PATH=/Users/timpalpant/Documents/Workspace/rnnlm-0.4b:$PATH

rnnlm -train ../data/train.train.lower.reduce_vocab_10000.pos.1-72000.txt -class 1000 -rnnlm ../data/rnnlm/model.classes1000 -binary -valid ../data/train.heldout.lower.reduce_vocab_10000.pos.1-72000.txt -hidden 30 -alpha 0.1 -beta 1e-7 -bptt 4 -independent

rnnlm -train ../data/train.train.lower.reduce_vocab_10000.pos.txt \
  -rnnlm ../data/rnnlm/model.128hidden -anti-kasparek 100000 \
  -valid ../data/train.heldout.lower.reduce_vocab_10000.pos.txt \
  -hidden 128 -alpha 0.1 -beta 1e-7 -bptt 4 -independent \
  -direct 5000 -direct-order 3 -binary