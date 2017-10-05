import io
import os.path
import subprocess
import sys
import time

def generate():
    for i in xrange(0, 20):
        print 'line ' + str(i)
        sys.stdout.flush()
        time.sleep(0.3)

def invoke_subprocess(bufsize):
    return subprocess.Popen('python ' + os.path.abspath(__file__) + ' --generate', shell=True, stdout=subprocess.PIPE, bufsize=bufsize)

def subprocess_communicate(bufsize):
    p = invoke_subprocess(bufsize)
    while p.returncode is None:
        (stdout, stderr) = p.communicate()
        for line in stdout.splitlines():
            yield line

def io_open():
    p = invoke_subprocess(1)
    for line in io.open(p.stdout.fileno()):
        yield line.rstrip('\n')

def demo():
    for (name, fn) in {
        'unbuffered p.communicate()': lambda: subprocess_communicate(0),
        'line buffered p.communicate()': lambda: subprocess_communicate(1),
        'io.open(p.stdout)': lambda: io_open(),
    }.iteritems():
        start = time.time()
        first = None
        stop = None
        lines = []
        for line in fn():
            lines.append(line)
            if first is None:
                first = time.time()
        stop = time.time()
        print name + ': ' + str(len(lines)) + ' received'
        if first is not None:
            print name + ': ' + str(first - start) + ' seconds until first line'
        print name + ': ' + str(stop - start) + ' seconds until all lines'

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--generate':
        generate()
    else:
        demo()
