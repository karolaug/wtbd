#! /usr/bin/python2.7
import os

def tobits(n):
    s = []
    while n > 0:
        r = n%2
        n = n/2
        s.append('%i' % r)
    s.reverse()
    return ''.join(s)

def frombits(bits):
    res = 0
    for c in bits:
        if c not in '01':
            raise ValueError('not bits!')
        res *= 2
        res += int(c)
    return res


def wc(n):
    file = open(n).read()
    lines  = file.count('\n')
    words = len(file.split())
    size = len(file)
    return lines, words, size, n

def wc1(n):
    try:
        f = open(n)
    except TypeError:
        f = plik
    l, w, c = 0, 0, 0
    for line in f:
        l += 1
        w += len(line.split())
        c += len(line)
    return l, w, c


'''
    if __name__ == '__main__':
        #from sys import argv, stdin
        args = argv[1:]
        if args:
            reslines = list(wc(plik) + (plik,) for plik in args)
        else:
            reslines = [wc(stdin) + ('*',)]
        if len(reslines) > 1:
            reslines.append(tuple(sum(t) for t in zip(*reslines)[:3]) + ('RAZEM',))
        reslines = list(tuple(str(x) for x in line) for line in reslines)
        maxl = tuple(max(len(s) for s in col) + 1 for col in zip(*reslines))
        fmt = '%%%ds%%%ds%%%ds %%s' % maxl[:3]
        for line in reslines:
            print fmt % line
'''
