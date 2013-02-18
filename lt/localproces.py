#!/usr/bin/python
import sys
import os
import subprocess

filename=sys.argv[1]

print sys.argv[1]
cmdstr="tshark -r %s -T fields \
    -e radiotap.dbm_antsignal \
    -e frame.len \
    -e wlan.ta \
    -e wlan.ra \
    -e wlan.sa \
    -e wlan.da \
    -e wlan.fc.type_subtype \
    -e frame.time_epoch \
    -e radiotap.chanel.freq \
    -e wlan_mgt.ssid \
    -e radiotap.channel.type"  % (filename)

cmd=cmdstr.split()
rc=subprocess.call(cmd)


