#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 13:44:19 2017
Tribute module to 'Introduction into computer linguistics'

@author: christopher
"""

from enum import Enum

class Ordinal (Enum):
    N  = ('N' ,  0, -1)
    NE = ('NE',  1, -1)
    E  = ('E' ,  1,  0)
    SE = ('SE',  1,  1)
    S  = ('S' ,  0,  1)
    SW = ('SW', -1,  1)
    W  = ('W' , -1,  0)
    NW = ('NW', -1, -1)
    
    def getName (self):
        return self.value[0]
    
    def getDX (self):
        return self.value[1]
    
    def getDY (self):
        return self.value[2]
    
    def __str__ (self):
        return '%s (%s, %s)' % (self.getName().ljust(2),
                    str(self.getDX()).rjust(3), 
                    str(self.getDY()).rjust(3))
        
    def invert (self):
        lk = {Ordinal.N  : Ordinal.S,
              Ordinal.NE : Ordinal.SW,
              Ordinal.E  : Ordinal.W,
              Ordinal.SE : Ordinal.NW,
              
              Ordinal.S : Ordinal.N,
              Ordinal.SW : Ordinal.NE,
              Ordinal.W : Ordinal.E,
              Ordinal.NW : Ordinal.SE,
              }
        return lk[self]
    

class Operation(Enum):
    ROOT    = (None, 0),
    INSERT  = (Ordinal.E , 1) 
    DELETE  = (Ordinal.S , 1) 
    REPLACE = (Ordinal.SE, 2) 
    MATCH   = (Ordinal.SE, 0)
	
    @classmethod
    def getCost (self):
        return self.value[1]
    
    @classmethod
    def getOrdinal(self):
        return self.value[0]
    
class Role (Enum):
    ORIGIN     = 0
    BETWEEN    = 1
    END        = 2
    SINGLE     = 3
    UNDEFINIED = 4

class MEDField:
    
    def __init__ (self, pos = (0, 0), isEnd, role):
        self.pos = pos
        self.isEnd = isEnd
        self.role = role
    
    def setToAlphaOmega (self):
        self.role = Role.SINGLE
        
    def setCost(self, cost):
        self.cost = cost

#def calculateMinimumEditDistance(leftWord, rightWord):
   
   
for cd in Ordinal:
    print(cd, cd.invert())
    

    
