# -*- coding: utf-8 -*-
"""
Created on Thu May 16 15:48:54 2019

@author: luken
"""

class Cluster:
    def __init__(self, title, mean, path):
        self.title = title
        self.mean = mean
        self.path = path
        self.members = []