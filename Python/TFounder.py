import platform
import random
from datetime import datetime
#import matplotlib.pyplot as plt
import xlsxwriter
import ParticleClass

# Number of Generations
# Generation 0 always have only 1 patient
# Generations 1 and forward have the number of patients defined in the GEN1PATIENTS variable
Generations = 1

# this array is called inside the RunSimulation function
InfectionCycle = {1: 4, 2: 4, 3: 4, 4: 4}

# Number of Patients in Generation 1
Gen1Patients = 4

# Number of Cycles
Cycles = 100

# Number of Classes
Classes = 11

# Matrix containing all the data (generations, patients, cycles and classes)
Matrix = []

# The "InitialParticles" is the initial amount of viral particles, that is: the initial virus population of a infection.
InitialParticles = 5

ClassOfInitialParticles = 10

InfectionParticles = 5

# Max particles per cycle	
MaxParticles = 1000000
MakeCutOff = False

DeleteriousProbability = [0] * Cycles
BeneficialProbability = [0] * Cycles

# if TRUE, beneficial probability will increase by INCREMENT each cycle
# if FALSE, it will change from a fixed value to another fixed value, at the chosen cycle
BeneficialIncrement = False

FirstBeneficial = 0.0008
SecondBeneficial = 0.0008

# if TRUE, deleterious probability will increase by INCREMENT each cycle
# if FALSE, it will change from a fixed value to another fixed value, at the chosen cycle
DeleteriousIncrement = False

FirstDeleterious = 0.8
SecondDeleterious = 0.8

ChangeCycle = 8

# Lists to keep the number of particles that go up or down the classes, during mutations
# So, for example, the list ClassUpParticle[0][1, 4] will keep the number of particles
# that went up 1 class, in GENERATION 0, PATIENT 1, CYCLE 4

ClassUpParticles = []
ClassDownParticles = []

OutputFile = open('Testfile.txt', 'w') 

ExcelFileName = "TFounderSim" + datetime.now().strftime('%d-%m-%Y_%H-%M-%S') + '.xlsx'
workbook = xlsxwriter.Workbook(ExcelFileName)
worksheet = workbook.add_worksheet()
HorizAlign = workbook.add_format()
HorizAlign.set_align('center')

bold = workbook.add_format({'bold': True})
LastRowAvailable = 0
LastPatient = -1

# set_column(column1, column2, size)
worksheet.set_column(0, 0, 20)
worksheet.set_column(13, 13, 5)
worksheet.set_column(14, 14, 12)
worksheet.set_column(15, 15, 10)
worksheet.set_column(16, 16, 13)
worksheet.set_column(17, 17, 13)
worksheet.set_column(18, 18, 16)

worksheet.write(3, 5, "Cut Off Function", bold)
worksheet.write(4, 5, str(MakeCutOff), bold)

worksheet.write(LastRowAvailable, 0, "Generations", bold)
worksheet.write(LastRowAvailable, 1, Generations)
LastRowAvailable += 1
worksheet.write(LastRowAvailable, 0, "Gen1Patients", bold)
worksheet.write(LastRowAvailable, 1, Gen1Patients)
LastRowAvailable += 1
worksheet.write(LastRowAvailable, 0, "InfectionCycle", bold)
worksheet.write(LastRowAvailable, 1, str(InfectionCycle))
LastRowAvailable += 1
worksheet.write(LastRowAvailable, 0, "Cycles", bold)
worksheet.write(LastRowAvailable, 1, Cycles)
LastRowAvailable += 1
worksheet.write(LastRowAvailable, 0, "InitialParticles", bold)
worksheet.write(LastRowAvailable, 1, InitialParticles)
LastRowAvailable += 1
worksheet.write(LastRowAvailable, 0, "ClassOfInitialParticles", bold)
worksheet.write(LastRowAvailable, 1, ClassOfInitialParticles)
LastRowAvailable += 1
worksheet.write(LastRowAvailable, 0, "InfectionParticles", bold)
worksheet.write(LastRowAvailable, 1, InfectionParticles)
LastRowAvailable += 1
worksheet.write(LastRowAvailable, 0, "MaxParticles", bold)
worksheet.write(LastRowAvailable, 1, MaxParticles)
LastRowAvailable += 1
worksheet.write(LastRowAvailable, 0, "First Beneficial", bold)
worksheet.write(LastRowAvailable, 1, FirstBeneficial)
LastRowAvailable += 1
worksheet.write(LastRowAvailable, 0, "Second Beneficial", bold)
worksheet.write(LastRowAvailable, 1, SecondBeneficial)
LastRowAvailable += 1
worksheet.write(LastRowAvailable, 0, "First Deleterious", bold)
worksheet.write(LastRowAvailable, 1, FirstDeleterious)
LastRowAvailable += 1
worksheet.write(LastRowAvailable, 0, "Second Deleterious", bold)
worksheet.write(LastRowAvailable, 1, SecondDeleterious)
LastRowAvailable += 1
worksheet.write(LastRowAvailable, 0, "Change Cycle", bold)
worksheet.write(LastRowAvailable, 1, ChangeCycle)
LastRowAvailable += 1


# TODO place a TAB Summary and a TAB results in the Excel workbook 

def main():
    
    print("\nMain function started: " + str(datetime.now()) + "\n")
    startTime = datetime.now()
    
    IdentifyMachine()

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
        FillDeleteriousArrayWithIncrement(FirstDeleterious, 0.1)
        # FIRST PARAMETER: initial probability
        # SECOND PARAMENTER: increment

    else:
        FillDeleteriousArray(FirstDeleterious, SecondDeleterious, ChangeCycle)
        # FIRST PARAMETER: first probability
        # SECOND PARAMENTER: second probability
        # THIRD PARAMETER: cycle to change from first probability to second probability

    if BeneficialIncrement == True:
        FillBeneficialArrayWithIncrement(FirstBeneficial, 0.1)
        # FIRST PARAMETER: initial probability
        # SECOND PARAMENTER: increment

    else:
        FillBeneficialArray(FirstBeneficial, SecondBeneficial, ChangeCycle)
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

    RunSimulation()
    
    print("\nMain function ended: " + str(datetime.now()) + "\n")
    print("Total run time: " + str(datetime.now() - startTime) + "\n")
    print("Date: " + str(datetime.now()) + "\n")
    print("Python Implementation: " + platform.python_implementation())
    
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

 
def RunSimulation():
    
    global LastPatient
    
#    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    
    # print("RunSimulation function started: " + str(datetime.now()) + "\n")
    
    # Main Loop to create more particles on the next Cycles from the Cycle Zero.
    # Each matrix position will bring a value. This value will be mutiplied by its own class number. 
    for g in range(Generations):
        for p in range(pow(Gen1Patients, g)): # pow(Gen1Patients, g) gives the generation size
            RunPatient(g, p) 
#            SaveData(g, p, Cycles - 1)
            Matrix[g][p].clear()
            LastPatient = 0
            
#        pool.map(RunPatient, [(g, 0), (g, 1), (g, 2), (g, 3)])    
      
def RunPatient(g, p):
    
    global LastRowAvailable
    
    print("Patient started: GEN " + str(g) + " - P " + str(p))
    OutputFile.write("Patient started: GEN " + str(g) + " - P " + str(p) + "\n")
    worksheet.write(LastRowAvailable + 1, 0, "Patient started: GEN " + str(g) + " - P " + str(p))
    LastRowAvailable += 1
    
    for Cy in range(Cycles):
        
        print(Cy)
                
        if(Cy > 0):
            Matrix[g][p].append([]) # adds 1 cycle
            
            ClassUpParticles[g][p].append([]) # adds 1 cycle
            ClassDownParticles[g][p].append([]) # adds 1 cycle
            
            if MakeCutOff:
                for particle in Matrix[g][p][Cy - 1]: # takes 1 particle from previous cycle
                    for i in range(particle.R): # creates N new particles, based on the R class
                        Matrix[g][p][Cy].append(ParticleClass.Particle(particle.R))
                        
                CutOffMaxParticlesPerCycle(g, p, Cy)
                
            else:
                for i in range(len(Matrix[g][p][Cy - 1])):
                    
                    if len(Matrix[g][p][Cy]) <= MaxParticles:
                        RandomParticle = random.random()
                        RandomParticle = int(RandomParticle * len(Matrix[g][p][Cy - 1]))
    #                    print(RandomNumber, len(Matrix[g][p][Cy - 1]))
                        
                        particle = Matrix[g][p][Cy - 1][RandomParticle]
                        
                        for i in range(particle.R): # creates N new particles, based on the R class
                            Matrix[g][p][Cy].append(ParticleClass.Particle(particle.R))
                
        ApplyMutationsProbabilities(g, p, Cy)
        
        #print("Cycle " + str(Cy) + " " + str(Matrix[g][p, Cy]))

        for cycle in InfectionCycle:
            # IF the current cycle (Cy) is contained inside the INFECTIONCYCLE dictionary
		    # AND it is not the last generation, make infection
            
            # Cy == InfectionCycle[cycle] is comparing the current the cycle with
            # the value, not the key
            if  Cy == InfectionCycle[cycle] and g < (Generations - 1):
                # here we are passing cycle as the key, not the value
                PickRandomParticlesForInfection(g, p, Cy, cycle) 
                
        SaveData(g, p, Cy)
        
        if Cy > 0:
            Matrix[g][p][Cy - 1].clear()
                
        #print which Cycle was finished just to give user feedback, because it may take too long to run.
	    #print("Cycles processed: " + str(Cy));
	    #print("Patients processed: GEN " + str(g) + " - P " + str(p));
        
   # memory()
   
def CutOffMaxParticlesPerCycle(g, p, Cy):
    
    if(len(Matrix[g][p][Cy]) > MaxParticles):
    
        rndParticles = random.sample(Matrix[g][p][Cy], MaxParticles)
    
        Matrix[g][p][Cy] = rndParticles 
                              
def ApplyMutationsProbabilities(g, p, Cy):
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

def PickRandomParticlesForInfection(g, p, Cy, cycleForInfection):
    
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
        InfectPatients(InfectedParticles, g, p, Cy,cycleForInfection)
    
def InfectPatients(InfectedParticles, g, p, Cy, cycleForInfection):
    
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
    
    # Example: if INFECTIONCYCLE is {1: 8, 2: 4, 3: 6, 4: 2}
    # and cycleForInfection is 3 (3 is the key, not the value), 
    # patient = PatientsToInfect[3 - 1] = PatientsToInfect[2]
    patient = PatientsToInfect[cycleForInfection - 1]
    
    for particle in InfectedParticles:
        # creates 1 new particle, on a patient in the next generation
        # in cycle 0. The new particle will be of the same class of the
        # one that infected the patient
        Matrix[g + 1][patient][0].append(ParticleClass.Particle(particle.R))
        
    print("G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy))
    OutputFile.write("G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy) + "\n") 
    
#    worksheet.write(LastRowAvailable, 0, "G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy))
#    LastRowAvailable += 1

def SaveData(g, p, Cy):
    global LastRowAvailable, LastPatient
    
    PercentageOfParticlesUp = 0.0
    PercentageOfParticlesDown = 0.0
    
    LastRowAvailable += 1
    
    if LastPatient != p:
    
        for R in range(Classes):
            # fill a line in the Excel file with R0, R1, R2 .... R10
            worksheet.write(LastRowAvailable, R + 2, "R" + str(R), HorizAlign)
            
        worksheet.write(LastRowAvailable, 13, "Cycle", HorizAlign)
        worksheet.write(LastRowAvailable, 14, "Cycle Particles", HorizAlign)
        worksheet.write(LastRowAvailable, 15, "Particles Up", HorizAlign)
        worksheet.write(LastRowAvailable, 16, "Particles Up - %", HorizAlign)
        worksheet.write(LastRowAvailable, 17, "Particles Down", HorizAlign)
        worksheet.write(LastRowAvailable, 18, "Particles Down - %", HorizAlign)

        LastRowAvailable += 1
           
    ClassCount = [0] * Classes # R Classes from 0 to 10
    
    for particle in Matrix[g][p][Cy]:
        ClassCount[particle.R] += 1 # R Class 10 actually goes to array position 11
    
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
        
#    LastRowAvailable += 1
    
    LastPatient = p
            
def memory():
    import os
    import psutil
    process = psutil.Process(os.getpid())
    print("Memory used: " + str((process.memory_info().rss)/1048576) + " MB")   # in Megabytes 
    
def IdentifyMachine():
    
    worksheet.write(0, 5, "Python Implementation", bold)
    worksheet.write(1, 5, platform.python_implementation(), bold)

    try:
        import cpuinfo
        print("CPU: " + cpuinfo.cpu.info[0]['ProcessorNameString'])
        worksheet.write(6, 5, "CPU: " + cpuinfo.cpu.info[0]['ProcessorNameString'])
    except:
        print("No cpuinfo.py module. Download it at https://github.com/pydata/numexpr/blob/master/numexpr/cpuinfo.py")
        worksheet.write(6, 5, "No cpuinfo.py module. Download it at https://github.com/pydata/numexpr/blob/master/numexpr/cpuinfo.py")
        
    print("Processor: " + platform.processor())
    print("Architecture (32 or 64 bits): " + platform.machine())
    print("OS: " + platform.platform())
    
    worksheet.write(7, 5, "Processor: " + platform.processor())
    worksheet.write(8, 5, "Architecture (32 or 64 bits): " + platform.machine())
    worksheet.write(9, 5, "OS: " + platform.platform() + "\n")
        
main()

# TODO fazer gráficos com frequência relativa: porcentagem de partículas em cada classe
# TODO identificar R máximo recebido na infecção e gerar gráfico boxplot (Fig.14 pré-dissertação).
# TODO gerar valor de mi (u). Sendo u = número de partículas que um ciclo pode gerar para o próximo (Fig13 pré-dissertação).
# TODO Colocar opção de infectar paciente sempre com partículas das classes mais altas.
# TODO sortear o ciclo em que ocorre a infecção.  
# TODO atribuir probabilidades para faixas de valores de ciclos de transmissão. 
# TODO fazer um resumo de dados informando qual foi o paciente máximo com partículas virais dentro dele e qual o total de pacientes popssíveis.