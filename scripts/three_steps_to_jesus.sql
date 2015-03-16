# Pages with most incoming links
SELECT page.page_title, COUNT(*) AS c
FROM pagelinks
INNER JOIN page ON page.page_id=pagelinks.pl_to
GROUP BY page.page_id
ORDER BY c DESC
LIMIT 100;

# 1-hop links to Jesus
SELECT p1.page_title, page.page_title
FROM page
INNER JOIN pagelinks pl1 
  ON pl1.pl_to=page.page_id
INNER JOIN page p1 
  ON p1.page_id=pl1.pl_from
WHERE page.page_title='Jesus';

# 2-hop paths to Jesus
SELECT p2.page_title, p1.page_title, page.page_title
FROM page
INNER JOIN pagelinks pl1 
  ON pl1.pl_to=page.page_id
INNER JOIN page p1 
  ON p1.page_id=pl1.pl_from
INNER JOIN pagelinks pl2 
  ON pl2.pl_to=p1.page_id
  AND pl2.pl_from!=page.page_id # no cycles
INNER JOIN page p2 
  ON p2.page_id=pl2.pl_from
WHERE page.page_title='Jesus';

# 3-hop paths to Jesus
SELECT p3.page_title, p2.page_title, p1.page_title, page.page_title
FROM page
INNER JOIN pagelinks pl1 
  ON pl1.pl_to=page.page_id
INNER JOIN page p1 
  ON p1.page_id=pl1.pl_from
INNER JOIN pagelinks pl2 
  ON pl2.pl_to=p1.page_id
  AND pl2.pl_from!=page.page_id # no cycles
INNER JOIN page p2 
  ON p2.page_id=pl2.pl_from
INNER JOIN pagelinks pl3 
  ON pl3.pl_to=p2.page_id
  AND pl3.pl_from!=p1.page_id # no cycles
  AND pl3.pl_from!=page.page_id # no cycles
INNER JOIN page p3 
  ON p3.page_id=pl3.pl_from
WHERE page.page_title='Jesus';

# Total number of pages
SELECT COUNT(*) FROM page;
# 4666968

# Number of pages within 1 link
SELECT COUNT(*)
FROM page
INNER JOIN pagelinks ON pagelinks.pl_to=page.page_id
WHERE page.page_title='Jesus';
# 9997

# Number of pages within 2 links
SELECT COUNT(DISTINCT pl2.pl_from)
FROM page
INNER JOIN pagelinks pl1 
  ON pl1.pl_to=page.page_id
INNER JOIN pagelinks pl2 
  ON pl2.pl_to=pl1.pl_from
  AND pl2.pl_from!=page.page_id # no cycles
WHERE page.page_title='Jesus';
# 874508 distinct

# Number of pages within 3 links
SELECT COUNT(DISTINCT pl3.pl_from)
FROM page
INNER JOIN pagelinks pl1 
  ON pl1.pl_to=page.page_id
INNER JOIN pagelinks pl2 
  ON pl2.pl_to=pl1.pl_from
  AND pl2.pl_from!=page.page_id # no cycles
INNER JOIN pagelinks pl3 
  ON pl3.pl_to=pl2.pl_from
  AND pl3.pl_from!=pl1.pl_from # no cycles
  AND pl3.pl_from!=page.page_id # no cycles
WHERE page.page_title='Jesus';
# 4557781 distinct

# Page not within 3 links of Jesus
SELECT *
FROM page
WHERE page_id NOT IN (
  SELECT DISTINCT pagelinks.pl_from AS page_id
  FROM page
  INNER JOIN pagelinks ON pagelinks.pl_to=page.page_id
  WHERE page.page_title='Jesus'
  UNION
  SELECT DISTINCT pl2.pl_from
  FROM page
  INNER JOIN pagelinks pl1 
    ON pl1.pl_to=page.page_id
  INNER JOIN pagelinks pl2 
    ON pl2.pl_to=pl1.pl_from
  WHERE page.page_title='Jesus'
  UNION
  SELECT DISTINCT pl3.pl_from
  FROM page
  INNER JOIN pagelinks pl1 
    ON pl1.pl_to=page.page_id
  INNER JOIN pagelinks pl2 
    ON pl2.pl_to=pl1.pl_from
  INNER JOIN pagelinks pl3 
    ON pl3.pl_to=pl2.pl_from
  WHERE page.page_title='Jesus'
) LIMIT 500;

SELECT *
FROM page nojesus
LEFT JOIN page
LEFT JOIN pagelinks pl1 
  ON pl1.pl_to=page.page_id
LEFT JOIN pagelinks pl2 
  ON pl2.pl_to=pl1.pl_from
  AND pl2.pl_from!=page.page_id # no cycles
LEFT JOIN pagelinks pl3 
  ON pl3.pl_to=pl2.pl_from
  AND pl3.pl_from!=pl1.pl_from # no cycles
  AND pl3.pl_from!=page.page_id # no cycles
WHERE page.page_title='Jesus';

# Number of links through each directly connected page
SELECT p1.page_title, COUNT(*) AS c
FROM page
INNER JOIN pagelinks pl1 ON pl1.pl_to=page.page_id
INNER JOIN pagelinks pl2 ON pl2.pl_to=pl1.pl_from
INNER JOIN pagelinks pl3 ON pl3.pl_to=pl2.pl_from
INNER JOIN page p1 ON p1.page_id=pl1.pl_from
WHERE page.page_title='Jesus'
GROUP BY p1.page_id
ORDER BY c DESC
LIMIT 100;

# Number of links through each incoming 2 pages
SELECT p2.page_title, p1.page_title, COUNT(*) AS c
FROM page
INNER JOIN pagelinks pl1 ON pl1.pl_to=page.page_id
INNER JOIN pagelinks pl2 ON pl2.pl_to=pl1.pl_from
INNER JOIN pagelinks pl3 ON pl3.pl_to=pl2.pl_from
INNER JOIN page p1 ON p1.page_id=pl1.pl_from
INNER JOIN page p2 ON p2.page_id=pl2.pl_from
WHERE page.page_title='Jesus'
GROUP BY p1.page_id, p2.page_id
ORDER BY c DESC
LIMIT 100;

# Number of paths from A to Jesus
SELECT p3.page_title, p2.page_title, p1.page_title, page.page_title
FROM page
INNER JOIN pagelinks pl1 ON pl1.pl_to=page.page_id
INNER JOIN pagelinks pl2 ON pl2.pl_to=pl1.pl_from
INNER JOIN pagelinks pl3 ON pl3.pl_to=pl2.pl_from
INNER JOIN page p1 ON p1.page_id=pl1.pl_from
INNER JOIN page p2 ON p2.page_id=pl2.pl_from
INNER JOIN page p3 ON p3.page_id=pl3.pl_from
WHERE p3.page_title='Aviation' AND page.page_title='Jesus';

SELECT p2.page_title, p1.page_title, page.page_title
FROM page
INNER JOIN pagelinks pl1 ON pl1.pl_to=page.page_id
INNER JOIN pagelinks pl2 ON pl2.pl_to=pl1.pl_from
INNER JOIN page p1 ON p1.page_id=pl1.pl_from
INNER JOIN page p2 ON p2.page_id=pl2.pl_from
WHERE p2.page_title='Aviation' AND page.page_title='Jesus';

SELECT p1.page_title, page.page_title
FROM page
INNER JOIN pagelinks pl1 ON pl1.pl_to=page.page_id
INNER JOIN page p1 ON p1.page_id=pl1.pl_from
WHERE p1.page_title='Aviation' AND page.page_title='Jesus';

# Usage: the standard syntax:
#   WITH RECURSIVE recursive_table AS
#    (initial_SELECT
#     UNION ALL
#     recursive_SELECT)
#   final_SELECT;
# should be translated by you to 
# CALL WITH_EMULATOR(recursive_table, initial_SELECT, recursive_SELECT,
#                    final_SELECT, 0, "").

# ALGORITHM:
# 1) we have an initial table T0 (actual name is an argument
# "recursive_table"), we fill it with result of initial_SELECT.
# 2) We have a union table U, initially empty.
# 3) Loop:
#   add rows of T0 to U,
#   run recursive_SELECT based on T0 and put result into table T1,
#   if T1 is empty
#      then leave loop,
#      else swap T0 and T1 (renaming) and empty T1
# 4) Drop T0, T1
# 5) Rename U to T0
# 6) run final select, send relult to client

# This is for *one* recursive table.
# It would be possible to write a SP creating multiple recursive tables.

delimiter |

CREATE PROCEDURE WITH_EMULATOR(
recursive_table varchar(100), # name of recursive table
initial_SELECT varchar(65530), # seed a.k.a. anchor
recursive_SELECT varchar(65530), # recursive member
final_SELECT varchar(65530), # final SELECT on UNION result
max_recursion int unsigned, # safety against infinite loop, use 0 for default
create_table_options varchar(65530) # you can add CREATE-TABLE-time options
# to your recursive_table, to speed up initial/recursive/final SELECTs; example:
# "(KEY(some_column)) ENGINE=MEMORY"
)

BEGIN
  declare new_rows int unsigned;
  declare show_progress int default 0; # set to 1 to trace/debug execution
  declare recursive_table_next varchar(120);
  declare recursive_table_union varchar(120);
  declare recursive_table_tmp varchar(120);
  set recursive_table_next  = concat(recursive_table, "_next");
  set recursive_table_union = concat(recursive_table, "_union");
  set recursive_table_tmp   = concat(recursive_table, "_tmp");
  # If you need to reference recursive_table more than
  # once in recursive_SELECT, remove the TEMPORARY word.
  SET @str = # create and fill T0
    CONCAT("CREATE TEMPORARY TABLE ", recursive_table, " ",
    create_table_options, " AS ", initial_SELECT);
  PREPARE stmt FROM @str;
  EXECUTE stmt;
  SET @str = # create U
    CONCAT("CREATE TEMPORARY TABLE ", recursive_table_union, " LIKE ", recursive_table);
  PREPARE stmt FROM @str;
  EXECUTE stmt;
  SET @str = # create T1
    CONCAT("CREATE TEMPORARY TABLE ", recursive_table_next, " LIKE ", recursive_table);
  PREPARE stmt FROM @str;
  EXECUTE stmt;
  if max_recursion = 0 then
    set max_recursion = 100; # a default to protect the innocent
  end if;
  recursion: repeat
    # add T0 to U (this is always UNION ALL)
    SET @str =
      CONCAT("INSERT INTO ", recursive_table_union, " SELECT * FROM ", recursive_table);
    PREPARE stmt FROM @str;
    EXECUTE stmt;
    # we are done if max depth reached
    set max_recursion = max_recursion - 1;
    if not max_recursion then
      if show_progress then
        select concat("max recursion exceeded");
      end if;
      leave recursion;
    end if;
    # fill T1 by applying the recursive SELECT on T0
    SET @str =
      CONCAT("INSERT INTO ", recursive_table_next, " ", recursive_SELECT);
    PREPARE stmt FROM @str;
    EXECUTE stmt;
    # we are done if no rows in T1
    select row_count() into new_rows;
    if show_progress then
      select concat(new_rows, " new rows found");
    end if;
    if not new_rows then
      leave recursion;
    end if;
    # Prepare next iteration:
    # T1 becomes T0, to be the source of next run of recursive_SELECT,
    # T0 is recycled to be T1.
    SET @str =
      CONCAT("ALTER TABLE ", recursive_table, " RENAME ", recursive_table_tmp);
    PREPARE stmt FROM @str;
    EXECUTE stmt;
    # we use ALTER TABLE RENAME because RENAME TABLE does not support temp tables
    SET @str =
      CONCAT("ALTER TABLE ", recursive_table_next, " RENAME ", recursive_table);
    PREPARE stmt FROM @str;
    EXECUTE stmt;
    SET @str =
      CONCAT("ALTER TABLE ", recursive_table_tmp, " RENAME ", recursive_table_next);
    PREPARE stmt FROM @str;
    EXECUTE stmt;
    # empty T1
    SET @str =
      CONCAT("TRUNCATE TABLE ", recursive_table_next);
    PREPARE stmt FROM @str;
    EXECUTE stmt;
  until 0 end repeat;
  # eliminate T0 and T1
  SET @str =
    CONCAT("DROP TEMPORARY TABLE ", recursive_table_next, ", ", recursive_table);
  PREPARE stmt FROM @str;
  EXECUTE stmt;
  # Final (output) SELECT uses recursive_table name
  SET @str =
    CONCAT("ALTER TABLE ", recursive_table_union, " RENAME ", recursive_table);
  PREPARE stmt FROM @str;
  EXECUTE stmt;
  # Run final SELECT on UNION
  SET @str = final_SELECT;
  PREPARE stmt FROM @str;
  EXECUTE stmt;
  # No temporary tables may survive:
  SET @str =
    CONCAT("DROP TEMPORARY TABLE ", recursive_table);
  PREPARE stmt FROM @str;
  EXECUTE stmt;
  # We are done :-)
END|

delimiter ;