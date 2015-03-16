DROP TABLE IF EXISTS ngram_prefix;
CREATE TABLE IF NOT EXISTS ngram_prefix (
  id bigint unsigned not null,
  prefix_id bigint unsigned,
  word_id int unsigned not null,
  pos_id tinyint unsigned,
  freq bigint unsigned,
  UNIQUE KEY (prefix_id, word_id, pos_id)
);

INSERT INTO ngram_prefix (id, prefix_id, word_id, pos_id, freq)
SELECT ngram.id, NULL, ngram_word.word_id, ngram_word.pos_id, ngram.freq
FROM ngram
INNER JOIN ngram_word 
    ON ngram_word.ngram_id=ngram.id
    AND ngram_word.ordinal=0
WHERE ngram.n=1;

INSERT INTO ngram_prefix (id, prefix_id, word_id, pos_id, freq)
SELECT ngram.id, prefix.id, w1.word_id, w1.pos_id, ngram.freq
FROM ngram
INNER JOIN ngram_word w0
  ON w0.ngram_id=ngram.id AND w0.ordinal=0
INNER JOIN ngram_prefix prefix
  ON prefix.prefix_id IS NULL 
  AND prefix.word_id=w0.word_id 
  AND prefix.pos_id=w0.pos_id
INNER JOIN ngram_word w1
  ON w1.ngram_id=ngram.id AND w1.ordinal=1
WHERE ngram.n=2;

INSERT INTO ngram_prefix (id, prefix_id, word_id, pos_id, freq)
SELECT ngram.id, prefix.id, w2.word_id, w2.pos_id, ngram.freq
FROM ngram
INNER JOIN ngram_word w0
  ON w0.ngram_id=ngram.id AND w0.ordinal=0
INNER JOIN ngram_word w1
  ON w1.ngram_id=ngram.id AND w1.ordinal=1
INNER JOIN ngram_prefix p0
  ON p0.prefix_id IS NULL
  AND p0.word_id=w0.word_id
  AND p0.pos_id=w0.pos_id
INNER JOIN ngram_prefix prefix
  ON prefix.prefix_id=p0.id
  AND prefix.word_id=w1.word_id 
  AND prefix.pos_id=w1.pos_id
INNER JOIN ngram_word w2
  ON w2.ngram_id=ngram.id AND w2.ordinal=2
WHERE ngram.n=3;

INSERT INTO ngram_prefix (id, prefix_id, word_id, pos_id, freq)
SELECT ngram.id, prefix.id, w3.word_id, w3.pos_id, ngram.freq
FROM ngram
INNER JOIN ngram_word w0
  ON w0.ngram_id=ngram.id AND w0.ordinal=0
INNER JOIN ngram_word w1
  ON w1.ngram_id=ngram.id AND w1.ordinal=1
INNER JOIN ngram_word w2
  ON w2.ngram_id=ngram.id AND w2.ordinal=2
INNER JOIN ngram_prefix p0 
  ON p0.prefix_id IS NULL
  AND p0.word_id=w0.word_id
  AND p0.pos_id=w0.pos_id
INNER JOIN ngram_prefix p1
  ON p1.prefix_id=p0.id
  AND p1.word_id=w1.word_id
  AND p1.pos_id=w1.pos_id
INNER JOIN ngram_prefix prefix
  ON prefix.prefix_id=p1.id
  AND prefix.word_id=w2.word_id
  AND prefix.pos_id=w2.pos_id
INNER JOIN ngram_word w3
  ON w3.ngram_id=ngram.id AND w3.ordinal=3
WHERE ngram.n=4;

INSERT INTO ngram_prefix (id, prefix_id, word_id, pos_id, freq)
SELECT ngram.id, prefix.id, w4.word_id, w4.pos_id, ngram.freq
FROM ngram
INNER JOIN ngram_word w0
  ON w0.ngram_id=ngram.id AND w0.ordinal=0
INNER JOIN ngram_word w1
  ON w1.ngram_id=ngram.id AND w1.ordinal=1
INNER JOIN ngram_word w2
  ON w2.ngram_id=ngram.id AND w2.ordinal=2
INNER JOIN ngram_word w3
  ON w3.ngram_id=ngram.id AND w3.ordinal=3
INNER JOIN ngram_prefix p0
  ON p0.prefix_id IS NULL
  AND p0.word_id=w0.word_id
  AND p0.pos_id=w0.pos_id
INNER JOIN ngram_prefix p1
  ON p1.prefix_id=p0.id
  AND p1.word_id=w1.word_id
  AND p1.pos_id=w1.pos_id
INNER JOIN ngram_prefix p2
  ON p2.prefix_id=p1.id
  AND p2.word_id=w2.word_id
  AND p2.pos_id=w2.pos_id
INNER JOIN ngram_prefix prefix
  ON prefix.prefix_id=p2.id
  AND prefix.word_id=w3.word_id
  AND prefix.pos_id=w3.pos_id
INNER JOIN ngram_word w4
  ON w4.ngram_id=ngram.id AND w4.ordinal=4
WHERE ngram.n=5;

ALTER TABLE ngram_prefix (
  CHANGE COLUMN id id bigint unsigned not null auto_increment,
  ADD PRIMARY KEY (id),
  ADD FOREIGN KEY (word_id) REFERENCES word(id),
  ADD FOREIGN KEY (prefix_id) REFERENCES ngram_prefix(id)
);
