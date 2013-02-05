#!/usr/bin/python
import sys

count=0
while 1:
    try:
        line = sys.stdin.readline()
	fields = line.split('\t')
	if (len(fields[4])>0):
		sourcemac=fields[4]
	else if (len(fields[2])>0):
		sourcemac=fields[2]
	else
		continue;
		#no sa or ta
	

	count+=1
	if(count>1000):
		count=0
		display_update()
	

    except KeyboardInterrupt:
        break

    if not line:
        break

    print >> sys.stderr, fields


def display_update():


