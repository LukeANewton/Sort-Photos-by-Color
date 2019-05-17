# -*- coding: utf-8 -*-
"""
Created on Thu May 16 20:10:35 2019

@author: luken
"""

class ImageFeatures:
    def __init__(self, filename, brightness, majorityRed, majorityGreen, majorityBlue):
        self.filename = filename
        self.brightness = brightness
        self.majorityRed = majorityRed
        self.majorityGreen = majorityGreen
        self.majorityBlue = majorityBlue
        