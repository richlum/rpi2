#!/usr/bin/python
import threading
import time

class Locator(threading.Thread):
  def __init__(self,aggregator):
    super(Locator,self).__init__()
    self.aggr = aggregator
    self.active=True

  def off(self):
    self.active=False
    
  def run(self):
    counter=0
    while (self.active):
      dataset = self.aggr.get_sig_summary()
      for i,mac in enumerate(dataset):
	print str(i)+ " "  +   mac  + str (dataset[mac].get_signals()) +  \
	  str(dataset[mac].get_xy())
      counter+=1
      print "counter = %d" % counter
      time.sleep(1)
      
      
      
      
      #use aggr.get_sig_summary to get a SigSummary Object.(called dataset here)
      #see file distrubute.py SigSummary class1
      #dataset.set_xy(xval,yval)
      #dataset.get_var(self):
      #dataset.get_signals(self):
      #dataset.get_xy():
   

    
