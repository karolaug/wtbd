
import re
import io
import sqlite3
import sys

dbname = 'baza.db'
filename = 'available'
re_package = re.compile(r'^Package: (.*)$')
re_version = re.compile(r'^Version: (.*)$')
re_section = re.compile(r'^Section: (.*)$')
re_priority = re.compile(r'^Priority: (.*)$')
re_size = re.compile(r'^Installed-Size: (.*)$')


def dbinit(db):
    db.execute('drop table if exists PACKAGES;')
    db.execute('create table PACKAGES (Package text primary key, Version text, Section text, Priority text, Installed_Size integer);')


def dataret(lines):
    data = []
    num = -1
    for line in lines:
        q = re_package.match(line)
        if q:
            num += 1
            data.append([])
            data[num].append(q.group(1))
            continue
        q = re_priority.match(line)
        if q:
            data[num].append(q.group(1))
            continue
        q = re_section.match(line)
        if q:
            data[num].append(q.group(1))
            continue
        q = re_size.match(line)
        if q:
            data[num].append(q.group(1))
            continue
        q = re_version.match(line)
        if q:
            data[num].append(q.group(1))
            continue
    return data

def dbfill(db, lines):
    data = dataret(lines)
    for i in data:
        db.execute('''insert into Packages(Package, Priority, Section, Installed_Size, Version)  values (?,?,?,?,?);''',i)



def z1(filename):
    data = dataret(io.open(filename, encoding='utf-8').readlines())
    print 'Ilosc Packages: ', len(data)
    razem = 0
    for i in data:
        razem += int(i[3])
    print 'Installed_size: ', razem





def z2(dbname, filename):
    with sqlite3.connect(dbname) as db:
        dbinit(db)
        dbfill(db, io.open(filename, encoding='utf-8').readlines())

    


def z3(dbname, filename):
    z2(dbname, filename)
    with sqlite3.connect(dbname) as db:
        
        q1 = 'Select Count(Package) from Packages;'
        q2 = 'select count(*) from (Select Section from Packages group by Section);'
        q3 = 'Select Count(Package), Section from Packages group by Section;'
        q4 = 'Select Count(Package), Priority from Packages group by Priority;'
        q5 = 'Select Sum(Installed_Size) from Packages;'
        q = [q1, q2, q3, q4, q5]


        for i in q:
            print i
            for j in db.execute(i):
                print j
            

if __name__ == '__main__':
    if sys.argv[1] == 'z1': 
        z1(filename)
    elif sys.argv[1] == 'z1':
        z2(dbname, filename)
    elif sys.argv[1] == 'z3':
        z2(dbname, filename)
        z3(dbname, filename)
