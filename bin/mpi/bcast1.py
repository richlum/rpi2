#!/usr/bin/python

import mpi4py as mpi
from mpi4py import MPI
import time


def snd():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    buffer={} 
    data = {'a': 7, 'b': 3.14, 'rank': rank}
   #comm.isend(data, dest=0, tag=11)
    if rank == 0:
        time.sleep(1)
        for i in range(0,10):
            print "broadcasting from rank %d" % rank
            comm.bcast(data, root=0)
            time.sleep(5)
    else:
        print "rank =%d irecving" % rank
        while True:
            print "%d getting broadcast" % rank
            buffer=comm.bcast(buffer)
            if buffer:
                print "r=%d: %s" % (rank, str(buffer))
            else:
                print "no data"

snd()
