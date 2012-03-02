import sqlite3
import io

dbname = 'PT.db'
filename = 'PanTadeusz1.txt'
def zadanie3(dbname):
    with sqlite3.connect(dbname) as db:
        db.execute('drop table if exists slowa')
        s = 'create table slowa (slowo, line int, col int);'
        db.execute(s)
        
        plik = io.open(filename, encoding='utf-8').readlines()
        #print plik
        a = []
	for i in plik:
	    a.append(i.split())
	for i in range(len(a)):
	    for j in range(len(a[i])):
		#print i, j, a[i][j]
		data = [a[i][j], i, j]
    		db.execute('insert into slowa values (?,?,?);',data)


zadanie3(dbname)
