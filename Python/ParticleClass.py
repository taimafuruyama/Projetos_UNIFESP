# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 23:42:45 2019

@author: Marcos
"""

class Particle():
    
    __slots__ = ('R')
    
    def __init__(self, RClass):
        self.R = RClass # R Class from R0 to R10. self.Class is an INT
        
#        self.id = ID
#        self.id = Particle.ParticleIdCounter
        
    def RaiseClass(self):
        
        if(self.R < 10):
            self.R = self.R + 1
    
    def DemoteClass(self):
          
        if(self.R == 0):
            self.__del__()
            
        else:
            self.R = self.R - 1
