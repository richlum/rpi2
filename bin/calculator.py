#!/usr/bin/python
import threading
import time
import dbufwindow

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
      if (self.aggr.rank == 0):
        for i,mac in enumerate(dataset):
          print str(self.aggr.rank) +":"+ str(i)+ " "  +   mac  + str (dataset[mac].get_signals()) +  \
            str(dataset[mac].get_xy())
        counter+=1
        print "counter = %d" % counter
      else:
        #TODO:  TONY  this is where your logic for distributed calculations should be integrated to
        # send data if not rank 0.   Matching recv logic in distribute.py recv thread 
        # we need an mpisend here using tag  POSITION_DIST    (which needs to be put into a common file
        # accessible from both distribute.py and calculator.py
        #send calculated data back to rank 0
        pass
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
   

    
