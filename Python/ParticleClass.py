# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 23:42:45 2019

@author: Marcos
"""

class Particle():
    
    ParticleAmount = 0 # amount of particles at any given time during runtime
    ParticleIdCounter = 0 # amount of ID generateds. It is the total number of particles generated
    
    def __init__(self, RClass):
        self.R = RClass # R Class from R0 to R10. But self.Class is an INT
        
        Particle.ParticleAmount += 1
        Particle.ParticleIdCounter += 1
        
        self.id = Particle.ParticleIdCounter
        
    def RaiseClass(self):
        
        if(self.R < 10):
            self.R = self.R + 1
    
    def DemoteClass(self):
          
        if(self.R == 0):
            self.__del__()
            
        else:
            self.R = self.R - 1
        
    def __del__(self):
        Particle.ParticleAmount -= 1
        print("deleted")
