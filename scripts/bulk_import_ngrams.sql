myisamchk --keys-used=0 -pq --key-buffer-size=8G --sort-buffer-size=2G --myisam-sort-buffer-size=2G --read-buffer-size=8M --write-buffer-size=8M --tmpdir=/tmp /Volumes/Data/mysql/ngram/ngram_word
myisamchk -pq --key-buffer-size=8G --sort-buffer-size=2G --myisam-sort-buffer-size=2G --read-buffer-size=8M --write-buffer-size=8M --tmpdir=/tmp /Volumes/Data/mysql/ngram/ngram_word

SET UNIQUE_CHECKS=0;
SET FOREIGN_KEY_CHECKS=0;
SET SESSION tx_isolation='READ-UNCOMMITTED';
SET sql_log_bin=0;
SET SESSION myisam_sort_buffer_size = 2*1024*1024*1024;

LOAD DATA INFILE '/Volumes/Data/raw/ngram/3-grams/pos.txt' INTO TABLE pos;
ALTER TABLE word DISABLE KEYS;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/3-grams/word.txt' INTO TABLE word;
ALTER TABLE word ENABLE KEYS;
ALTER TABLE ngram DISABLE KEYS;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/3-grams/ngram.txt' INTO TABLE ngram;
ALTER TABLE ngram ENABLE KEYS;
ALTER TABLE ngram_word DISABLE KEYS;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/3-grams/ngram_word.txt' INTO TABLE ngram_word;
ALTER TABLE ngram_word ENABLE KEYS;
#LOAD DATA INFILE '/Volumes/Data/raw/ngram/1-grams/ngram_freq.txt' INTO TABLE ngram_freq;

SET UNIQUE_CHEKCS=1;
SET FOREIGN_KEY_CHECKS=1;
SET SESSION tx_isolation='READ-REPEATABLE';