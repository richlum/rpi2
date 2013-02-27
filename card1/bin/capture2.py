#!/usr/bin/python
import observ2
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
        #outstr = "%s, sig = %4d  var = %2d" %( x[0]  , x[1].rolling_avg() ,x[1].rolling_var()  )
        outstr = "%s sig = %4d  var = %5.1f %s %4d %s" %( x[0]  , x[1].rolling_avg() ,x[1].rolling_var(), x[1].subtype , x[1].getlocalcount(),  x[1].ssid)
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
    

    except KeyboardInterrupt:
        break

    if not line:
       continue
    

#    print >> sys.stderr, "*" + str(fields)

