from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import multiprocessing
from multiprocessing.pool import ThreadPool
import threading
import time


def bar(i=0):
    if i == 0:
        raise ValueError("bar raise")
    return i ** 2


def main_Thread():
    thread = threading.Thread(target=bar)
    thread.start()
    thread.join()
    raise RuntimeError("Exception not caught")


def main_ThreadPool():
    p = ThreadPool(4)
    for i in p.map(bar, xrange(4)):
        print i
    raise RuntimeError("Exception not caught")


def main_ThreadPoolExecutorMap():
    with ThreadPoolExecutor(4) as ex:
        for i in ex.map(bar, xrange(4)):
            print i
    raise RuntimeError("Exception not caught")


def main_ThreadPoolExecutorSubmit():
    with ThreadPoolExecutor(4) as ex:
        s = ex.submit(bar)
        print s.result()
    raise RuntimeError("Exception not caught")


def main_Process():
    thread = multiprocessing.Process(target=bar)
    thread.start()
    thread.join()
    raise RuntimeError("Exception not caught")


def main_ProcessPool():
    p = multiprocessing.Pool(4)
    for i in p.map(bar, xrange(4)):
        print i
    raise RuntimeError("Exception not caught")


def main_ProcessPoolExecutorMap():
    with ProcessPoolExecutor(4) as ex:
        for i in ex.map(bar, xrange(4)):
            print i
    raise RuntimeError("Exception not caught")


def main_ProcessPoolExecutorSubmit():
    with ProcessPoolExecutor(4) as ex:
        s = ex.submit(bar, 0)
        print s.result()
    raise RuntimeError("Exception not caught")


def run(fun):
    ac = threading.active_count()
    try:
        fun()
    except RuntimeError:
        print fun.__name__, "[NOT raised]"
    except ValueError:
        print fun.__name__, "[RAISED]"
    time.sleep(1)
    print "Zombie thread:", threading.active_count() - ac

if __name__ == '__main__':
    run(main_Thread)
    run(main_ThreadPool)
    run(main_ThreadPoolExecutorMap)
    run(main_ThreadPoolExecutorSubmit)
    run(main_Process)
    run(main_ProcessPool)
    run(main_ProcessPoolExecutorMap)
    run(main_ProcessPoolExecutorSubmit)
