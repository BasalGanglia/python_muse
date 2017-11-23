#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 15:21:32 2017

@author: ikosunen
"""
import numpy as np


## Simple ringbuffer, copied from:
# https://scimusing.wordpress.com/2013/10/25/ring-buffers-in-pythonnumpy/
# by ??
# with few modifications by me...


class RingBuffer():
    "A 1D ring buffer using numpy arrays"
    def __init__(self, length):
        self.data = np.zeros(length, dtype='f')
        self.index = 0

    def extend(self, x):
        "adds array x to ring buffer"
        x_index = (self.index + np.arange(1)) % self.data.size
        self.data[x_index] = x
        self.index = x_index[-1] + 1

    def get(self):
        "Returns the first-in-first-out data in the ring buffer"
        idx = (self.index + np.arange(self.data.size)) %self.data.size
        return self.data[idx]
    def get_index(self):
        return self.index
    
    def get_last_n(self,n):
        idx = (self.index + np.arange(self.data.size)) %self.data.size
        return self.data[idx[-n:]]
        
