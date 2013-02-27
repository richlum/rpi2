#!/usr/bin/python
import observ
import sys
import curses
import os
import operator

#myscr=curses.initscr()
#myscr.border(0)
#yx=myscr.getmaxyx()
#rows=yx[0]
#cols=yx[1]
#myscr.addstr(str(rows) + "," + str(cols))
#myscr.refresh()



def display_update(mac_signal):
    print "updating"
    sorted_signals=sorted(mac_signal.iteritems(),key=operator.itemgetter(1))
    for x in sorted_signals:
        print "%s, sig = %4d  var = %2d" %( x[0]  , x[1].rolling_avg() ,x[1].rolling_var()  )



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
        if(count>1000):
            count=0
            display_update(mac_sample)
    

    except KeyboardInterrupt:
        break

    if not line:
       continue
    

#    print >> sys.stderr, "*" + str(fields)

