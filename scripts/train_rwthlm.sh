The parameter NETWORK specifies the architecture of the neural network LM as well as the file name at the same time. The format is "name-layer1-layer2-...". Here, "name" can be chosen arbitrarily, but may not contain a dash ("-"). The hidden layers ("layer1", "layer2", ...) are separated by dashes "-", the first character specifies the type of the layer, the number indicates the size of the layer. The available layer types are:

'i': linear layer with identity activation function (must be the first layer)
'2'-'9': feedforward input layer with 2, ..., 9 history words (must be the first layer)
'l': linear layer with tanh activation function
'L': linear layer with sigmoid activation function
'r': recurrent layer with tanh activation function
'R': recurrent layer with sigmoid activation function
'm' or 'M': LSTM layer (may not be the first layer)
Examples: The argument "example1-i300-m300" creates a network with a linear layer and a subsequent LSTM layer, each comprising 300 neurons. The network "example2-7700-L100" is an 8-gram feedforward network with a linear layer of size 100 (for each of the 7 input words) and a hidden layer of size 100 with a sigmoid activation function. In all cases, the output layer is appended automatically.

# Train FF network
~/Documents/Workspace/rwthlm-0.11/rwthlm ff-4400-L100 \
  --vocab ../data/train.train.lower.vocab.10000.txt --unk \
  --train ../data/train.train.lower.reduce_vocab_10000.pos.txt \
  --dev ../data/train.heldout.lower.reduce_vocab_10000.pos.txt \
  --random-seed 123 \
  --batch-size 32 --feedforward --learning-rate 5e-4 \
  --no-shuffling --word-wrapping fixed --verbose

# Train LSTM network
~/Documents/Workspace/rwthlm-0.11/rwthlm lstm-i256-m256 \
  --vocab ../data/train.train.lower.vocab.10000.txt --unk \
  --train ../data/train.train.lower.reduce_vocab_10000.pos.txt \
  --dev ../data/train.heldout.lower.reduce_vocab_10000.pos.txt \
  --random-seed 123 \
  --batch-size 32 --learning-rate 5e-4 \
  --no-shuffling --word-wrapping fixed --verbose

Timothys-MBP:scripts timpalpant$ ~/Documents/Workspace/rwthlm-0.11/rwthlm lstm-i2048-m512 \
>   --vocab ../data/train.train.lower.vocab.10000.txt --unk \
>   --train ../data/train.train.lower.reduce_vocab_10000.pos.txt \
>   --dev ../data/train.heldout.lower.reduce_vocab_10000.pos.txt \
>   --random-seed 123 \
>   --batch-size 32 --learning-rate 5e-4 \
>   --no-shuffling --word-wrapping fixed --verbose
Reading vocabulary from file '../data/train.train.lower.vocab.10000.txt' ...
Randomly initializing neural network weights ...
Reading development data from file '../data/train.heldout.lower.reduce_vocab_10000.pos.txt' ...
Reading training data from file '../data/train.train.lower.reduce_vocab_10000.pos.txt' ...
Training ...
training perplexity = 11574.83
time = 99.521 seconds / batch = > 3 years for 29M sentences
^C
Timothys-MBP:scripts timpalpant$ ~/Documents/Workspace/rwthlm-0.11/rwthlm lstm-i256-m256 \
>   --vocab ../data/train.train.lower.vocab.10000.txt --unk \
>   --train ../data/train.train.lower.reduce_vocab_10000.pos.txt \
>   --dev ../data/train.heldout.lower.reduce_vocab_10000.pos.txt \
>   --random-seed 123 \
>   --batch-size 32 --learning-rate 5e-4 \
>   --no-shuffling --word-wrapping fixed --verbose
Reading vocabulary from file '../data/train.train.lower.vocab.10000.txt' ...
Randomly initializing neural network weights ...
Reading development data from file '../data/train.heldout.lower.reduce_vocab_10000.pos.txt' ...
Reading training data from file '../data/train.train.lower.reduce_vocab_10000.pos.txt' ...
Training ...
training perplexity = 10526.36
time = 38.148 seconds / batch = ~ 1 year for 29M sentences

# Train LSTM network with word2vec classes
~/Documents/Workspace/rwthlm-0.11/rwthlm w2vlstm-i300-m300 \
  --vocab ../data/word2vec/train.train.lower.classes.2000.txt --unk \
  --train ../data/train.train.lower.reduce_vocab_10000.pos.txt \
  --dev ../data/train.heldout.lower.reduce_vocab_10000.pos.txt \
  --random-seed 123 \
  --batch-size 32 --learning-rate 5e-4 \
  --no-shuffling --word-wrapping fixed --verbose