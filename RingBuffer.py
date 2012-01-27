import numpy as np

class RingBuffer:
    def __init__(self,size_max=5,default=0,data=[]):
        self.max = size_max
        self.default = default
        self.data = list(data)
        self.index = len(data) % self.max
        self.count = len(data) # number of non-default values in RingBuffer
        self.data.extend([default for i in range(self.max-len(self.data))])

    def write(self,x):
        "writes value into ring buffer"
        self.data[self.index] = x
        if self.index + 1 > self.count:
            self.count = self.index + 1
        self.index = (self.index + 1) % self.max
    def empty(self):
        "clears data list"
        self.data = [default for i in self.data]
        self.count = 0

    def get(self):
        "returns a list of elements from oldest to newest"
        return self.data[self.index:] + self.data[:self.index]
    def get_prev(self,i):
        "returns nth previous element"
        return self.data[(self.index - i) % self.max]
    def get_last(self):
        "returns last element"
        return self.get_prev(1)

    def set_prev(self,i,value):
        "sets nth previous element"
        self.data[(self.index - i) % self.max] = value
    def set_last(self,value):
        "sets last element"
        self.set_prev(1,value)

    # FIXME below functions only work for integer values right now, not objects
    def average(self):
        "returns average of data vector"
        return np.average(self.data)
    def meanmagnitude(self):
        "returns average magnitude of data vector"
        return np.sqrt(np.dot(self.data,self.data))/self.max
