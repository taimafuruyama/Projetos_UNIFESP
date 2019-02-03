# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 19:49:55 2019

@author: Taimá Furuyama
"""

import matplotlib.pyplot as plt
import random
import ParticleClass

from datetime import datetime

startTime = datetime.now()

        
print("\n")

ParticleArray = []
        
for i in range(100):
    ParticleArray.append(ParticleClass.Particle(10))
    
RandomTime = datetime.now()

rndParticles = random.sample(ParticleArray, 90)

#for i in rndParticles:
#    print(i.id)

ParticleArray.clear()

ParticleArray = rndParticles

#print("\n")
#print("Particle Array after sorting")
#
#for i in ParticleArray:
#    print(i.id)

print("\n")

print("Particle Array size: " + str(len(ParticleArray)))

print("Particle Amount: " + str(ParticleArray[0].ParticleAmount))

print("x[2] id: " + str(ParticleArray[0].id))

print("x[2] Rclass: " + str(ParticleArray[0].R))

ParticleArray[0].RaiseClass()
ParticleArray[0].DemoteClass()

print("x[2] Rclass: " + str(ParticleArray[0].R))

print("x[0] Rclass: " + str(ParticleArray[0].R))

ParticleArray[0].RaiseClass()

print("x[0] Rclass: " + str(ParticleArray[0].R))

ParticleArray[0].DemoteClass()

ParticleArray[0].DemoteClass()

print("Particle Amount: " + str(ParticleArray[0].ParticleAmount))

print("Total run time: " + str(datetime.now() - startTime) + "\n")
print("Random run time: " + str(datetime.now() - RandomTime) + "\n")


