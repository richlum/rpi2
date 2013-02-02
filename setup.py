#!/usr/bin/python
import re
import subprocess

cmd1='airmon-ng'
arg1='check'
arg2='wlan0'
instr = subprocess.check_output([cmd1,arg1,arg2])
print output

#fn='prepmon_input.txt'
#f=open(fn,'r')
#instr = f.read()

print instr

m=re.findall("\n(\d{4})\s+(\w+)",instr)
args=['kill']
for  process in m:
    if "wpa_supplicant" != process[1]:
        args.append(process[0])

for a in args:
    print a



