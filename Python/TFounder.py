import numpy as np
import random

from numba import jit
from numba import cuda
from numba import vectorize

from datetime import datetime
import matplotlib.pyplot as plt
import xlsxwriter

import ParticleClass

# Number of Generations
# Generation 0 always have only 1 patient
# Generations 1 and forward have the number of patients defined in the PATIENTS variable
Generations = 3

# this array is called inside the RunPatients function
# it is an array because if there is increment from the infection cycle from one patient to another,
# different values for infection cycle have to be stored
InfectionCycle = [ 2, 4, 6, 8 ]

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

ClassOfInitialParticles = 10

InfectionParticles = 5

# Limite máximo de partículas que quero impor para cada ciclo (linha)	
MaxParticles = 100000

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

OutputFile = open('Testfile.txt', 'w') 

workbook = xlsxwriter.Workbook('Demo.xlsx')
worksheet = workbook.add_worksheet()
HorizAlign = workbook.add_format()
HorizAlign.set_align('center')

bold = workbook.add_format({'bold': True})
LastRowAvailable = 0

# set_column(column1, column2, size)
worksheet.set_column(0, 0, 10)
worksheet.set_column(13, 13, 5)
worksheet.set_column(14, 14, 12)
worksheet.set_column(15, 15, 10)
worksheet.set_column(16, 16, 13)
worksheet.set_column(17, 17, 13)
worksheet.set_column(18, 18, 16)

def main():
    
    global LastRowAvailable
    
    print("\nMain function started: " + str(datetime.now()) + "\n")
    startTime = datetime.now()

    # number of patients at 1st generation is defined by the number of cycles that 
    # occur infection
    #Gen1Patients = InfectionCycle.GetLength(0)

    # Declaring the three-dimensional Matrix: 
    # it has p Patients, Cy lines of Cycles, 
    # defined by the variables at the begginning of the code. 

    for g in range(Generations):
        Matrix.append([])
        ClassUpParticles.append([])
        ClassDownParticles.append([])
    
        PatientsPerGen = pow(Gen1Patients, g)
    
        # in the FOR LOOP below, we append 1 array for each patient.
        # and 1 array for each cycle.
        # we only append cycle here (Cycle 0) because the cycles will be maked at the time
        # each progeny is composed
        for patients in range(PatientsPerGen):
            Matrix[g].append([]) # patient
            Matrix[g][patients].append([]) # cycle
        
            ClassUpParticles[g].append([]) # patient
            ClassUpParticles[g][patients].append([]) # cycle
            
            ClassDownParticles[g].append([]) # patient
            ClassDownParticles[g][patients].append([]) # cycle

	#FillInfectionCycleArray(6, 0); // FIRST PARAMETER: initial cycle, SECOND PARAMENTER: increment

    if DeleteriousIncrement == True:
        FillDeleteriousArrayWithIncrement(0.3, 0.1)
        # FIRST PARAMETER: initial probability
        # SECOND PARAMENTER: increment

    else:
        FillDeleteriousArray(0.9, 0.9, 5)
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

    for i in range(InitialParticles):
        Matrix[0][0][0].append(ParticleClass.Particle(ClassOfInitialParticles))
      
#    print(Matrix[0][0][0][0])    
#        
#    for i in range(InitialParticles):
#        print(Matrix[0][0][0][i].id)

    RunPatients(Matrix)

    PrintOutput(Matrix)
    
    print("\nMain function ended: " + str(datetime.now()) + "\n")
    print("Total run time: " + str(datetime.now() - startTime) + "\n")
    print("Date: " + str(datetime.now()) + "\n")
    
    OutputFile.write("Total run time: " + str(datetime.now() - startTime) + "\n")
    OutputFile.write("Date: " + str(datetime.now()) + "\n")
    OutputFile.close()
    
    # worksheet.write(Row, Column, String, format)
    worksheet.write(LastRowAvailable, 0, "Total run time: " + str(datetime.now() - startTime), bold)
    worksheet.write(LastRowAvailable + 1, 0, "Date: " + str(datetime.now()), bold)
    workbook.close()

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
    
    global LastRowAvailable
    
    # print("RunPatients function started: " + str(datetime.now()) + "\n")
    
    # Main Loop to create more particles on the next Cycles from the Cycle Zero.
    # Each matrix position will bring a value. This value will be mutiplied by its own class number. 
    for g in range(Generations):
        for p in range(pow(Gen1Patients, g)): # pow(Gen1Patients, g) gives the generation size
            print("Patient started: GEN " + str(g) + " - P " + str(p))
            OutputFile.write("Patient started: GEN " + str(g) + " - P " + str(p) + "\n")
            worksheet.write(LastRowAvailable, 0, "Patient started: GEN " + str(g) + " - P " + str(p))
            LastRowAvailable += 1
            
            for Cy in range(Cycles):
                
                if(Cy > 0):
                    Matrix[g][p].append([]) # adds 1 cycle
                    
                    ClassUpParticles[g][p].append([]) # adds 1 cycle
                    ClassDownParticles[g][p].append([]) # adds 1 cycle
                
                    for particle in Matrix[g][p][Cy - 1]: # takes 1 particle from previous cycle
                        for i in range(particle.R): # creates N new particles, based on the R class
                            Matrix[g][p][Cy].append(ParticleClass.Particle(particle.R))
                
                CutOffMaxParticlesPerCycle(Matrix, g, p, Cy)
                ApplyMutationsProbabilities(Matrix, g, p, Cy)
                
                #print("Cycle " + str(Cy) + " " + str(Matrix[g][p, Cy]))

				# if the INFECTIONCYLE array contains the cycle "Cy"
				# and it is not the last generation, make infection
                if Cy in InfectionCycle:
                    if g < Generations - 1:
                        PickRandomParticlesForInfection(Matrix, g, p, Cy)

					    # print which Cycle was finished just to give user feedback, because it may take too long to run.
					    #print("Cycles processed: " + str(Cy));
					    #print("Patients processed: GEN " + str(g) + " - P " + str(p));
      
                
def ApplyMutationsProbabilities(Matrix, g, p, Cy):
    # This function will apply three probabilities: Deleterious, Beneficial or Neutral.
    # Their roles is to simulate real mutations of virus genome.
    # So here, there are mutational probabilities, which will bring an 
    # stochastic scenario sorting the progenies by the classes.
    
    UpParticles = 0
    DownParticles = 0 
    
    if(Cy > 0):
        for particle in Matrix[g][p][Cy]:
            # In this loop, for each particle a random number is selected.
            # Here a random (float) number greater than zero and less than one is selected.
            RandomNumber = random.random()
            
            # If the random number is less than the DeleteriousProbability 
            # defined, one particle of the previous Cycle will 
            # decrease one Class number. Remember this function is 
            # inside a loop for each Cy and each Cl values.
            # So this loop will run through the whole Matrix, 
            # particle by particle on its own positions.
            
            if RandomNumber < DeleteriousProbability[Cy]:
                # Deleterious Mutation = 90,0% probability (0.9)
                particle.DemoteClass()
                DownParticles += 1
                
            elif (RandomNumber < (DeleteriousProbability[Cy] + BeneficialProbability[Cy])):
                # Beneficial Mutation = 0,5% probability (0.005)
                particle.RaiseClass()
                UpParticles += 1

    ClassUpParticles[g][p][Cy] = UpParticles
    ClassDownParticles[g][p][Cy] = DownParticles


def CutOffMaxParticlesPerCycle(Matrix, g, p, Cy):
    
    if(len(Matrix[g][p][Cy]) > MaxParticles):
    
        rndParticles = random.sample(Matrix[g][p][Cy], MaxParticles)
        
        Matrix[g][p][Cy].clear()
    
        Matrix[g][p][Cy] = rndParticles

#@jit
def PickRandomParticlesForInfection(Matrix, g, p, Cy):
    
    NoParticlesForInfection = False
    
    ParticlesInThisCycle = len(Matrix[g][p][Cy])
    
    # TODO remove selected infection particles from the Matrix, or 
    # copy the same particle, to keep the id
    
    if (ParticlesInThisCycle > 0):
        if(ParticlesInThisCycle >= InfectionParticles):
            InfectedParticles = random.sample(Matrix[g][p][Cy], InfectionParticles)
        else:
            InfectedParticles = random.sample(Matrix[g][p][Cy], ParticlesInThisCycle)
        
    else:
        NoParticlesForInfection = True
    
    # if there are no particles for infection, there is no infection
    if (NoParticlesForInfection):
        print("Patient " + str(p) + " Cycle " + str(Cy) + " has no particles.")
        OutputFile.write("Patient " + str(p) + " Cycle " + str(Cy) + " has no particles.") 
        
    else:
        InfectPatients(Matrix, InfectedParticles, g, p, Cy)
    
def InfectPatients(Matrix, InfectedParticles, g, p, Cy):
    
    global LastRowAvailable
    
    PatientsToInfect = [0] * Gen1Patients
    
    # each patient will infect a group of patients of size Gen1Patients
    LastPatient = ((p + 1) * Gen1Patients) - 1; # the last patient of this group
    FirstPatient = LastPatient - (Gen1Patients - 1); # the first patient of this group
    
    for x in range(Gen1Patients):
        PatientsToInfect[x] = FirstPatient + x
        #print(PatientsToInfect[x]);
        
    #print(FirstPatient);
    #print(LastPatient);
    
    # looks for the first occurrence of the required patient
    # Example: Cycle 6. If InfectionCycle = [ 2, 4, 6 ], so InfectionCycle.index(Cy) = 2
    # So, patient = PatientsToInfect[2]
    patient = PatientsToInfect[InfectionCycle.index(Cy)]
    
    for particle in InfectedParticles:
        # creates 1 new particle, on a patient in the next generation
        # in cycle 0. The new particle will be of the same class of the
        # one that infected the patient
        Matrix[g + 1][patient][0].append(ParticleClass.Particle(particle.R))
        
    print("G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy))
    OutputFile.write("G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy) + "\n") 
    
    worksheet.write(LastRowAvailable, 0, "G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy))
    LastRowAvailable += 1

def PrintOutput(Matrix):
    
    global LastRowAvailable
    
    PercentageOfParticlesUp = 0.0
    PercentageOfParticlesDown = 0.0
    
    # Formatting Output for the Console screen. 
    print("\n \t\t\tR0\tR1\tR2\tR3\tR4\tR5\tR6\tR7\tR8\tR9\tR10 ")
    
    OutputFile.write("\t\t\tR0\tR1\tR2\tR3\tR4\tR5\tR6\tR7\tR8\tR9\tR10 \n") 
    
    LastRowAvailable += 1
    
    for R in range(Classes):
        # fill a line in the Excel file with R0, R1, R2 .... R10
        worksheet.write(LastRowAvailable, R + 2, "R" + str(R), HorizAlign)
        
    # worksheet.write(Row, Column, String, format)
    worksheet.write(LastRowAvailable, 13, "Cycle", HorizAlign)
    worksheet.write(LastRowAvailable, 14, "Cycle Particles", HorizAlign)
    worksheet.write(LastRowAvailable, 15, "Particles Up", HorizAlign)
    worksheet.write(LastRowAvailable, 16, "Particles Up - %", HorizAlign)
    worksheet.write(LastRowAvailable, 17, "Particles Down", HorizAlign)
    worksheet.write(LastRowAvailable, 18, "Particles Down - %", HorizAlign)
        
    LastRowAvailable += 1
    worksheet.freeze_panes(LastRowAvailable, 0)

    for g in range(Generations):
        for p in range(pow(Gen1Patients, g)):
            for Cy in range(Cycles):
                
                Line = "G " + str(g) + " P " + str(p) + " Cycle " + str(Cy) + "\t\t"
                
                ClassCount = [0] * Classes # R Classes from 0 to 10
                
                for particle in Matrix[g][p][Cy]:
                    ClassCount[particle.R] += 1 # R Class 10 actually goes to array position 11
                
                for Cl in range(Classes):
                    Line += str(ClassCount[Cl]) + "\t"
                
                if(len(Matrix[g][p][Cy]) > 0):
                    PercentageOfParticlesUp = (ClassUpParticles[g][p][Cy] / len(Matrix[g][p][Cy]))
                    PercentageOfParticlesDown = (ClassDownParticles[g][p][Cy] / len(Matrix[g][p][Cy]))
                else:
                    PercentageOfParticlesUp = 0.0
                    PercentageOfParticlesDown = 0.0
                
                if(Cy == 0):
                    worksheet.write(LastRowAvailable, 0, "Generation")
                    worksheet.write(LastRowAvailable, 1, g, HorizAlign)
                    worksheet.write(LastRowAvailable + 1, 0, "Patient")
                    worksheet.write(LastRowAvailable + 1, 1, p, HorizAlign)
                
                for R in range(Classes):
                    # fill a line in the Excel file with number of particles from R0, R1, R2 .... R10
                    worksheet.write(LastRowAvailable, R + 2, ClassCount[R], HorizAlign)
                    
                worksheet.write(LastRowAvailable, 13, Cy, HorizAlign)
                worksheet.write(LastRowAvailable, 14, len(Matrix[g][p][Cy]), HorizAlign)
                worksheet.write(LastRowAvailable, 15, ClassUpParticles[g][p][Cy], HorizAlign)
                worksheet.write(LastRowAvailable, 16, PercentageOfParticlesUp, HorizAlign)
                worksheet.write(LastRowAvailable, 17, ClassDownParticles[g][p][Cy], HorizAlign)
                worksheet.write(LastRowAvailable, 18, PercentageOfParticlesDown, HorizAlign)
                    
                LastRowAvailable += 1
                
#                print(Line)
#                print("\nSoma do ciclo " + str(Cy) + ": " + str(len(Matrix[g][p][Cy])))
#                print("Particles Up: " + str(ClassUpParticles[g][p][Cy]) + " - " + str(PercentageOfParticlesUp))
#                print("Particles Down: " + str(ClassDownParticles[g][p][Cy]) + " - " + str(PercentageOfParticlesDown))
#                print("******************************************************")
            
                OutputFile.write(Line)
                OutputFile.write("\nSoma do ciclo " + str(Cy) + ": " + str(len(Matrix[g][p][Cy])))
                OutputFile.write("\nParticles Up: " + str(ClassUpParticles[g][p][Cy]) + " - " + str(PercentageOfParticlesUp))
                OutputFile.write("\nParticles Down: " + str(ClassDownParticles[g][p][Cy]) + " - " + str(PercentageOfParticlesDown))
                OutputFile.write("\n****************************************************** \n")
        
#                plt.plot(ClassCount, label = 'Cycle ' + str(Cy))
#                plt.bar(range(Classes), ClassCount, label = 'Cycle ' + str(Cy))
#                plt.xlabel('R Classes')
#                plt.ylabel('Number of Particles')
#                plt.title("Generation " + str(g) + " - Patient " + str(p))
#                plt.grid(True)
#                
#                plt.xticks(np.arange(0, 11, step = 1))
#                plt.yticks(np.arange(0, 1000, step = 100))
            
#                plt.legend(bbox_to_anchor = (1.05, 1), loc = 'upper left')
#    
#                plt.savefig('Gen' + str(g) + 'Patient' + str(p) + 'Cycle' + str(Cy) + '.png', dpi = 200, bbox_inches = 'tight')
#            
#                plt.show()
                
            LastRowAvailable += 1
        
main()

# TODO fazer gráficos com frequência relativa: porcentagem de partículas em cada classe
# TODO identificar R máximo recebido na infecção e gerar gráfico boxplot (Fig.14 pré-dissertação).
# TODO gerar valor de mi (u). Sendo u = número de partículas que um ciclo pode gerar para o próximo (Fig13 pré-dissertação).
# TODO Colocar opção de infectar paciente sempre com partículas das classes mais altas.
# TODO sortear o ciclo em que ocorre a infecção.  
# TODO atribuir probabilidades para faixas de valores de ciclos de transmissão. 
