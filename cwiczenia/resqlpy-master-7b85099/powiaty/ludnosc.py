# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import sys
import re
import io
import sqlite3

woj_re = re.compile(r'^[#][#]WOJ \s* , \s* ([\w-]+) \s*$', re.X|re.U)
pow_re = re.compile(r'''^((?:m\. \s+ (?:st\. \s+ )?)? [\w -]+?) \s* ,
                        \s* (\d+) \s*$''', re.X|re.U)

DBNAME = 'ludność.sqlite'

def dbfill(db, lines):
    for num, line in enumerate(lines):
        m = woj_re.match(line)
        if m:
            woj = m.group(1)
            db.execute('''INSERT INTO wojewodztwa VALUES (?)''',
                       (woj,))
            continue

        m = pow_re.match(line)
        if not m:
            raise ValueError("błąd l. {}: {!r}".format(num, line))
        pow, pop = m.group(1), int(m.group(2))
        try:
            db.execute('''INSERT INTO powiaty VALUES (?, ?, ?)''',
                       (pow, pop, woj))
        except sqlite3.IntegrityError:
            raise ValueError("błąd l. {}: {!r}".format(num, line))

def dbinit(db):
    db.execute('''DROP TABLE IF EXISTS powiaty''')
    db.execute('''DROP TABLE IF EXISTS wojewodztwa''')

    db.execute('''CREATE TABLE wojewodztwa (
                       wojewodztwo TEXT PRIMARY KEY
               )''')
    db.execute('''CREATE TABLE powiaty (
                       powiat TEXT,
                       populacja INTEGER NON NULL,
                       wojewodztwo TEXT REFERENCES wojewodztwa,
                       PRIMARY KEY (wojewodztwo, powiat)
               )''')

def dbmake(dbname, plikzdanymi):
    with sqlite3.connect(dbname) as db:
        dbinit(db)
        dbfill(db, io.open(plikzdanymi, encoding='utf-8').readlines())

def write_q(dbname, pyt):
    select = {
        'q1': '''SELECT wojewodztwo, sum(populacja) as poptot FROM powiaty
                 GROUP BY wojewodztwo ORDER BY poptot DESC
              ''',
        'q2': '''SELECT wojewodztwo, powiat, populacja FROM powiaty,
                 (SELECT wojewodztwo as maxwoj, MAX(populacja) AS maxpop
                  FROM powiaty GROUP BY wojewodztwo)
                 WHERE populacja = maxpop AND wojewodztwo = maxwoj
                 ORDER BY wojewodztwo
              ''',
        'q2_nat':
              '''SELECT * FROM powiaty NATURAL JOIN
                 (SELECT wojewodztwo, MAX(populacja) AS populacja FROM powiaty
                  GROUP BY wojewodztwo)
                 ORDER BY wojewodztwo''',
        'q3_lista':
              '''SELECT wojewodztwo, powiat, populacja, avgpop FROM powiaty,
                 (SELECT AVG(populacja) as avgpop FROM powiaty)
                 WHERE populacja > avgpop
                 ORDER BY wojewodztwo, populacja DESC
              ''',
        'q3': '''SELECT count(*) FROM powiaty,
                 (SELECT AVG(populacja) as avgpop FROM powiaty)
                 WHERE populacja > avgpop
              ''',
        }

    with sqlite3.connect(dbname) as db:
        for line in db.execute(select[pyt]):
            print(*line, sep='\t')

if __name__ == '__main__':
    if sys.argv[1] == 'create':
        dbmake(DBNAME, 'pl_lud_2010_00_03-2.csv')
    else:
        write_q(DBNAME, sys.argv[1])
