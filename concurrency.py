
import shelve
import multiprocessing
import os

filename = "tmp.shelve"
N = 4
end = 10000


def insert((offset, jump, end, filename)): 
    d = shelve.open(filename)
    for i in range(offset, end, jump):
        d[str(i)] = i

if os.path.exists(filename):
    os.unlink(filename)

pool = multiprocessing.Pool(processes=N)
pool.map(insert, zip(range(1, N+1), [N]*N, [end]*N, [filename]*N))

d = shelve.open(filename)
sorted(map(int, d.keys()))[:20]
