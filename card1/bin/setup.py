#!/usr/bin/python
#####################################
# richardlum13@gmail.com
# 20130202
# 
# setup and execute airmon commands to start wireshark

import sys
import re
import subprocess



cmd1='airmon-ng'
arg1='check'
arg2='wlan0'
instr = subprocess.check_output([cmd1,arg1,arg2])
print  >> sys.stderr, instr

# get all the pids that might interfere with airmon
m=re.findall("\n(\d{4})\s+(\w+)",instr)
args=['kill']
for  process in m:
    if "wpa_supplicant" != process[1]:
        # do not kill wpa process - cuts of internet access
        args.append(process[0])

for a in args:
    print >> sys.stderr, a
rc=0
#kill the processes
if len(args)>1:
    rc = subprocess.call(args)
    print >>sys.stderr,  "kill rc = " + str(rc)

#is monitor already running
cmd='ifconfig'
res = subprocess.check_output(cmd)
m=re.search(r"\n(mon\d)\s+Link",res)
if m:
	interface=m.group(1)
else:
	interface=None

#only start monitor mode if its not already up
if ((rc == 0) and ((interface)==None)) :
    arg1='start'
    arg2='wlan0'
    instr = subprocess.check_output([cmd1,arg1,arg2])
    print >>sys.stderr, instr    
    # get the interface that has been activated
    m=re.search(r"monitor mode enabled on\s(\w+)\)",instr)
    if (m is None):
      print >> sys.stderr, "Unable to start monitor mode"
    else:
      interface=m.group(1)

print >> sys.stderr, interface
cmdstr="tshark -i %s -T fields -e radiotap.dbm_antsignal -e frame.len -e wlan.ta -e wlan.ra -e wlan.sa -e wlan.da -e wlan.fc.type_subtype" % (interface)
cmd=cmdstr.split()
rc = subprocess.call(cmd)
print  >> sys.stderr, "tshark rc = " + str(rc)  
    
