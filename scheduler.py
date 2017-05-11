
"""
Usage:

>>>from schedule import schedule, run

>>>@schedule(hours=1)
>>>def my_task():
    print "Yolo Swag!"

>>>run()
"""



from dateutil.relativedelta import relativedelta
from datetime import datetime

tasks = {}

def schedule(**kwargs):
    def deco(f):
        tasks[f.__name__] = (datetime.utcnow(), relativedelta(**kwargs), f)
        return f
    return deco


def run():
    while True:
        time.sleep(1)
        for name, timeframe in tasks.items():
            last, gen, task = timeframe
            if datetime.utcnow() > last+gen:
                print "Running task %s" % name
                task()
                tasks[name] = (datetime.utcnow(), gen, task)
