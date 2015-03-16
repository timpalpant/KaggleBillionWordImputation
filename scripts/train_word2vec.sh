# 2000 word classes
~/Documents/Workspace/word2vec/word2vec -train ../data/train.train.lower.txt -output ../data/train.train.lower.classes2000.txt -cbow 0 -size 200 -window 5 -negative 0 -hs 1 -sample 1e-3 -threads 8 -classes 2000
sort ../data/train.train.lower.classes2000.txt -k 2 -n > ../data/train.train.lower.classes2000.sorted.txt