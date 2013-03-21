#!/usr/bin/python
#####################################
# richardlum13@gmail.com
# 20130217
# 
# specific tshark input expected on stdin (see start_sym.py)
# 
# if this has command line arg 'prox' will display proximity signal screen
# 
# also builds distribute objects in prep for mpi distribution.

import observ3
import sys
import curses
import os
import operator
import time
import distribute
from distribute import Aggregegate
from distribute import SigSummary
import util
from mpi4py import MPI
from calculator import Locator


options=[]
if (len(sys.argv) > 1):
    options = sys.argv[1:]

proxdisplay=False
if "prox" in options:
  proxdisplay=True
  
inited=False

def initscreen():
    global inited
    global myscr
    if not inited:
        inited=True
        myscr=curses.initscr()
        myscr.border(0)
        yx=myscr.getmaxyx()
        rows=yx[0]
        cols=yx[1]
        myscr.addstr(str(rows) + "," + str(cols))
        myscr.refresh()
    return myscr

updatecount=0
def display_update(mac_signal):
    "input: dict of mac to observation data "
    global screen
    global updatecount
    screen=initscreen()

    samples=[]
    sorted_signals=[]
    ssignals=[]
    for entry in mac_signal:
        samples=[]
        samples.append(entry)
        samples.append(mac_signal[entry])
        samples.append(mac_signal[entry].rolling_avg())
        ssignals.append(samples)  
    
    #sorted_signals.sort(key = lambda row: row[2])
    sorted_signals=sorted(ssignals,key=(operator.itemgetter(2)), reverse=True )
    count=2
    for x in sorted_signals:
        ssid=x[1].ssid + (8-len(x[1].ssid))*' '
        outstr = "%s sig = %4d  var = %5.1f %s %2d %4.4s %4d %s" %( x[0]  , x[1].rolling_avg() ,x[1].rolling_var(), x[1].subtype, x[1].isAP%100 ,x[1].freq , x[1].getlocalcount(),  ssid)
        screen.addstr(count,2, outstr  )
        #curses leaves rest of line untouched if new line is shorter than old line
        rest = screen.getmaxyx()[0]-1 - len(outstr)
        if rest>0:
            for x in rest:
                mvaddch(count,len(outstr)+x,' ')
        count+=1
        if count>=(screen.getmaxyx()[0]-1):
            break;
    screen.addstr(screen.getmaxyx()[0]-1,2,str(updatecount)+"rows="+str(count))
    updatecount+=1
    screen.refresh()

def initialize_mpi():
  """
  keep comm and rank here at top level incase we need to invoke other mpi communication
  """
  comm=MPI.COMM_WORLD
  rank=comm.Get_rank()
  size=comm.Get_size()
  return (comm,rank,size)
  
    
    
#my_mac_addr = util.get_mac() 
my_mac_addr = 'blank' 
inited=False
mac_sample={}  # hash of observations
count=0

(comm, rank,size) = initialize_mpi()

## TONY HARDCODED
## TODO : Dynamically determine max # of RPI
MAX_NUM_PI = 3

signal_aggregator = Aggregegate(comm,rank,size)
#start signal_aggregator mpi recieve thread 
signal_aggregator.start()
position_calculator =  Locator(signal_aggregator, MAX_NUM_PI)
position_calculator.start()

while 1:
    try:
        line = sys.stdin.readline()
        fields = line.split(';')
        if (len(fields[4])>0):
            mac=fields[4]
        elif (len(fields[2])>0):
            mac=fields[2]
        else:
            continue
        #fields are defined in setup.py .  see tshark command setup for list 
        # 0 - signal strength dbm
        # 1 - frame.len bytes
        # 2 - transmit addr
        # 3 - recv addr
        # 4 - sender addr
        # 5 - dest addr
        # 6 - wlan.fc.type_subtype
        # 7 - time_epoch
        # 8 - freq
        # 9 - ssid
        # 10 - channel.type (a/b/g)
        # my_mac_addr is mac address of observing pi (source of dbm readings)
        if (mac not in mac_sample):
        #new mac address needs new observation
            #print "adding " + mac
            o=observ3.Observation(fields[0], \
                fields[1], \
                fields[6], \
                fields[7], \
                fields[8], \
                fields[9], \
                fields[10], \
                my_mac_addr); 
            mac_sample[mac]=o
        else:
            #existing mac address, just update signal
            #print "updating " + mac
            mac_sample[mac].add(fields[0])

        count+=1
        if(count>100):
            count=0
            if proxdisplay:
              display_update(mac_sample)
        #save locally and broadcast out data
#        changed_obs={}
#        for mac in mac_sample:
#          if mac_sample[mac].dirty:
#            changed_obs[mac]=mac_sample[mac]
#            distribute.share(signal_aggregator,changed_obs,rank)
#        for mac in mac_sample:
#          mac_sample[mac].dirty=False
          #this timer is for simulator only, remove on actual rpi implementation
            #print str(rank) + ":distribute qty macs "  + str(len(mac_sample))
            distribute.share(signal_aggregator,mac_sample,rank)
            mac_sample={}
            time.sleep(1)
            
    

    except KeyboardInterrupt:
      signal_aggregator.shutdown()
      comm.Disconnect()
      break

    if not line:
      continue
    
