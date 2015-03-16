export PATH=/Users/timpalpant/Documents/Workspace/nplm/src:$PATH

prepareNeuralLM --train_text ../data/train.lower.txt --ngram_size 4 \
  --vocab_size 10000 \
  --train_file ../data/nplm/train.ngrams \
  --validation_size 10000 \
  --validation_file ../data/nplm/validation.ngrams

trainNeuralNetwork --train_file ../data/nplm/train.ngrams \
  --validation_file ../data/nplm/validation.ngrams \
  --words_file ../data/nplm/words \
  --num_epochs 10 --mmap_file 0 \
  --model_prefix ../data/nplm/model
  