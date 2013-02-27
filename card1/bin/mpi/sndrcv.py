#!/usr/bin/python

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

data = {'a': 7, 'b': 3.14, 'rank': rank}
comm.send(data, dest=(rank+1)%5, tag=11)
data = comm.recv(source=(rank-1)%5, tag=11)
print data


