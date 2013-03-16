#!/usr/bin/python
import subprocess
import re
import sys
import inspect
debug=False

def dbg(rank=99,msg=""):
  if debug:
    callerframerecord = inspect.stack()[1]
    frame=callerframerecord[0]
    info=inspect.getframeinfo(frame)
    if len(msg)<=0:
      print str(rank)+":"+info.filename + ":" + info.function +":"+str(info.lineno)
    else:
      print str(rank)+":"+info.filename + ":" + info.function +":"+str(info.lineno) + ": " + msg



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
  
def stream_pcap(fn='sample.pcap'):
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
 

 
