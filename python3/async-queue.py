
# http://stackoverflow.com/questions/23864341/equivalent-of-asyncio-queues-with-worker-threads

import asyncio, random

q = asyncio.Queue()

@asyncio.coroutine
def produce():
    while True:
        yield from q.put(random.random())
        yield from asyncio.sleep(0.5 + random.random())

@asyncio.coroutine
def consume():
    while True:
        value = yield from q.get()
        print("Consumed", value)


loop = asyncio.get_event_loop()
loop.create_task(produce())
loop.create_task(consume())
loop.run_forever()

