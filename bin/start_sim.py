#!/usr/bin/python
import subprocess
import re
import sys

def get_mac():
  cmdstr = 'ifconfig wlan0'
  cmd = cmdstr.split()
  res = subprocess.check_output(cmd)
  m=re.search(r"HWaddr\s+([0-9a-fA-F:]+)",res)
  if m:
    mac=m.group(1)
  else:
    mac='unknown'
  return mac
  
def stream_pcap(fn):
  cmdstr="tshark -r %s -T fields \
    -E separator=; \
    -e radiotap.dbm_antsignal \
    -e frame.len \
    -e wlan.ta \
    -e wlan.ra \
    -e wlan.sa \
    -e wlan.da \
    -e wlan.fc.type_subtype \
    -e frame.time_epoch \
    -e radiotap.channel.freq \
    -e wlan_mgt.ssid \
    -e radiotap.channel.type"  % (fn)
  cmd=cmdstr.split()
  print >>sys.stderr, "executing cmd\n" + str(cmd)
  rc=subprocess.call(cmd)
  print >>sys.stderr, "tshark rc = " + str(rc)
  
filename="sample.pcap"
if (len(sys.argv) >1):
    filename=sys.argv[1]
print "file = %s " % filename
stream_pcap(filename)