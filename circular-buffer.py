#!/usr/bin/python

class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None
    def __repr__(self):
        return "Node[%s]" % self.value

class CircularBuffer(object):
    def __init__(self, size):
        if size <= 0:
            raise AttributeError("Size must be positive")
        self.size = int(size)
        self.start = None
        self.end = None
        self.arr = [None for x in range(0, self.size)]

    def next_index(self, ind):
        return (ind + 1) % len(self.arr)

    def enqueue(self, value):
        if self.start is None and self.end is None:
            self.arr[0] = value
            self.start = self.end = 0
        else:
            self.end = self.next_index(self.end)
            self.arr[self.end] = value
            if self.end == self.start:
                self.start = self.next_index(self.start)

    def dequeue(self):
        if self.start is None:
            raise ValueError("Empty buffer")
        elem = self.arr[self.start]
        if self.start == self.end:
            self.start = self.end = None
        else:
            self.start = self.next_index(self.start)
        return elem

    def debug(self):
        print "State:"
        print "  arr = %s" % self.arr
        print "  start = %s" % (self.arr[self.start] if self.start is not None else "None")
        print "  end = %s" % (self.arr[self.end] if self.end is not None else "None")
