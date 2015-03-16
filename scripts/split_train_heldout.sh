head -n 1000000 ../data/train_v2.txt > ../data/train.heldout.txt
tail -n+1000001 ../data/train_v2.txt > ../data/train.train.txt
./remove_random_word.py < ../data/train.heldout.txt 1> ../data/train.heldout.removed.txt 2> ../data/train.heldout.i_removed.txt
./insert_blanks.py ../data/train.heldout.removed.txt ../data/train.heldout.i_removed.txt > ../data/train.heldout.madlib.txt
