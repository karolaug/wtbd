
import re
import io
import sqlite3
import sys

dbname = 'samorzad_access_log.db'
filename = 'samorzad.access.log'
re_ip = re.compile(r'^([0-9]{1,3}[.]{1}[0-9]{1,3}[.]{1}[0-9]{1,3}[.]{1}[0-9]{1,3}) ')
re_day = re.compile(r'[\-]{1}[ ]{1}[\-]{1}[.]{2}([0-9]{2})')
re_month = re.compile(r'[\[][.]{3}([.]{3})')
re_time = re.compile(r'[\[][.]{7}(.*)]')
re_type = re.compile(r'\] "([.]{3})')
re_url = re.compile(r'".{3} (.*)"')
re_status = re.compile(r'" ([:digit:]{3})')
re_size = re.compile(r'[:digit:]{3} ([:digit:]*)')
re_client = re.compile(r'"-" "(.*)"')

def dbinit(db):
    db.execute('drop table if exists log')
    db.execute('create table log (ip text, day int, month text, time text, type text, url text, status int, size int, client text);')


def dataret(lines):
    data = []
    num = -1
    for line in lines:
        q = re_ip.match(line)
        if q:
            num += 1
            data.append([])
            data[num].append(q.group(1))
            continue
        q = re_day.match(line)
        if q:
            data[num].append(q.group(1))
            continue
        q = re_month.match(line)
        if q:
            data[num].append(q.group(1))
            continue
        q = re_time.match(line)
        if q:
            data[num].append(q.group(1))
            continue
        q = re_type.match(line)
        if q:
            data[num].append(q.group(1))
            continue
        q = re_url.match(line)
        if q:
            data[num].append(q.group(1))
            continue
        q = re_status.match(line)
        if q:
            data[num].append(q.group(1))
            continue
        q = re_size.match(line)
        if q:
            data[num].append(q.group(1))
            continue
        q = re_client.match(line)
        if q:
            data[num].append(q.group(1))
            continue
    print data
    return data

def dbfill(db, lines):
    data = dataret(lines)
    for i in data:
        db.execute('''insert into log(ip, time, type, url, status, size, client)  values (?,?,?,?,?,?,?);''',i)



def zad2(dbname, filename):
    with sqlite3.connect(dbname) as db:
        dbinit(db)
        dbfill(db, io.open(filename, encoding='utf-8').readlines())


def zad3(dbname, filename):
    zad2(dbname, filename)
    with sqlite3.connect(dbname) as db:
        
        q1 = 'select sum(size) from log group by day;'
        q2 = 'select count(*), url from (Select url from log where status=404 group by url);'
        q3 = 'Select ip from log where status=404 group by ip;'
        q = [q1, q2, q3]


        for i in q:
            print i
            for j in db.execute(i):
                print j
            

if __name__ == '__main__':
    if sys.argv[1] == 'zad2':
        zad2(dbname, filename)
    elif sys.argv[1] == 'zad3':
        z3(dbname, filename)
