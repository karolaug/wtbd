# -*- coding:utf-8 -*-
"""
  +------+	  +------+
  |Stacja|\       |Pociąg|
  +------+ \	  +---/--+
       	    \	     /
       	   +-\------/-----+
	   |Postój     	  |
	   |początek hh:mm|
           |koniec   hh:mm|
	   +--------------+
"""

def dbinit(db):
    pass

def dbfill(db, schedule):
    pass

def write_q(db, question):
    pass

def main(dbname, command, *args):
    if command == 'create':
        dbinit(db)
    elif command == 'register':
        for schedule in args:
            dbfill(db, schedule)
    else:
        write_q(db, command)
    return 0

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
