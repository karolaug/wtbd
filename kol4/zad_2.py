import sys
import sqlite3


q = sys.argv[1]
dbname = 'pl_lud.db'

def zadanie2(dbname):
    with sqlite3.connect(dbname) as db:
        
	if q == 'q1':
             s = 'select wojewodztwa.nazwa, count(*) from wojewodztwa, powiaty where powiaty.w_id = wojewodztwa.id group by wojewodztwa.nazwa;'
        elif q == 'q2':
	     s = 'select powiaty.nazwa, powiaty.ludnosc, wojewodztwa.nazwa from powiaty, wojewodztwa where powiaty.w_id = wojewodztwa.id order by powiaty.ludnosc desc limit 10;'
        elif q == 'q3':
            #s = 'select avg(ludnosc),  from powiaty;'
	    s = 'SELECT ludavg, AVG((ludnosc - ludavg)*(ludnosc - ludavg)) FROM powiaty, (SELECT AVG(ludnosc) AS ludavg FROM powiaty);'
        
        for j in db.execute(s):
            print j


zadanie2(dbname)
