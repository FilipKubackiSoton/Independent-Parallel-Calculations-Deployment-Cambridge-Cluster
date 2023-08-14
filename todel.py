from mpi4py import MPI
import numpy as np
import os
import itertools
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()

#########################################################################
# HELPER FUNCTION FOR DATA LOADINT INTO THE SYSTEM
# DATA ARRAY MUST BE LOADED AND PARTITIONED BEFORE STARTING CALCULAITONS
# IN PRACTICE IT WILL WORK FOR 'FOR' LOOP WITHOUT INTERNAL CONDITIONS

def readData():
    import pandas as pd
    df = pd.read_csv("HM.csv")
    seqs = df["3AA"].map(lambda x: x.replace("(", "")).map(lambda x: x.replace(")", ""))
    return seqs

def getCombinations(data):
    import itertools
    indexedSeqs = [(i, data[i]) for i in range(len(data))]
    comb = list(itertools.combinations(indexedSeqs, 2))[:10]
    return comb

#########################################################################
if rank == 0:
    
    data = getCombinations(readData()) #list(itertools.combinations([1,2,3,4], 2))

    # determine the size of each sub-task
    ave, res = divmod(len(data), nprocs)
    counts = [ave + 1 if p < res else ave for p in range(nprocs)]

    # determine the starting and ending indices of each sub-task
    starts = [sum(counts[:p]) for p in range(nprocs)]
    ends = [sum(counts[:p+1]) for p in range(nprocs)]

    # converts data into a list of arrays 
    data = [data[starts[p]:ends[p]] for p in range(nprocs)]
else:
    data = None

data = comm.scatter(data, root=0)

for (ix, x), (iy, y) in data:
    os.system("python test.py {} {} {} {}".format(ix, x, iy, y))
    # print('Process {} {} has data:'.format(rank), x, y)