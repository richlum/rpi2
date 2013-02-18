#!/usr/bin/python

import mpi4py as mpi
from mpi4py import MPI
import time
import threading
import datetime



class SndThread(threading.Thread):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    def run(self):
        now = datetime.datetime.now()
        print "%d:%s snd thread starting %s" % (self.rank,self.getName(),now)
        data = {'a': 7, 'b': 3.14, 'rank': self.rank}
        self.bcastsnd()        
    
    def bcastsnd(self):
        data = {'a': 7, 'b': 3.14, 'rank': self.rank}
        time.sleep(1)
        for i in range(0,3):
            print "broadcasting from rank %d" % self.rank
            self.comm.bcast(data, root=self.rank)
            time.sleep(5)

class RcvThread(threading.Thread):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    def run(self):
        now = datetime.datetime.now()
        print "%s rcvr thread starting %s" % (self.getName(), now)
        self.bcastrcv()

    def bcastrcv(self):    
        buffer={} 
        print "%d getting broadcast" % self.rank
        while True:
            buffer=self.comm.bcast(buffer)
            if buffer:
                print "r=%d: %s" % (self.rank, str(buffer))


########### main

snd_thread=SndThread()
rcv_thread=RcvThread()

snd_thread.start()
rcv_thread.start()


snd_thread.join()
