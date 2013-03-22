#!/usr/bin/python
#####################################
# richardlum13@gmail.com
# 20130217
# 
# receive dictionary of Observations {mac:Observation}
# stores dictionaries (min 3) in Aggregate object
# Aggregate provides collation of 3 observations by mac into a SigSummary object
# create a dictionary of SigSummary objects keyed by mac {mac:SigSummary} as input
# into mpi for dietribution.

# mixture of methods and two classes here centered on saving and sharing signal info

from mpi4py import MPI
import threading
import thread
import util 
from datetime import datetime
import itertools


DICT_DIST = 10
POSITION_DIST = 20
PIMAC_DIST = 30
AP_DIST = 40
CMD_STOP = 50
CMD_START = 60
CMD_CLEARSTALE = 70
CALC_DIST = 80

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
    util.dbg(10)
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
    self.count=0

  
  def update(self, sig0, sig1, sig2, var0, var1, var2):
    self.sig0=sig0
    self.sig1=sig1
    self.sig2=sig2
    self.var0=var0
    self.var1=var1
    self.var2=var2
    self.count+=1
  
  def setcount(self,count):
    self.count=count 

  def getcount(self):
    return self.count


  def set_xy(self,xval,yval):
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
      util.dbg(self.rank)
      observations = self.receive_mac_obs()
      #print "recv loop:" + str(observations)
      
  def __init__(self, comm, rank, size):
    """
    save mpi parameters so that Aggregate and provide send/recv services
    """
    super(Aggregegate,self).__init__()
    self.comm=comm
    self.rank=rank
    self.size=size
    self.Lock_obs = thread.allocate_lock()
    self.Lock_sigsum =  thread.allocate_lock()
    self.active=True
    self.observationlists={}
    self.sigsum={}
    
    print "initialized"
    
  def send_location_summary_helper(self, dest_rank, sig_sum, tag_type):
    if dest_rank<0  or dest_rank> self.size :
        print "############# dest rank = %d" % dest_rank
        return
    if sig_sum:
        dbgmsg = "%d:%d send loc summary: %s" % (self.rank, dest_rank, str(sig_sum))
        util.dbg(self.rank, dbgmsg)
        try:
            self.comm.send(sig_sum, dest=dest_rank, tag=POSITION_DIST)
        except RuntimeError as r:
            print "runtime error" + r.args
        except TypeError as t:
            print "typeerror" + t.args
        except IOError as i:
            print "ioerror" + i.args
        except Exception as e:
            print "exception" + e.args
            

        util.dbg(self.rank, dbgmsg)
    else:
        print "###################sig_sum=NULL, nothing sent"
 
  def shutdown(self):
    util.dbg(self.rank)
    self.active=False
    
  def distrib(self, mac_observations):
    commsize = self.comm.Get_size()
    util.dbg(self.rank)
    for ranks in range(commsize):
      if ranks != self.rank:
        self.Lock_obs.acquire()
        util.dbg(self.rank,"locked Lock_obs")
        #print "%d: mac_obs going into send %d" % (ranks, len(mac_observations))
        copy_mac_obs=mac_observations.copy()
        self.Lock_obs.release()
        util.dbg(self.rank,"unlocked Lock_obs")
        
        maxsendqty=20
        qty=len(copy_mac_obs)
        print "%d:%d total size to send %d " % (self.rank, ranks, qty)
        # slice up dictionaries into chunks of 10 or less for sending
        while qty>0:
            if qty>=maxsendqty:
                tosend=dict(itertools.islice(copy_mac_obs.iteritems(),0,maxsendqty))
                copy_mac_obs=dict(itertools.islice(copy_mac_obs.iteritems(),maxsendqty,qty))
            else:
                tosend=copy_mac_obs
                copy_mac_obs={}
            qty=len(copy_mac_obs)
            print "%d: %d sending size %d" % (self.rank, ranks, len(tosend))    
            try:
                self.comm.send(tosend, dest=ranks, tag=DICT_DIST)
            except RuntimeError as r:
                print "RUNTIME error"+r.args
            except TypeError as t:
                print "TYPERROR"+t.args
            except IOError as i:
                print "IOERROR"+i.args
            except Exception as e:
                print "EXCEPTION"+e.args
             
#        self.comm.send(copy_mac_obs, dest=ranks, tag=DICT_DIST)
        dbgmsg = str(len(copy_mac_obs)) + " macs sent"
        util.dbg(self.rank,dbgmsg)
   
  def timestamp(self,mac_obs):
    currtime=datetime.now()
    for mac in mac_obs:
      mac_obs[mac].settimestamp(currtime)

  def removeold(self,mac_obs,newlist):
    maxdelta = 30
    oldsize= len(mac_obs)
    currenttime=datetime.now()
    
    #newlist={}
    for mac in mac_obs:
      delta = mac_obs[mac].gettimestamp() - currenttime
      if delta.seconds < maxdelta :
        newlist[mac]=mac_obs[mac]
    mac_obs=newlist
    newsize = len(mac_obs)
    #if newsize != oldsize :
    #  print "changed obs size from " + str(oldsize) + " to " + str(newsize)
    return newlist
  
  def push_obs(self,mac_observations, src_rank):
    """
    collect dictionaries of Observation objects keyed by the rank of the observing pi
    that generated the data
    """
    #todo implement locks around the observationlists
    if len(mac_observations) <= 0:
        print "Empty observation"
        return
    obslist={}
    util.dbg(self.rank)
    self.Lock_obs.acquire()
    #print str(self.rank) + ":length of observ list = " + str(len(self.observationlists[src_rank]))
    self.timestamp(mac_observations)
    util.dbg(self.rank,"locked Lock_obs")
    if src_rank not in self.observationlists :
     self.observationlists[src_rank]=mac_observations.copy()
    else: 
     obslist=self.observationlists[src_rank]
     obslist = self.removeold(mac_observations,obslist)
     obslist.update(mac_observations)
     #self.observationlists[src_rank]=obslist.copy()
     self.observationlists[src_rank]=mac_observations.copy()
#todo: something is wrong with observation list, it grows unbounded 
# and does not match macobs size    
    print "observationlist len = %d" % len(self.observationlists[src_rank])
    self.Lock_obs.release()
    print str(self.rank) + ":length of observ list = " + str(len(self.observationlists[src_rank]))
#    print str(self.rank) + ":length of macobs list = " + str(len(mac_observations))
    util.dbg(self.rank,"unlocked Lock_obs")
    ## if you want to verify updates being entered uncomnent the following
#    for mac in mac_observations:
#      if (mac_observations[mac].count>2):
#        print str(self.rank) + ": " + mac + " " + str(mac_observations[mac].rolling_avg())  +" activity=" + str(mac_observations[mac].count)
   
 
  def get_sig_summary(self):
    """
    create a SigSummary object that provides current view of all clients collated
    signal information from 3 pi observers
    
    """
    #self.sigsum={}
    
    self.Lock_obs.acquire()
    print str(self.rank) + ": len obs list = " +  str(len(self.observationlists) ) 
    if len(self.observationlists) != 3:
      # data not present yet
      self.Lock_obs.release()
      util.dbg(self.rank)
      return self.sigsum.copy()
    size0 = str(len(self.observationlists[0]))
    size1 = str(len(self.observationlists[1]))
    size2 = str(len(self.observationlists[2]))
    dbgmsg  = "size of list (0,1,2) = " + size0 + ", " + size1 + ", " + size2 
    util.dbg(self.rank,dbgmsg)
    self.Lock_sigsum.acquire()
    if len(self.sigsum)>100:
      self.sigsum={}
    for macaddr in self.observationlists[0]:
      if (macaddr in self.observationlists[0] and \
        macaddr in self.observationlists[1] and \
        macaddr in self.observationlists[2]):
      
        obs0 = self.observationlists[0][macaddr]
        obs1 = self.observationlists[1][macaddr]
        obs2 = self.observationlists[2][macaddr]
    #    self.Lock_sigsum.acquire()
        #if macaddr not in self.sigsum:
        self.sigsum[macaddr]=SigSummary( \
            obs0.rolling_avg(), \
            obs1.rolling_avg(), \
            obs2.rolling_avg(), \
            obs0.rolling_var(), \
            obs1.rolling_var(), \
            obs2.rolling_var() )
        #else:
         # ss=self.sigsum[macaddr]
          #ss.update( \
          #  obs0.rolling_avg(), \
          #  obs1.rolling_avg(), \
          #  obs2.rolling_avg(), \
          #  obs0.rolling_var(), \
          #  obs1.rolling_var(), \
          #  obs2.rolling_var() )
        #self.Lock_sigsum.release()
      else: #mac not in all three observation lists
        #dont bother processing unless we have all 3 observation
        continue
    self.Lock_sigsum.release()
    self.Lock_obs.release()
    pass
    self.Lock_sigsum.acquire()
    #copy results and send to requestor. needs to be a copy to
    #prevent simultaneus read/write to same dictionary
    sigsum_copy=self.sigsum.copy()
    self.Lock_sigsum.release()
    dbgmsg= str(len(sigsum_copy)) + "sigsumm items"
    util.dbg(self.rank, dbgmsg)
    return sigsum_copy
  
 
  def append_sigsummary(self,calcresults):
    """
    with another pi calculates position, use this method to add
    calculated results into local list of position results
    note this will also overwrite reported signals s1 s2 s3
    """
    self.Lock_sigsum.acquire()
    self.sigsum.update(calcresults) # Update sig summary dict
    self.Lock_sigsum.release()
 
  def receive_mac_obs(self):
      """
      receive side of mpi_recv to receive {mac:Observation} from other Observers
      """
      
      util.dbg(self.rank,"recv mac obs")
      #if (self.rank == 0):
        #print "!!!!!!!!!!!!!!!!!!!!!!!"
        #print len(self.sigsum)
        #print "!!!!!!!!!!!!!!!!!!!!!!!"

      stat = MPI.Status()
      data = self.comm.recv( source=MPI.ANY_SOURCE , tag=MPI.ANY_TAG, status=stat )
      #print "received obs from %d\n" % stat.Get_source()
      data_tag = stat.Get_tag()
      if data_tag == DICT_DIST:
        self.push_obs(data, stat.Get_source() )
      elif data_tag == CALC_DIST:
        #we are getting distributed calculation results. collate them
        # the send side should be sending us a dictionary of SigSummary
        # Objects with the x y co-ordinates populated.
        #TODO: needs testing
        self.append_sigsummary()
        pass
      elif data_tag == POSITION_DIST:
    # Only RANK 0 will recv this tag; update sig_summary sent from other
        self.append_sigsummary(data)
        pass
      elif data_tag == PIMAC_DIST:
        #TODO: build datastructure to hold the mac of the pi and rank
        # build to estefan requirements
        pass
      elif data_tag == AP_DIST:
        #TODO: build datastructure to hold all AP mac and ssid (if avail)
        # build to estefan requirements
        pass
      elif data_tag == CMD_STOP:
        #TODO: set active off for all mac
        #at this point, design may not keep recvg messages for start
        #review code to implement
        pass
      elif data_tag == CMD_START:
        #TODO:
        pass
      elif data_tag == CMD_CLEARSTALE:
        #TODO: initiate wipe of mac addresses that havent been updated in a while
        pass
      
      util.dbg(self.rank)
      return data
      
