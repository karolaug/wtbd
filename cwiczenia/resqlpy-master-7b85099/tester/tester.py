# -*- coding:utf-8 -*-
"""\
Pozwala na sprawdzenie wyrażenia regularnego względem zestawu
przykładów.

Użycie:
  ./tester.py <wyrażenie> <przykłady-dobre-plik> <przykłady-złe-plik>
"""

from __future__ import print_function
import sys
import re

def testone(wzorzec, napis, isgood):
    m = wzorzec.match(napis)
    failed = bool(m) != bool(isgood)
    return (failed,
            'GOOD' if isgood else 'BAD',
            napis,
            'failed' if failed else 'OK')

def testmany(wzorzec, dobre, zle):
    failed = 0
    total = 0
    for file,expected in ((dobre, True), (zle, False)):
        for napis in file:
            fail, a1, a2, a3 = testone(wzorzec, napis.rstrip('\n'), expected)
            failed += fail
            total += 1
            print(a1, a2, a3)
    if failed:
        print('failed {} / {}'.format(failed, total))
    else:
        print('all {} OK'.format(total))
    return bool(failed)

if __name__ == '__main__':
    ret = testmany(re.compile(sys.argv[1], re.X),
                   open(sys.argv[2]).readlines(),
                   open(sys.argv[3]).readlines())
    sys.exit(ret)
