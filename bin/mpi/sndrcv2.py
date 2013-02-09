#!/usr/bin/python

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

class square:
    def __init__(self, data, lastmsg=True):
        self.data=data
        self.lastmsg=lastmsg
    def getdata(self):
        return self.data
    def callme(self):
        print "rank %d has been called" % rank
    def setlastmsg(self,lastmsg=False):
        self.lastmsg=lastmsg



data = {'a': 7, 'b': 3.14, 'rank': rank}
sq=square(data)
comm.send(sq, dest=(rank+1)%5, tag=11)
newsq = comm.recv(source=(rank-1)%5, tag=11)
print newsq.data
newsq.callme()
