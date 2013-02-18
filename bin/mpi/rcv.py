#!/usr/bin/python


from mpi4py import MPI

com=MPI.COMM_WORLD

rank=com.Get_Rank()
size=com.GetSize()


data= {"a": 1, "b":2}

: 
