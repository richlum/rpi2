#!/usr/bin/python
import sys

while 1:
    try:
        line = sys.stdin.readline()
	fields = line.split()
	

    except KeyboardInterrupt:
        break

    if not line:
        break

    print >> sys.stderr, fields

