BWI=BillionWordImputation/build/Release/BillionWordImputation

for VOCAB_SIZE in 1000 5000 10000 20000 40000; do
  for N in {3..6}; do
    for TYPE in probing trie; do
      if [ -e ~/Tim/lm/models/${N}-grams.lower.vocab_${VOCAB_SIZE}.pos.${TYPE}.kenlm ]; then
        $BWI ~/Tim/lm/models/${N}-grams.lower.vocab_${VOCAB_SIZE}.pos.${TYPE}.kenlm < ~/Tim/lm/data/train.heldout.removed.lower.reduce_vocab_${VOCAB_SIZE}.pos.txt > ~/Tim/lm/predictions/train.heldout.removed.lower.reduce_vocab_${VOCAB_SIZE}.pos.txt
      fi
    
      if [ -e ~/Tim/lm/models/${N}-grams.lower.vocab_${VOCAB_SIZE}.pos.${TYPE}.kenlm ]; then
        $BWI ~/Tim/lm/models/${N}-grams.lower.vocab_${VOCAB_SIZE}.${TYPE}.kenlm < ~/Tim/lm/data/train.heldout.removed.lower.reduce_vocab_${VOCAB_SIZE}.txt > ~/Tim/lm/predictions/train.heldout.removed.lower.reduce_vocab_${VOCAB_SIZE}.txt
      fi
    
      if [ -e ~/Tim/lm/models/${N}-grams.lower.vocab_${VOCAB_SIZE}.pos.${TYPE}.kenlm ]; then
        $BWI ~/Tim/lm/models/${N}-grams.vocab_${VOCAB_SIZE}.pos.${TYPE}.kenlm < ~/Tim/lm/data/train.heldout.removed.reduce_vocab_${VOCAB_SIZE}.pos.txt > ~/Tim/lm/predictions/train.heldout.removed.reduce_vocab_${VOCAB_SIZE}.pos.txt
      fi
    
      if [ -e ~/Tim/lm/models/${N}-grams.lower.vocab_${VOCAB_SIZE}.pos.${TYPE}.kenlm ]; then
        $BWI ~/Tim/lm/models/${N}-grams.vocab_${VOCAB_SIZE}.${TYPE}.kenlm < ~/Tim/lm/data/train.heldout.removed.reduce_vocab_${VOCAB_SIZE}.txt > ~/Tim/lm/predictions/train.heldout.removed.reduce_vocab_${VOCAB_SIZE}.txt
      fi
    done
  done
done