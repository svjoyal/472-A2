# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 00:26:16 2022

@author: Sarah Joyal
"""

class PriorityQueue(object):
    """
    Attributes:
        queue = queue containing all values
    """
    
    def __init__(self):
        self.queue = []
        
    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.queue == other.queue

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        q = ''
        for item in self.queue:
            q += f'{item}, '
        return q

    def push(self, priority, data):
        self.queue.append((priority, data))
        self.sort()
        
    def pop(self):
        return self.queue.pop(0)
        
    def swap(self, a, b):
        self.queue[a], self.queue[b] = self.queue[b], self.queue[a]
    
    def empty(self):
        return len(self.queue) == 0
        
    def sort(self):
        l = len(self.queue)
        for i in range(l-1,-1,-1):
            if i >= 1 and self.queue[i][0] < self.queue[i-1][0]:
                self.swap(i, i-1)

