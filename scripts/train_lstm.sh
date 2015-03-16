export PATH=/Users/timpalpant/Documents/Workspace/LSTM:$PATH
export PYTHONPATH=/Users/timpalpant/Documents/Workspace/LSTM/python-source:$PYTHONPATH

python /Users/timpalpant/Documents/Workspace/LSTM/lstm.py --train ../data/train.train.lower.txt ../data/train.heldout.lower.txt ../data/test.lower.txt --hidden 100 --independent --random-seed 123 --debug --cache 100 --cores 8 --save-net ../data/lstm/rnn.net

python /Users/timpalpant/Documents/Workspace/LSTM/python-source/make-lstm-lm.py ../data/train.train.lower.txt ../data/train.heldout.lower.txt 100