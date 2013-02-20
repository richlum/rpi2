#!/usr/bin/python
#####################################
# richardlum13@gmail.com
# 20130217
# 
# receive dictionary of Observations {mac:Observation}
# stores dictionaries (min 3) in Aggregate object
# Aggregate provides collation of 3 observations by mac into a SigSummary object
# create a dictionary of SigSummary objects keyed by mac {mac:SigSummary} as input
# into mpi for distribution.

# mixture of methods and two classes here centered on saving and sharing signal info

from mpi4py import MPI
import threading
import thread



DICT_DIST = 10

def initialize_mpi():
    """
    c requires initialize_mpi, unsure of python equivalent
    """
    pass
  
def share(sig_aggregate, mac_observations, rank):
    """
    invoke mpi_send to send {mac:Observation} dictionaries to other Observers
    """
    #store locally first
    sig_aggregate.push_obs(mac_observations, rank)
    sig_aggregate.distrib(mac_observations)
    pass
  

  
  


class SigSummary:
  """
  collection of signal data for a give mac observed.
  """
  def __init__(self, sig0, sig1, sig2, var0, var1, var2, xpos=0, ypos=0):
    self.sig0=sig0
    self.sig1=sig1
    self.sig2=sig2
    self.var0=var0
    self.var1=var1
    self.var2=var2
    self.x=xpos
    self.y=ypos
  
  def set_xy(xval,yval):
    """
    Utility class for position calculator to deposit results
    """
    self.x=xval
    self.y=yval
  
    
  def get_var(self):
    """
    first cut approx of overall variance for X,Y position 
    """
    return max( self.var0, self.var1, self.var2)
    
  def get_signals(self):
    return (self.sig0,self.sig1,self.sig2)
    
  def get_xy(self):
    return (self.x, self.y)
    
 
    
  
  
class Aggregegate(threading.Thread):
  """
  Object to hold current set of signal observations, Assumed to be 3 dictionaries
  from 3 seperate pi observers 
  """
  def run(self):
    print "aggregator run thread"
    while(self.active):
      observations = self.receive_mac_obs()
      #print "recv loop:" + str(observations)
      
  def __init__(self, comm, rank):
    """
    save mpi parameters so that Aggregate and provide send/recv services
    """
    super(Aggregegate,self).__init__()
    self.comm=comm
    self.rank=rank
    self.Lock_obs = thread.allocate_lock()
    self.active=True
    self.observationlists={}
    print "initialized"
    
    
  def shutdown(self):
    self.active=False
    
  def distrib(self, mac_observations):
    commsize = self.comm.Get_size()
    for ranks in range(commsize):
      if ranks != self.rank:
	 self.Lock_obs.acquire()
	 self.comm.send(mac_observations, dest=ranks, tag=DICT_DIST)
	 #print "sent observations"
	 self.Lock_obs.release()
  
  def push_obs(self,mac_observations, src_rank):
    """
    collect dictionaries of Observation objects keyed by the rank of the observing pi
    that generated the data
    """
    #todo implement locks around the observationlists
    self.Lock_obs.acquire()
    self.observationlists[src_rank]=mac_observations
    self.Lock_obs.release()
    #print "push observationlists"
    #print self.observationlists
    
  def get_sig_summary(self):
    """
    create a SigSummary object that provides current view of all clients collated
    signal information from 3 pi observers
    
    needs to implement locks to prevent multiple threaded read/write collisions
    
    todo: aging out of stale data. Active data automatically is averaged out but
    inactive clients never age out and are currently treated same as current active
    client observations.
    """
    sig_summary={}
    self.Lock_obs.acquire()
    if len(self.observationlists) != 3:
      # data not present yet
      self.Lock_obs.release()
      return sig_summary
    for keys in self.observationlists:
	print keys
	print "----"
    for macaddr in self.observationlists[0]:
      if (macaddr in self.observationlists[0] and \
	  macaddr in self.observationlists[1] and \
	  macaddr in self.observationlists[2]):
	    
	    obs0 = self.observationlists[0][macaddr]
	    obs1 = self.observationlists[1][macaddr]
	    obs2 = self.observationlists[2][macaddr]
	    sig_summary[macaddr]=SigSummary( \
	      obs0.rolling_avg(), \
	      obs1.rolling_avg(), \
	      obs2.rolling_avg(), \
	      obs0.rolling_var(), \
	      obs1.rolling_var(), \
	      obs2.rolling_var() )
      else:
	#dont bother processing unless we have all 3 observations
	continue
    self.Lock_obs.release()
    pass
    return sig_summary
  
  
  def receive_mac_obs(self):
      """
      receive side of mpi_recv to receive {mac:Observation} from other Observers
      """
      #print "recv mac objs"
      stat = MPI.Status()
      data = self.comm.recv( source=MPI.ANY_SOURCE , tag=MPI.ANY_TAG, status=stat )
      #print "received obs from %d\n" % stat.Get_source()
      self.push_obs(data, stat.Get_source() )
      return data
      