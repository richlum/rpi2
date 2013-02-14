#!/usr/bin/python

from mpi4py import MPI

def snd():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    data = {'a': 7, 'b': 3.14, 'rank': rank}
    comm.send(data, dest=0, tag=11)
    Rdata = comm.recv(source=0, tag=11)
    print Rdata


