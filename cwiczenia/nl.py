from sys import stdout, stderr, argv, stdin

args = argv[1:]

if args:
    for i in args:
        f = open(i)
        z = 1
        print "***PLIK: ", i, " ***"
        for k in f:    
            stdout.write(str(z)+str(": ")+str(k))
            z += 1
else:
    k = 1
    for i in stdin:
        stdout.write(str(k)+": "+str(i))
        k += 1

