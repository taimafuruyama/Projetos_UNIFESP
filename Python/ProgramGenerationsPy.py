# -*- coding: utf-8 -*-

import numpy
import random

# Number of Generations
# Generation 0 always have only 1 patient
# Generations 1 and forward have the number of patients defined in the PATIENTS variable
Generations = 2

# this array is called inside the RunPatients function
# it is an array because if there is increment from the infection cycle from one patient to another,
# different values for infection cycle have to be stored
InfectionCycle = [ 2, 4 ]

# Number of Patients in Generation 1
Gen1Patients = 4

# Number of Cycles
Cycles = 10

# Number of Classes
Classes = 11

# Matrix containing all the data (generations, patients, cycles and classes)
Matrix = []

# The "InitialParticles" is the initial amount of viral particles, that is: the initial virus population of a infection.
InitialParticles = 5

InfectionParticles = 20

# Limite máximo de partículas que quero impor para cada ciclo (linha)	
MaxParticles = 1000000

DeleteriousProbability = [0] * Cycles
BeneficialProbability = [0] * Cycles

# if TRUE, beneficial probability will increase by INCREMENT each cycle
# if FALSE, it will change from a fixed value to another fixed value, at the chosen cycle
BeneficialIncrement = False

# if TRUE, deleterious probability will increase by INCREMENT each cycle
# if FALSE, it will change from a fixed value to another fixed value, at the chosen cycle
DeleteriousIncrement = False

# Lists to keep the number of particles that go up or down the classes, during mutations
# So, for example, the list ClassUpParticle[0][1, 4] will keep the number of particles
# that went up 1 class, in GENERATION 0, PATIENT 1, CYCLE 4

ClassUpParticles = []
ClassDownParticles = []

def main():

    #Random rnd = new Random()

    # number of patients at 1st generation is defined by the number of cycles that 
    # occur infection
    #Gen1Patients = InfectionCycle.GetLength(0)

    # create and start the Stopwatch Class. From: https://msdn.microsoft.com/en-us/library/system.diagnostics.stopwatch
    #Stopwatch stopWatch = new Stopwatch()
    #stopWatch.Start()
    #Thread.Sleep(10000);

    # Declaring the three-dimensional Matrix: 
    # it has p Patient, x lines of Cycles and y columns of Classes, 
    # defined by the variables above. 

    for g in range(Generations):
        Matrix.append([])
        ClassUpParticles.append([])
        ClassDownParticles.append([])
    
        # numpy.zeros fills the array with zeros (0) in each position
        Matrix[g] = numpy.zeros((pow(Gen1Patients, g), Cycles, Classes))
        ClassUpParticles[g] = numpy.zeros((pow(Gen1Patients, g), Cycles))
        ClassDownParticles[g] = numpy.zeros((pow(Gen1Patients, g), Cycles))

	#FillInfectionCycleArray(6, 0); // FIRST PARAMETER: initial cycle, SECOND PARAMENTER: increment

    if DeleteriousIncrement == True:
        FillDeleteriousArrayWithIncrement(0.3, 0.1)
        # FIRST PARAMETER: initial probability
        # SECOND PARAMENTER: increment

    else:
        FillDeleteriousArray(0.8, 0.9, 5)
        # FIRST PARAMETER: first probability
        # SECOND PARAMENTER: second probability
        # THIRD PARAMETER: cycle to change from first probability to second probability

    if BeneficialIncrement == True:
        FillBeneficialArrayWithIncrement(0.0003, 0.0001)
        # FIRST PARAMETER: initial probability
        # SECOND PARAMENTER: increment

    else:
        FillBeneficialArray(0.0003, 0.0008, 5)
        # FIRST PARAMETER: first probability
        # SECOND PARAMENTER: second probability
        # THIRD PARAMETER: cycle to change from first probability to second probability
        
    # The Matrix starts on the Patient 0, 10th position (column) on the line zero. 
    # The "InitialParticles" is the amount of viral particles that exists in the class 10 on the cycle zero.
    # That is: these 5 particles have the potential to create 10 particles each.

    Matrix[0][0, 0, 10] = InitialParticles

    RunPatients(Matrix)

    #stopWatch.Stop()
    # Get the elapsed time as a TimeSpan value.
    #TimeSpan ts = stopWatch.Elapsed

    PrintOutput(Matrix)

    # Format and display the TimeSpan value.
    #string elapsedTime = String.Format("{0:00}:{1:00}:{2:00}.{3:00}", ts.Hours, ts.Minutes, ts.Seconds, ts.Milliseconds / 10);
    #OutputConsole.AppendText(Environment.NewLine);
    #OutputConsole.AppendText("Total Run Time: " + elapsedTime);

def FillDeleteriousArray(FirstProbability, SecondProbability, ChangeCycle):
    for i in range(Cycles):
        if i <= ChangeCycle:
            DeleteriousProbability[i] = FirstProbability
                
        else:
            DeleteriousProbability[i] = SecondProbability

def FillDeleteriousArrayWithIncrement(InitialProbability, Increment):
    for i in range(Cycles):
        if i == 0:
            DeleteriousProbability[i] = InitialProbability
            
        else:
            if (DeleteriousProbability[i - 1] + Increment <= (1 - BeneficialProbability.GetLength(0))):
                DeleteriousProbability[i] = DeleteriousProbability[i - 1] + Increment
            
            else:
                DeleteriousProbability[i] = DeleteriousProbability[i - 1]

def FillBeneficialArray(FirstProbability, SecondProbability, ChangeCycle):
    for i in range(Cycles):
        if i <= ChangeCycle:
            BeneficialProbability[i] = FirstProbability
        else:
            BeneficialProbability[i] = SecondProbability

def FillBeneficialArrayWithIncrement(InitialProbability, Increment):
    for i in range(Cycles):
        if i == 0:
            BeneficialProbability[i] = InitialProbability
        else:
            if (BeneficialProbability[i - 1] + Increment <= (1 - DeleteriousProbability.GetLength(0))):
                BeneficialProbability[i] = BeneficialProbability[i - 1] + Increment
            else:
                BeneficialProbability[i] = BeneficialProbability[i - 1]

def RunPatients(Matrix):
    # Main Loop to create more particles on the next Cycles from the Cycle Zero (lines values).
    # Each matrix position will bring a value. This value will be mutiplied by its own class number (column value). 
    for g in range(Generations):
        for p in range(pow(Gen1Patients, g)): # pow(Gen1Patients, g) gives the generation size
            print(f"Patient started: GEN {g} - P {p}")
            
            for Cy in range(Cycles):
                for Cl in range(Classes):
                    if(Cy > 0):
                        # Multiplies the number os particles from de previous Cycle by the Class number which belongs.
                        # This is the progeny composition.
                        #Matrix[p, i, j] = Matrix[p, (i - 1), j] * j;
                        Matrix[g][p, Cy, Cl] = Matrix[g][p, (Cy - 1), Cl] * Cl
                
                CutOffMaxParticlesPerCycle(Matrix, g, p, Cy)
                ApplyMutationsProbabilities(Matrix, g, p, Cy)

				# if the INFECTIONCYLE array contains the cycle "i"
				# and it is not the last generation, make infection
                if Cy in InfectionCycle:
                    if g < Generations - 1:
                        PickRandomParticlesForInfection(Matrix, g, p, Cy)
					    #Console.WriteLine("*** INFECTION CYCLE *** {0}", i);

					    # print which Cycle was finished just to give user feedback, because it may take too long to run.
					    #Console.WriteLine("Cycles processed: {0}", i);
					    #Console.WriteLine("Patients processed: GEN {0} - P {1}", g, p);

def ApplyMutationsProbabilities(Matrix, g, p, Cy):
    # This function will apply three probabilities: Deleterious, Beneficial or Neutral.
    # Their roles is to simulate real mutations of virus genome.
    # So here, there are mutational probabilities, which will bring an 
    # stochastic scenario sorting the progenies by the classes.

    UpParticles = 0
    DownParticles = 0 

	# array to store the number of particles of each class, in the current cycle
    ThisCycle = [0] * Classes

    for j in range(Classes):
        # storing the number of particles of each class (j)
        ThisCycle[j] = Matrix[g][p, Cy, j]
        
    for j in range(Classes):
        if (ThisCycle[j] > 0 & Cy > 0):
            for particles in range(j):
                # In this loop, for each particle removed from the Matrix [i,j], a random number is selected.
                # Here a random (float) number greater than zero and less than one is selected.
                RandomNumber = random.random()
                
                # If the random number is less than the DeleteriousProbability 
                # defined, one particle of the previous Cycle will 
                # decrease one Class number. Remember this function is 
                # inside a loop for each i and each j values.
                # So this loop will run through the whole Matrix, 
                # particle by particle on its own positions. 

                if RandomNumber < DeleteriousProbability[Cy]:
                    # Deleterious Mutation = 90,0% probability (0.9)
                    Matrix[g][p, Cy, (j - 1)] = Matrix[g][p, Cy, (j - 1)] + 1
                    Matrix[g][p, Cy, j] = Matrix[g][p, Cy, j] - 1
                    
                    DownParticles += 1
                
                elif (RandomNumber < (DeleteriousProbability[Cy] + BeneficialProbability[Cy])):
                    # Beneficial Mutation = 0,5% probability (0.005)
                    if (j < (Classes - 1)):
                        Matrix[g][p, Cy, (j + 1)] = Matrix[g][p, Cy, (j + 1)] + 1
                        Matrix[g][p, Cy, j] = Matrix[g][p, Cy, j] - 1
                    if (j == Classes):
                        Matrix[g][p, Cy, j] = Matrix[g][p, Cy, j] + 1
                        
                    UpParticles += 1

    ClassUpParticles[g][p, Cy] = UpParticles
    ClassDownParticles[g][p, Cy] = DownParticles

def ParticlesInCycle(Matrix, g, p, Cy):
    # This funtion brings the sum value of particles by Cycle. 
    Particles = 0
    
    for j in range(Classes):
        Particles = Particles + Matrix[g][p, Cy, j]
        
    return Particles

def CutOffMaxParticlesPerCycle(Matrix, g, p, Cy):
    
    # Quantidade de partículas somadas por ciclo (linha)
    ParticlesInThisCycle = ParticlesInCycle(Matrix, g, p, Cy)
    
    # Declarando o array que é a lista abaixo
    StatusR = [0] * Classes
    
    # Se, x = ParticlesInCycle, for maior do que o núm MaxParticles definido, então...
    if ParticlesInThisCycle > MaxParticles:
        # Para cada valor de x iniciando no valor de soma das partículas por ciclo;
	    # sendo x, ou seja, esta soma, maior do que o limite MaxParticles definido;
	    # então, diminua em uma unidade a soma das partículas por ciclo 
	    # até que atinja o limite MaxParticles definido.

        # conversion of Numpy Float 64 do int
        # ParticlesInThisCycle.astype(numpy.int64)

        for particles in range(MaxParticles, ParticlesInThisCycle.astype(numpy.int64)):
            
            StatusR[0] = Matrix[g][p, Cy, 0]
            StatusR[1] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1]
            StatusR[2] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2]
            StatusR[3] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3]
            StatusR[4] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4]
            StatusR[5] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4] + Matrix[g][p, Cy, 5]
            StatusR[6] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4] + Matrix[g][p, Cy, 5] + Matrix[g][p, Cy, 6]
            StatusR[7] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4] + Matrix[g][p, Cy, 5] + Matrix[g][p, Cy, 6] + Matrix[g][p, Cy, 7]
            StatusR[8] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4] + Matrix[g][p, Cy, 5] + Matrix[g][p, Cy, 6] + Matrix[g][p, Cy, 7] + Matrix[g][p, Cy, 8]
            StatusR[9] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4] + Matrix[g][p, Cy, 5] + Matrix[g][p, Cy, 6] + Matrix[g][p, Cy, 7] + Matrix[g][p, Cy, 8] + Matrix[g][p, Cy, 9]
            StatusR[10] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4] + Matrix[g][p, Cy, 5] + Matrix[g][p, Cy, 6] + Matrix[g][p, Cy, 7] + Matrix[g][p, Cy, 8] + Matrix[g][p, Cy, 9] + Matrix[g][p, Cy, 10]

			# Gero um número aleatório de 0 ao limite do valor de soma de partículas por 
			# ciclo (linha) = ParticlesInCycle
			#int RandomMaxParticles;
            #rndParticle = random.randint(0, ParticlesInThisCycle)
            rndParticle = numpy.random.randint(ParticlesInThisCycle)
            
            # Aqui gero as condições para saber de qual classe serão retiradas as partículas para que 
            # ParticlesInCycle atinja o limite estipulado por MaxParticles
            
            if (rndParticle > 0 and rndParticle <= StatusR[0]):
                Matrix[g][p, Cy, 0] = Matrix[g][p, Cy, 0] - 1
                
            if (rndParticle > StatusR[0] and rndParticle <= StatusR[1]):
                Matrix[g][p, Cy, 1] = Matrix[g][p, Cy, 1] - 1
                
            if (rndParticle > StatusR[1] and rndParticle <= StatusR[2]):
                Matrix[g][p, Cy, 2] = Matrix[g][p, Cy, 2] - 1
                
            if (rndParticle > StatusR[2] and rndParticle <= StatusR[3]):
                Matrix[g][p, Cy, 3] = Matrix[g][p, Cy, 3] - 1
                
            if (rndParticle > StatusR[3] and rndParticle <= StatusR[4]):
                Matrix[g][p, Cy, 4] = Matrix[g][p, Cy, 4] - 1
                
            if (rndParticle > StatusR[4] and rndParticle <= StatusR[5]):
                Matrix[g][p, Cy, 5] = Matrix[g][p, Cy, 5] - 1
                
            if (rndParticle > StatusR[5] and rndParticle <= StatusR[6]):
                Matrix[g][p, Cy, 6] = Matrix[g][p, Cy, 6] - 1
                
            if (rndParticle > StatusR[6] and rndParticle <= StatusR[7]):
                Matrix[g][p, Cy, 7] = Matrix[g][p, Cy, 7] - 1
                
            if (rndParticle > StatusR[7] and rndParticle <= StatusR[8]):
                Matrix[g][p, Cy, 8] = Matrix[g][p, Cy, 8] - 1
                
            if (rndParticle > StatusR[8] and rndParticle <= StatusR[9]):
                Matrix[g][p, Cy, 9] = Matrix[g][p, Cy, 9] - 1
                
            if (rndParticle > StatusR[9] and rndParticle <= StatusR[10]):
                Matrix[g][p, Cy, 10] = Matrix[g][p, Cy, 10] - 1

def PickRandomParticlesForInfection(Matrix, g, p, Cy):
    NoParticlesForInfection = False
    
    # array to store the particles that will infect patients of the next generation
    # it is just a 1D array (a list) where each index is a class
    InfectedParticles = [0] *Classes
    
    # Quantidade de partículas somadas por ciclo (linha)
    ParticlesInThisCycle = ParticlesInCycle(Matrix, g, p, Cy)
    StatusR = [0] * Classes; # TODO melhorar o nome deste array

	#for (int ParticlesSelected = 0; ParticlesSelected < InfectionParticles; ParticlesSelected++):
    for ParticlesSelected in range(InfectionParticles):
        StatusR[0] = Matrix[g][p, Cy, 0]
        StatusR[1] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1]
        StatusR[2] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2]
        StatusR[3] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3]
        StatusR[4] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4]
        StatusR[5] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4] + Matrix[g][p, Cy, 5]
        StatusR[6] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4] + Matrix[g][p, Cy, 5] + Matrix[g][p, Cy, 6]
        StatusR[7] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4] + Matrix[g][p, Cy, 5] + Matrix[g][p, Cy, 6] + Matrix[g][p, Cy, 7]
        StatusR[8] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4] + Matrix[g][p, Cy, 5] + Matrix[g][p, Cy, 6] + Matrix[g][p, Cy, 7] + Matrix[g][p, Cy, 8]
        StatusR[9] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4] + Matrix[g][p, Cy, 5] + Matrix[g][p, Cy, 6] + Matrix[g][p, Cy, 7] + Matrix[g][p, Cy, 8] + Matrix[g][p, Cy, 9]
        StatusR[10] = Matrix[g][p, Cy, 0] + Matrix[g][p, Cy, 1] + Matrix[g][p, Cy, 2] + Matrix[g][p, Cy, 3] + Matrix[g][p, Cy, 4] + Matrix[g][p, Cy, 5] + Matrix[g][p, Cy, 6] + Matrix[g][p, Cy, 7] + Matrix[g][p, Cy, 8] + Matrix[g][p, Cy, 9] + Matrix[g][p, Cy, 10]
        
        # Gero um número aleatório de 0 ao limite do valor de soma de partículas por ciclo (linha) = ParticlesInCycle
        #int RandomMaxParticles;
        
        if (ParticlesInThisCycle > 0):

            #rndParticle = random.randint(0, ParticlesInThisCycle)
            rndParticle = numpy.random.randint(ParticlesInThisCycle)
            
            # Aqui gero as condições para saber de qual classe serão retiradas as partículas para que 
            # ParticlesSelected atinja o limite estipulado por InfectioParticles 
            
            if (rndParticle > 0 and rndParticle <= StatusR[0]):
                InfectedParticles[0] += 1
                Matrix[g][p, Cy, 0] -= 1
                
            if (rndParticle > StatusR[0] and rndParticle <= StatusR[1]):
                InfectedParticles[1] += 1
                Matrix[g][p, Cy, 1] -= 1
                
            if (rndParticle > StatusR[1] and rndParticle <= StatusR[2]):
                InfectedParticles[2] += 1
                Matrix[g][p, Cy, 2] -= 1
                
            if (rndParticle > StatusR[2] and rndParticle <= StatusR[3]):
                InfectedParticles[3] += 1
                Matrix[g][p, Cy, 3] -= 1
                
            if (rndParticle > StatusR[3] and rndParticle <= StatusR[4]):
                InfectedParticles[4] += 1
                Matrix[g][p, Cy, 4] -= 1
                
            if (rndParticle > StatusR[4] and rndParticle <= StatusR[5]):
                InfectedParticles[5] += 1
                Matrix[g][p, Cy, 5] -= 1
                
            if (rndParticle > StatusR[5] and rndParticle <= StatusR[6]):
                InfectedParticles[6] += 1
                Matrix[g][p, Cy, 6] -= 1
                
            if (rndParticle > StatusR[6] and rndParticle <= StatusR[7]):
                InfectedParticles[7] += 1
                Matrix[g][p, Cy, 7] -= 1
                
            if (rndParticle > StatusR[7] and rndParticle <= StatusR[8]):
                InfectedParticles[8] += 1
                Matrix[g][p, Cy, 8] -= 1
                
            if (rndParticle > StatusR[8] and rndParticle <= StatusR[9]):
                InfectedParticles[9] += 1
                Matrix[g][p, Cy, 9] -= 1
                
            if (rndParticle > StatusR[9] and rndParticle <= StatusR[10]):
                InfectedParticles[10] += 1
                Matrix[g][p, Cy, 10] -= 1
                
        else:
            NoParticlesForInfection = True
            
    # if there are no particles for infection, there is no infection
    if (NoParticlesForInfection):
        print(f"Patient {p} Cycle {Cy} has no particles.")
        
    else:
        InfectPatients(Matrix, InfectedParticles, g, p, Cy)

def InfectPatients(Matrix, InfectedParticles, g, p, Cy):
    AmountOfParticlesAvailable = InfectedParticles[0] + InfectedParticles[1] + InfectedParticles[2] + InfectedParticles[3] + InfectedParticles[4] + InfectedParticles[5] + InfectedParticles[6] + InfectedParticles[7] + InfectedParticles[8] + InfectedParticles[9] + InfectedParticles[10]
    
    #Console.WriteLine(AmountOfParticlesAvailable);
    
    PatientsToInfect = [0] * Gen1Patients
    
    # each patient will infect a group of patients of size Gen1Patients
    LastPatient = ((p + 1) * Gen1Patients) - 1; # the last patient of this group
    FirstPatient = LastPatient - (Gen1Patients - 1); # the first patient of this group
    
    for x in range(Gen1Patients):
        PatientsToInfect[x] = FirstPatient + x
        #Console.WriteLine(PatientsToInfect[x]);
        
    #Console.WriteLine(FirstPatient);
    #Console.WriteLine(LastPatient);
    
    # looks for the first occurrence of the required patient
    # Example: Cycle 6. If InfectionCycle = [ 2, 4, 6 ], so InfectionCycle.index(Cy) = 2
    # So, patient = PatientsToInfect[2]
    patient = PatientsToInfect[InfectionCycle.index(Cy)]
    
    while (AmountOfParticlesAvailable > 0):
        rndClass = random.randint(0, Classes - 1)
        
        if (InfectedParticles[rndClass] > 0): # there is at least one particle in the class selected
            Matrix[g + 1][patient, 0, rndClass] += 1
            #ParticlesReceived[patient] += 1
            InfectedParticles[rndClass] -= 1
            AmountOfParticlesAvailable -= 1

        #Console.WriteLine("G {0} P {1} infected G {2} P {3}", g, p, g + 1, patient)

def PrintOutput(Matrix):
    PercentageOfParticlesUp = 0.0
    PercentageOfParticlesDown = 0.0
    
    #StreamWriter writer = new StreamWriter("numbers.txt");
    # The writer will bring the output file (txt in this case)
    # Ensure the writer will be closed when no longer used
    #using (writer)
        # Formatting Output for the Console screen. 
        #OutputConsole.AppendText("\t\tR0\tR1\tR2\tR3\tR4\tR5\tR6\tR7\tR8\tR9\tR10")
        #OutputConsole.AppendText(Environment.NewLine)
        #OutputConsole.AppendText(Environment.NewLine)
        #writer.Write("\t\tSoma\tR0\tR1\tR2\tR3\tR4\tR5\tR6\tR7\tR8\t\tR9\t\tR10\n\n");
        #writer.WriteLine("\n");
        
    for g in range(Generations):
        for p in range(pow(Gen1Patients, g)):
            for Cy in range(Cycles):
                #OutputConsole.AppendText("G " + g + " P " + p + " Cycle " + i + "\t")
                #writer.Write("G {0} P {1} Cic.{2} {3}\t\t", g, p, i, ParticlesInCycle(Matrix, g, p, i));
                
                for Cl in range(Classes):
                    #OutputConsole.AppendText(Matrix[g][p, i, j].ToString() + "\t")
                    #writer.Write("{0}\t", Matrix[g][p, i, j]);
                    
                    PercentageOfParticlesUp = (Convert.ToDouble(ClassUpParticles[g][p, Cy]) / Convert.ToDouble(ParticlesInCycle(Matrix, g, p, Cy))) * 100
                    PercentageOfParticlesDown = (Convert.ToDouble(ClassDownParticles[g][p,Cy]) / Convert.ToDouble(ParticlesInCycle(Matrix, g, p, Cy))) * 100

				    #Console.WriteLine("\nSoma do ciclo {0}: {1}", i, ParticlesInCycle(Matrix, g, p, i))
				    #Console.WriteLine("Particles Up: {0}, {1} %", ClassUpParticles[g][p, i], PercentageOfParticlesUp)
				    #Console.WriteLine("Particles Down: {0}, {1} %", ClassDownParticles[g][p, i], PercentageOfParticlesDown)
				    #Console.Write("\n");

				    #OutputConsole.AppendText(Environment.NewLine)
				    #OutputConsole.AppendText(Environment.NewLine)
				    #writer.WriteLine("\n");

			    #OutputConsole.AppendText("******************************************************" +
			    #OutputConsole.AppendText(Environment.NewLine)

main()
