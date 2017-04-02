import sqlite3 as lite
import sys

query_create = '''
CREATE TABLE IF NOT EXISTS category (
 id integer PRIMARY KEY,
 title text NOT NULL UNIQUE
) WITHOUT ROWID;
'''

query = '''
-- DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `cat_id` integer PRIMARY KEY,
  `cat_title` text NOT NULL UNIQUE,
  `cat_pages` integer NOT NULL DEFAULT '0',
  `cat_subcats` integer NOT NULL DEFAULT '0',
  `cat_files` integer NOT NULL DEFAULT '0'
) WITHOUT ROWID;
'''


query_create2 = '''
CREATE TABLE IF NOT EXISTS category_parent (
 category_id integer,
 parent_id integer,
 PRIMARY KEY (category_id, parent_id),
 FOREIGN KEY (category_id) REFERENCES category (id) 
 ON DELETE CASCADE ON UPDATE NO ACTION,
 FOREIGN KEY (parent_id) REFERENCES category (id) 
 ON DELETE CASCADE ON UPDATE NO ACTION
) WITHOUT ROWID;
'''

con = None

try:
    con = lite.connect('test.db')
    cur = con.cursor()
    cur.execute(query)
    # cur.execute(query_create2)
    # cur.execute('DROP TABLE Category')
    data = cur.fetchone()
    # print("SQLite version: %s" % data)

except lite.Error as e:
    print("Error %s:" % e.args[0])
    sys.exit(1)

finally:
    if con:
        con.close()
