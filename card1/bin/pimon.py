#!/usr/bin/python
#####################################
# richardlum13@gmail.com
# 20130202
# 
# setup and execute airmon commands to start wireshark


import re
import subprocess

def setup():
  cmd1='airmon-ng'
  arg1='check'
  arg2='wlan0'
  instr = subprocess.check_output([cmd1,arg1,arg2])
  print instr
  
  # get all the pids that might interfere with airmon
  m=re.findall("\n(\d{4})\s+(\w+)",instr)
  args=['kill']
  for  process in m:
      if "wpa_supplicant" != process[1]:
          # do not kill wpa process - cuts of internet access
          args.append(process[0])
  
  for a in args:
      print a
  
  #kill the processes
  rc = subprocess.call(args)
  print "kill rc = " + str(rc)
  
  if rc == 0 :
      arg1='start'
      arg2='wlan0'
      instr = subprocess.check_output([cmd1,arg1,arg2])
      print instr    
      # get the interface that has been activated
      m=re.search(r"monitor mode enabled on\s(\w+)\)",instr)
      interface=m.group(1)
      print interface
      return interface

define startTshark(interface):      
      cmd=[]
      cmd.append('tshark')
      cmd.append('-i')
      cmd.append(interface)
      rc = subprocess.call(cmd)
      print "tshark rc = " + str(rc)   

def shutdownmon(interface):
    cmd=[]
    cmd.append('airmon-ng')
    cmd.append('stop')
    cmd.append(interface)
    rc = subprocess.call(cmd)
    print "shutdown rc=" + str(rc)

#  sudo tshark -i mon0 -T fields -F (wlan.ta) -e radiotap.dbm_antsignal -e wlan.ta -e wlan_mgt
