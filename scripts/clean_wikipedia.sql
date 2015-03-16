DELETE FROM page
WHERE page_namespace!=0;

ALTER TABLE page
ADD COLUMN redirect_to_page_id int(8) unsigned default null,
DROP COLUMN page_namespace,
DROP COLUMN page_restrictions,
DROP COLUMN page_counter,
DROP COLUMN page_is_new,
DROP COLUMN page_random,
DROP COLUMN page_touched,
DROP COLUMN page_len,
DROP COLUMN page_latest,
DROP COLUMN page_links_updated,
DROP COLUMN page_content_model,
DROP COLUMN page_is_redirect,
DROP COLUMN page_no_title_convert,
DROP KEY page_len,
DROP KEY page_random,
DROP KEY page_redirect_namespace_len;

# Merge redirects table
UPDATE page
INNER JOIN redirect ON redirect.rd_from=page.page_id
INNER JOIN page rd ON rd.page_title=redirect.rd_title
SET page.redirect_to_page_id=rd.page_id;

DROP TABLE redirect;

DELETE FROM pagelinks
WHERE pl_namespace!=0 OR pl_from_namespace!=0;

CREATE TABLE tmp (
  pl_from int(8) unsigned not null,
  pl_to int(8) unsigned not null,
  PRIMARY KEY (pl_from, pl_to)
);

INSERT INTO tmp
SELECT pagelinks.pl_from, page.page_id
FROM pagelinks
INNER JOIN page
ON page.page_title=pagelinks.pl_title;

DROP TABLE pagelinks;
RENAME TABLE tmp TO pagelinks;

ALTER TABLE pagelinks
ADD FOREIGN KEY (pl_from) REFERENCES page(page_id),
ADD FOREIGN KEY (pl_to) REFERENCES page(page_id);

# Delete self-links
DELETE FROM pagelinks
WHERE pl_from=pl_to;

# Delete links from redirects
DELETE pagelinks FROM pagelinks
INNER JOIN page ON page.page_id=pagelinks.pl_from
WHERE page.page_id!=page.redirect_to_page_id;

# Resolve redirects in links
# Ignore because after resolving redirects there may be duplicates
UPDATE IGNORE pagelinks
INNER JOIN page 
  ON page.page_id=pagelinks.pl_to
  AND page.page_id!=page.redirect_to_page_id
SET pl_to=page.redirect_to_page_id;
# Remove any remaining (duplicate) links to redirects
DELETE pagelinks FROM pagelinks
INNER JOIN page 
  ON page.page_id=pagelinks.pl_to
  AND page.page_id!=page.redirect_to_page_id;

# Remove redirects from pages
DELETE FROM page
WHERE page_id!=redirect_to_page_id;

ALTER TABLE page
DROP COLUMN redirect_to_page_id;