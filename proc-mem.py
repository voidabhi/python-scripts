#!/usr/bin/env python
import os
import sys

def show_usage():
    sys.stderr.write('''memio - Simple I/O for /proc/<pid>/mem
Dump /proc/<pid>/maps:
    memio.py <pid>
Read from or write to (when some input is present on stdin) memory:
    memio.py <pid> <start> (<end> | +<size>)
    memio.py <pid> <hexrange>
    <hexrange> is in /proc/<pid>/maps format (e.g., 00400000-004f2000).
''')
    sys.exit(1)

def parse_args():
    n_args = len(sys.argv)
    start = end = None
    pid = int(sys.argv[1], 0)
    if n_args == 3:
        start, end = map(lambda x: int(x, 16), sys.argv[2].split('-'))
    elif n_args == 4:
        start = int(sys.argv[2], 0)
        if sys.argv[3][0] == '+':
            end = start + int(sys.argv[3][1:], 0)
        else:
            end = int(sys.argv[3], 0)
    return pid, start, end

def mem_io_range(pid, start, end, stream, read):
    page_size = os.sysconf('SC_PAGE_SIZE')
    mode = os.O_RDONLY if read else os.O_WRONLY
    fd = os.open('/proc/{}/mem'.format(pid), mode)
    os.lseek(fd, start, os.SEEK_SET)
    to_do = end - start
    while to_do > 0:
        chunk_size = min(to_do, page_size)
        if read:
            data = os.read(fd, chunk_size)
            stream.write(data)
        else:
            data = stream.read(chunk_size)
            if not data:
                to_do = 0
            os.write(fd, data)
        to_do -= chunk_size
    os.close(fd)

def dump_maps(pid, sink):
    with open('/proc/{}/maps'.format(pid)) as maps:
        sink.write(maps.read())

def main():
    if len(sys.argv) not in (2, 3, 4):
        show_usage()
    pid, start, end = parse_args()
    if start and end:
        if sys.stdin.isatty():
            mem_io_range(pid, start, end, sys.stdout, True)
        else:
            mem_io_range(pid, start, end, sys.stdin, False)
    else:
        dump_maps(pid, sys.stdout)

if __name__ == '__main__':
    main()
