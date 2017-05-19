#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 16:00:59 2017

@author: christopher
"""

def getMaximumColumnSizes (vals, keys = ['Name', 'Mail', 'Subject']):
    maxs = [0] * len(keys)
    
    for val in vals:
        for i in range(len(keys)):
            if len(str(val[keys[i]])) > maxs[i]:
                maxs[i] = len(str(val[keys[i]]))
                
    return tuple(maxs)