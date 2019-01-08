import matplotlib.pyplot as plt

class Particle():
    
    ParticleAmount = 0 # amount of particles at any given time during runtime
    ParticleIdCounter = 0 # amount of ID generateds. It is the total number of particles generated
    
    def __init__(self, Class):
        self.Class = Class
        
        Particle.ParticleAmount += 1
        Particle.ParticleIdCounter += 1
        
        self.id = Particle.ParticleIdCounter
        
        self.PreviousClasses = None
        self.PreviousPatients = None
        
    def RaiseClass():
        pass # adds 1 to the self.Class
    
    def DemoteClass():
        pass # subtracts 1 to the self.Class
        
    def __del__(self):
        Particle.ParticleAmount -= 1
        print("deleted")
        
x = [Particle(0), Particle(5), Particle(10)]

a = Particle(1)
b = Particle(2)
c = Particle(3)

print(x[2].Class)

print(c.id)

print("Particle amount: " + str(c.ParticleAmount))

del a

#print(a)

print("Particle amount: " + str(x[0].ParticleAmount))


