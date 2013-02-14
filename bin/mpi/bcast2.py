#!/usr/bin/python

import mpi4py as mpi
from mpi4py import MPI
import time
import threading
import datetime

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def bcastsnd():
    
    data = {'a': 7, 'b': 3.14, 'rank': rank}
    time.sleep(1)
    for i in range(0,3):
        print "broadcasting from rank %d" % rank
        comm.bcast(data, root=0)
        time.sleep(5)

def bcastrcv():    
    buffer={} 
    print "%d getting broadcast" % rank
    while True:
        buffer=comm.bcast(buffer)
        if buffer:
            print "r=%d: %s" % (rank, str(buffer))
#        else:
#           print "no data"

class SndThread(threading.Thread):
    def run(self):
        now = datetime.datetime.now()
        print "%s snd thread starting %s" % (self.getName(),now)
        data = {'a': 7, 'b': 3.14, 'rank': rank}
        bcastsnd()        
        
class RcvThread(threading.Thread):
    def run(self):
        now = datetime.datetime.now()
        print "%s rcvr thread starting %s" % (self.getName(), now)
        bcastrcv()

########### main

snd_thread=SndThread()
rcv_thread=RcvThread()

snd_thread.start()
rcv_thread.start()


snd_thread.join()
