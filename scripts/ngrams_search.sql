SELECT w0.word, w1.word, w2.word, ngram.freq
FROM ngram
JOIN ngram_word nw0
  ON nw0.ngram_id=ngram.id
  AND nw0.ordinal=0
JOIN ngram_word nw1
  ON nw1.ngram_id=nw0.ngram_id
  AND nw1.ordinal=1
JOIN ngram_word nw2
  ON nw2.ngram_id=nw1.ngram_id
  AND nw2.ordinal=2
JOIN word w0 ON w0.id=nw0.word_id
JOIN word w1 ON w1.id=nw1.word_id
JOIN word w2 ON w2.id=nw2.word_id
WHERE ngram.n=3 AND w0.word='Jesus' OR w1.word='Jesus' OR w2.word='Jesus';

SELECT w0.word, w1.word, w2.word
FROM word w0
STRAIGHT_JOIN ngram_word nw0
ON nw0.word_id=w0.id
AND nw0.ordinal=0
INNER JOIN ngram_word nw1
ON nw1.ngram_id=nw0.ngram_id
AND nw1.ordinal=1
INNER JOIN ngram_word nw2
ON nw2.ngram_id=nw0.ngram_id
AND nw2.ordinal=2
INNER JOIN word w1 ON w1.id=nw1.word_id
INNER JOIN word w2 ON w2.id=nw2.word_id
WHERE w0.word='Jesus'
LIMIT 5;