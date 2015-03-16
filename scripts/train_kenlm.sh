# KenLM doesn't do unigrams
#~/Documents/Workspace/kenlm/bin/lmplz -o 1 -S 20% --vocab_file vocab.txt < train_v2.txt | ~/Documents/Workspace/kenlm/bin/build_binary -S 20% /dev/stdin 1-grams.kenlm
~/Documents/Workspace/kaggle/BillionWordImputation/scripts/BillionWordImputation/build/Release/count_unigrams < train_v2.txt | sort -k 2,2 -g -r -S 20% > 1-grams.txt

# trie
~/Documents/Workspace/kenlm/bin/lmplz -o 4 -S 20% --skip_symbols --vocab_estimate 10031 --text ../data/train.train.lower.reduce_vocab_10000.pos.txt --discount_fallback 0.5 1 1.5 | ~/Documents/Workspace/kenlm/bin/build_binary -S 20% trie /dev/stdin ../data/kenlm/4-grams.kenlm

~/Documents/Workspace/kenlm/bin/lmplz -o 5 -S 20% --skip_symbols --vocab_estimate 10031 --text ../data/train.train.lower.reduce_vocab_10000.pos.txt --discount_fallback 0.5 1 1.5 | ~/Documents/Workspace/kenlm/bin/build_binary -S 20% trie /dev/stdin ../data/kenlm/5-grams.kenlm

# quantized probing
~/Documents/Workspace/kenlm/bin/lmplz -o 4 -S 30% --skip_symbols --vocab_estimate 10031 --text ../data/train.train.lower.reduce_vocab_10000.pos.txt --discount_fallback 0.5 1 1.5 | ~/Documents/Workspace/kenlm/bin/build_binary -S 20% probing /dev/stdin ../data/kenlm/4-grams.probing.kenlm -q 8

~/Documents/Workspace/kenlm/bin/lmplz -o 5 -S 30% --skip_symbols --vocab_estimate 10031 --text ../data/train.train.lower.reduce_vocab_10000.pos.txt --discount_fallback 0.5 1 1.5 | ~/Documents/Workspace/kenlm/bin/build_binary -S 20% probing /dev/stdin ../data/kenlm/5-grams.probing.kenlm -q 8