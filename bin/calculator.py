#!/usr/bin/python
import threading
import time
import dbufwindow
import distribute

#Tony Test
class Locator(threading.Thread):
  def __init__(self,aggregator,MAX_NUM_PI):
    super(Locator,self).__init__()
    self.aggr = aggregator
    self.active=True
    self.MAX_PI_COUNT = MAX_NUM_PI

  def off(self):
    self.active=False
    
  def run(self):
    counter=0
    while (self.active):

      # Shld Contain calc(x,y) obsv from other rank
      dataset = self.aggr.get_sig_summary()
      if (self.aggr.rank == 0):
        for i,mac in enumerate(dataset):

	  # Joey does (x,y) calc on dataset obvs, then resets
	  # Update GUI

          print str(self.aggr.rank) +":"+ str(i)+ " "  +   mac  + str (dataset[mac].get_signals()) +  \
            str(dataset[mac].get_xy())
      else:
	# ADDED BY TONY
	# For non-zero RPI, calculate (x,y) then send result to Rank 0
        for i,mac in enumerate(dataset):
	  mac_hash = int(''.join(mac.split(':')[0:]), 32) % self.MAX_PI_COUNT
	  if (mac_hash != self.aggr.rank):
            continue
	  else:
	    ########## Does does some (x,y)
	    #
	    # 1. Calculation ....   
	    # 2. Save calculated (x,y) back to dataset[mac]
	    #
	    ###########

            ## set coor to (20,20) to test weather send was successful
            dataset[mac].set_xy(20,20)
            sig_sum = {mac : dataset[mac]}
            self.aggr.send_location_summary_helper(0, sig_sum, distribute.POSITION_DIST)
        
      time.sleep(1)
      
  #def run(self):
    #counter=0
    #display=dbufwindow.DemoApp(0)
    #frame=display.getFrame()
    #while (self.active):
      #dataset = self.aggr.get_sig_summary()
      #frame.setData(dataset)
      #frame.NewDrawing()
      #time.sleep(1)
      
      
      #use aggr.get_sig_summary to get a SigSummary Object.(called dataset here)
      #see file distrubute.py SigSummary class1
      #dataset.set_xy(xval,yval)
      #dataset.get_var(self):
      #dataset.get_signals(self):
      #dataset.get_xy():
   

    
