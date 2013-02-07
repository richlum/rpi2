#!/usr/bin/python
import observ
import sys
import curses
import os
import operator

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
    global screen
    global updatecount
    screen=initscreen()
    #print "updating"
    sorted_signals=sorted(mac_signal.iteritems(),key=operator.itemgetter(1))
    count=2
    for x in sorted_signals:
        outstr = "%s, sig = %4d  var = %4.1f   %4d" %( x[0]  , x[1].rolling_avg() ,x[1].rolling_var() , x[1].getlocalcount() )
        screen.addstr(count,2, outstr  )
        count+=1
        if count>=(screen.getmaxyx()[0]-1):
            break;
    screen.addstr(screen.getmaxyx()[0]-1,2,str(updatecount))
    updatecount+=1
    screen.refresh()

inited=False
mac_sample={}  # hash of observations
count=0
while 1:
    try:
        line = sys.stdin.readline()
        fields = line.split('\t')
        if (len(fields[4])>0):
            mac=fields[4]
        elif (len(fields[2])>0):
            mac=fields[2]
        else:
            continue
        #no sa or ta
        if (mac not in mac_sample):
            o=observ.Observation(fields[0]);
            mac_sample[mac]=o
        else:
            mac_sample[mac].add(fields[0])

        count+=1
        if(count>200):
            count=0
            display_update(mac_sample)
    

    except KeyboardInterrupt:
        break

    if not line:
       continue
    

#    print >> sys.stderr, "*" + str(fields)

