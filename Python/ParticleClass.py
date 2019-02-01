# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 23:42:45 2019

@author: Marcos
"""

import matplotlib.pyplot as plt

class Particle():
    
    ParticleAmount = 0 # amount of particles at any given time during runtime
    ParticleIdCounter = 0 # amount of ID generateds. It is the total number of particles generated
    
    def __init__(self, RClass):
        self.R = RClass # R Class from R0 to R10. But self.Class is an INT
        
        Particle.ParticleAmount += 1
        Particle.ParticleIdCounter += 1
        
        self.id = Particle.ParticleIdCounter
        
        self.PreviousClasses = None
        self.PreviousPatients = None
        
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
        
print("\n")
        
x = [Particle(0), Particle(5), Particle(10)]

a = Particle(1)
b = Particle(2)
c = Particle(3)

print("Particle Amount: " + str(c.ParticleAmount))

print("x[2] id: " + str(x[2].id))

print("x[2] Rclass: " + str(x[2].R))

x[2].RaiseClass()
x[2].DemoteClass()

print("x[2] Rclass: " + str(x[2].R))

print("x[0] Rclass: " + str(x[0].R))

x[0].RaiseClass()

print("x[0] Rclass: " + str(x[0].R))

x[0].DemoteClass()

x[0].DemoteClass()

print("Particle Amount: " + str(c.ParticleAmount))

#print(x[2].Class)

#print(c.id)
#
#print("Particle amount: " + str(c.ParticleAmount))
#
#del a
#
##print(a)
#
#print("Particle amount: " + str(x[0].ParticleAmount))


