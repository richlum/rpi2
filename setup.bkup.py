#!/usr/bin/python
import re


fn='prepmon_input.txt'
f=open(fn,'r')
instr = f.read()

print instr

#m=re.search("\n(\d{4})\s+(\w+)",instr)
#print m.group(1)
#print m.group(2)

m=re.findall("\n(\d{4})\s+(\w+)",instr)
args=['kill']
for  process in m:
#    print process[0]
#    print process[1]
#    if "wpa_supplicant" == process[1] :
#        print "MATCH"
#    else:
    if "wpa_supplicant" != process[1]:
#        print "NOMATCH"
        args.append(process[0])

for a in args:
    print a






