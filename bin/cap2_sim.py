#!/usr/bin/python
import observ2
import sys
import curses
import os
import operator
import time

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
        myscr.addstr(0,20, "RPI2 POXIMITY")
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
    
    sorted_signals=sorted(ssignals,key=(operator.itemgetter(2)), reverse=True )
    count=2
    for x in sorted_signals:
        ssid=x[1].ssid + (8-len(x[1].ssid))*' '
        outstr = "%s sig = %4d  var = %5.1f %s %2d %4.4s %4d %s" %( \
            x[0]  , \
            x[1].rolling_avg() ,\
            x[1].rolling_var(), \
            x[1].subtype, x[1].isAP%100 ,\
            x[1].freq , \
            x[1].getlocalcount(),  \
            ssid)
        screen.addstr(count,2, outstr  )
        rest = screen.getmaxyx()[0]-1 - len(outstr)
        if rest>0:
            for x in rest:
                mvaddch(count,len(outstr)+x,' ')
        count+=1
        if count>=(screen.getmaxyx()[0]-1):
            break;
    screen.addstr(screen.getmaxyx()[0]-1,2,str(updatecount)+" rows="+str(count))
    updatecount+=1
    screen.refresh()
 
inited=False
mac_sample={}  # hash of observations
count=0
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
        #no sa or ta
        if (mac not in mac_sample):
            o=observ2.Observation(fields[0], \
                fields[1], \
                fields[6], \
                fields[7], \
                fields[8], \
                fields[9], \
                fields[10]); 
            mac_sample[mac]=o
        else:
            mac_sample[mac].add(fields[0])

        count+=1
        if(count>100):
            count=0
            display_update(mac_sample)
            time.sleep(1)
    

    except KeyboardInterrupt:
        break

    if not line:
       continue
    

#    print >> sys.stderr, "*" + str(fields)

