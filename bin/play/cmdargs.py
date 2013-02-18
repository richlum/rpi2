#!/usr/bin/python

import sys

options=[]
if (len(sys.argv)>1):
    options=sys.argv[1:]

print options
for i, x in enumerate(options):
    print str(i) + "," +  x 

if "a" in options:
    print "found a"
