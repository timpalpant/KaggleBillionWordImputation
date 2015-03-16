SET UNIQUE_CHECKS=0;
SET FOREIGN_KEY_CHECKS=0;
SET SESSION tx_isolation='READ-UNCOMMITTED';
SET sql_log_bin=0;

LOAD DATA INFILE '/Volumes/Data/raw/ngram/nodes/pos.txt' INTO TABLE pos;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/nodes/dep.txt' INTO TABLE dep;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/nodes/word.txt' INTO TABLE word;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/nodes/arc.txt' INTO TABLE arc;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/nodes/arc_word.txt' INTO TABLE arc_word;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/nodes/arc_freq.txt' INTO TABLE arc_freq;

LOAD DATA INFILE '/Volumes/Data/raw/ngram/arcs/pos.txt' INTO TABLE pos;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/arcs/dep.txt' INTO TABLE dep;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/arcs/word.txt' INTO TABLE word;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/arcs/arc.txt' INTO TABLE arc;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/arcs/arc_word.txt' INTO TABLE arc_word;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/arcs/arc_freq.txt' INTO TABLE arc_freq;

LOAD DATA INFILE '/Volumes/Data/raw/ngram/biarcs/pos.txt' INTO TABLE pos;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/biarcs/dep.txt' INTO TABLE dep;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/biarcs/word.txt' INTO TABLE word;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/biarcs/arc.txt' INTO TABLE arc;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/biarcs/arc_word.txt' INTO TABLE arc_word;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/biarcs/arc_freq.txt' INTO TABLE arc_freq;

LOAD DATA INFILE '/Volumes/Data/raw/ngram/triarcs/pos.txt' INTO TABLE pos;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/triarcs/dep.txt' INTO TABLE dep;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/triarcs/word.txt' INTO TABLE word;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/triarcs/arc.txt' INTO TABLE arc;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/triarcs/arc_word.txt' INTO TABLE arc_word;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/triarcs/arc_freq.txt' INTO TABLE arc_freq;

LOAD DATA INFILE '/Volumes/Data/raw/ngram/quadarcs/pos.txt' INTO TABLE pos;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/quadarcs/dep.txt' INTO TABLE dep;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/quadarcs/word.txt' INTO TABLE word;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/quadarcs/arc.txt' INTO TABLE arc;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/quadarcs/arc_word.txt' INTO TABLE arc_word;
LOAD DATA INFILE '/Volumes/Data/raw/ngram/quadarcs/arc_freq.txt' INTO TABLE arc_freq;

SET UNIQUE_CHEKCS=1;
SET FOREIGN_KEY_CHECKS=1;
SET SESSION tx_isolation='READ-REPEATABLE';