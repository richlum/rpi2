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
    while (self.active):
      dataset = self.aggr.get_sig_summary()
      for i,mac in enumerate(dataset):
	print str(i) +  str (dataset[mac].get_signals() )
      time.sleep(1)
      
      


    
