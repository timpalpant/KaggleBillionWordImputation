CREATE TABLE page_text ( 
  page_id int(8) unsigned not null, 
  page_text text,
  primary key (page_id)
);

DATADIR=/Volumes/Data/raw/wikipedia/
clang++ -O3 -o wikidump_to_sql wikidump_to_sql.cpp
pbunzip2 -d -c $DATADIR/enwiktionary-20140819-pages-articles.xml.bz2 | ./wikidump_to_sql | mysql -u timpalpant -p wiktionary

DELETE page_text FROM page_text
LEFT JOIN page ON page.page_id=page_text.page_id
WHERE page.page_id IS NULL;

ALTER TABLE page_text
ADD FOREIGN KEY (page_id) REFERENCES page(page_id),
ADD FULLTEXT KEY (page_text);