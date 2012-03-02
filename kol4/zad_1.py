import sqlite3
import numpy as np

dbname = 'T.db'

def mediana(wartosci):
  wartosci = sorted(wartosci)
  if len(wartosci) % 2 == 1:
      return wartosci[(len(wartosci)+1)/2-1]
  else:
    lower = wartosci[len(wartosci)/2-1]
    upper = wartosci[len(wartosci)/2]
    return (float(lower + upper)) / 2  


def zadanie1(dbname):
    with sqlite3.connect(dbname) as db:
        db.execute('drop table if exists T')
        s = 'create table T (X float not null);'
        db.execute(s)
        q = np.random.random(10000)*100
        for i in q:
            db.execute('insert into T (X) values ('+str(i)+');')

        s = '''SELECT AVG(X) FROM
        (SELECT X FROM T
        ORDER BY X
        LIMIT 1 + (SELECT (COUNT(*)+1) % 2 FROM T)
        OFFSET (SELECT COUNT(*) FROM T)/2);'''

        for j in db.execute(s):
            print j
        print mediana(q)

zadanie1(dbname)
