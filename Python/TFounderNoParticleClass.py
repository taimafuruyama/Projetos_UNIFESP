import platform
import random
from datetime import datetime
#import matplotlib.pyplot as plt
import xlsxwriter

# Number of Generations
# Generation 0 always have only 1 patient
# Generations 1 and forward have the number of patients defined in the GEN1PATIENTS variable
Generations = 9

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

# array of strings to store when infection occurs, so that it can be written to output
InfectionWarnings = []

InfectionUserDefined = True

# this array is called inside the RunSimulation function
NumberOfInfectionCycles = 4

# 0-10 - 50%
# 11-20 - 25%
# 21-30 - 15%
# 31-50 - 10%
DrawIntervals = {10: 50, 20: 25, 30: 15, 50: 10}
DrawIntervalsKeys = list(DrawIntervals.keys())

InfectionCycle = {}

CyclesForDrawing = [] # an array with CYCLES number of values, from 0 to CYCLES
DrawingWeights = [] # an array with CYCLES number of values, each one is a weight for the respective cycle
DrawnCycles = [] # an array the size of NumberOfInfectionCycles

# Max particles per cycle	
MaxParticles = 1000000

DeleteriousProbability = [0] * Cycles
BeneficialProbability = [0] * Cycles

# if TRUE, beneficial probability will increase by INCREMENT each cycle
# if FALSE, it will change from a fixed value to another fixed value, at the chosen cycle
BeneficialIncrement = False

FirstBeneficial = 0.0003
SecondBeneficial = 0.0008

# if TRUE, deleterious probability will increase by INCREMENT each cycle
# if FALSE, it will change from a fixed value to another fixed value, at the chosen cycle
DeleteriousIncrement = False

FirstDeleterious = 0.3
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
worksheet.set_column(2, 2, 5)
worksheet.set_column(14, 14, 12)
worksheet.set_column(15, 15, 10)
worksheet.set_column(16, 16, 13)
worksheet.set_column(17, 17, 13)
worksheet.set_column(18, 18, 16)

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
    
    global LastRowAvailable
    
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
        Matrix[0][0][0].append(ClassOfInitialParticles)
      
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
    LastRowAvailable += 2
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
    
    global LastPatient, worksheet, LastRowAvailable
    
    # Populates the CyclesForDrawing array with number of cycles
    for i in range(Cycles):
        CyclesForDrawing.append(i)
    
#    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    
    # print("RunSimulation function started: " + str(datetime.now()) + "\n")
    
    # Main Loop to create more particles on the next Cycles from the Cycle Zero.
    # Each matrix position will bring a value. This value will be mutiplied by its own class number. 
    for g in range(Generations):
        for p in range(pow(Gen1Patients, g)): # pow(Gen1Patients, g) gives the generation size
            
            print("Patient started: GEN " + str(g) + " - P " + str(p))
            OutputFile.write("Patient started: GEN " + str(g) + " - P " + str(p) + "\n")
            worksheet.write(LastRowAvailable + 1, 0, "Patient started: GEN " + str(g) + " - P " + str(p))
            LastRowAvailable += 1
            
            RunPatient(g, p) 
            Matrix[g][p].clear()
            LastPatient = 0
            DrawingWeights.clear()
            InfectionWarnings.clear()
            
            if LastRowAvailable >= 100:
                worksheet = workbook.add_worksheet()
                worksheet.set_column(0, 0, 20)
                worksheet.set_column(14, 14, 12)
                worksheet.set_column(15, 15, 10)
                worksheet.set_column(16, 16, 13)
                worksheet.set_column(17, 17, 13)
                worksheet.set_column(18, 18, 16)

                LastRowAvailable = 0
            
        LastPatient = -1
            
#        pool.map(RunPatient, [(g, 0), (g, 1), (g, 2), (g, 3)])    
     
def RunPatient(g, p):
    
    if InfectionUserDefined:
        InfectionCycle = {1: 4, 2: 4, 3: 4, 4: 4}
        
    else:
        for i in range(Cycles):
            if i <= DrawIntervalsKeys[0]:
                DrawingWeights.append(DrawIntervals[10])
            elif i > DrawIntervalsKeys[0] and i <= DrawIntervalsKeys[1]:
                DrawingWeights.append(DrawIntervals[20])
            elif i > DrawIntervalsKeys[1] and i <= DrawIntervalsKeys[2]:
                DrawingWeights.append(DrawIntervals[30])
            else:
                DrawingWeights.append(DrawIntervals[50])
                
#        print(DrawingWeights)
            
        DrawnCycles = random.choices(CyclesForDrawing, DrawingWeights, k = NumberOfInfectionCycles)
        
        for i in range(1, NumberOfInfectionCycles + 1):
            InfectionCycle[i] = DrawnCycles[i - 1]
    
    for Cy in range(Cycles):
        
#        print(Cy)
                
        if(Cy > 0):
            Matrix[g][p].append([]) # adds 1 cycle
            
            ClassUpParticles[g][p].append([]) # adds 1 cycle
            ClassDownParticles[g][p].append([]) # adds 1 cycle
            
            for particle in Matrix[g][p][Cy - 1]: # takes 1 particle from previous cycle
                for i in range(particle): # creates N new particles, based on the R class
                    Matrix[g][p][Cy].append(particle)
                        
        CutOffMaxParticlesPerCycle(g, p, Cy)
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
    
    i = 0
    
    if(Cy > 0):
        while i < len(Matrix[g][p][Cy]):
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
                if Matrix[g][p][Cy][i] > 0:
                    Matrix[g][p][Cy][i] -= 1
                    
                else:
                    Matrix[g][p][Cy][i].pop(i)
                    
                DownParticles += 1
                
            elif (RandomNumber < (DeleteriousProbability[Cy] + BeneficialProbability[Cy])):
                # Beneficial Mutation = 0,5% probability (0.005)
                if Matrix[g][p][Cy][i] < 10:
                    Matrix[g][p][Cy][i] += 1
                    
                UpParticles += 1
                
            i += 1

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
        text = "G" + str(g) + " " + "P" + str(p) + " Cycle " + str(Cy) + " has no particles."
        InfectionWarnings.append(text)
        
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
        Matrix[g + 1][patient][0].append(particle)
        
    print("G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy))
    OutputFile.write("G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy) + "\n") 
    
    text = "G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy)
    InfectionWarnings.append(text)
#    worksheet.write(LastRowAvailable, 0, "G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy))
#    LastRowAvailable += 1

def SaveData(g, p, Cy):
    global LastRowAvailable, LastPatient
    
    Mi = 0
    
    PercentageOfParticlesUp = 0.0
    PercentageOfParticlesDown = 0.0
    
    LastRowAvailable += 1
    
    if LastPatient != p:
    
        for R in range(Classes):
            # fill a line in the Excel file with R0, R1, R2 .... R10
            worksheet.write(LastRowAvailable, R + 3, "R" + str(R), HorizAlign)
            
        worksheet.write(LastRowAvailable, 2, "Cycle", HorizAlign)
        worksheet.write(LastRowAvailable, 14, "Cycle Particles", HorizAlign)
        worksheet.write(LastRowAvailable, 15, "Mi", HorizAlign)
        
        
        worksheet.write(LastRowAvailable, 16, "Particles Up", HorizAlign)
        worksheet.write(LastRowAvailable, 17, "Particles Up - %", HorizAlign)
        worksheet.write(LastRowAvailable, 18, "Particles Down", HorizAlign)
        worksheet.write(LastRowAvailable, 19, "Particles Down - %", HorizAlign)

        LastRowAvailable += 1
           
    ClassCount = [0] * (Classes + 1) # We want ClassCount to be an array of 11 positions, from 0 to 10, not 0 to 9
    
    for particle in Matrix[g][p][Cy]:
        try:
            ClassCount[particle] += 1
        except:
            print("Error: " + str(particle))
    
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
        
        MaxR = GetMaxR(ClassCount)
        worksheet.write(LastRowAvailable + 2, 0, "Max R at Cycle 0")
        worksheet.write(LastRowAvailable + 2, 1, MaxR, HorizAlign)
    
    for R in range(Classes):
        # fill a line in the Excel file with number of particles from R0, R1, R2 .... R10
        worksheet.write(LastRowAvailable, R + 3, ClassCount[R], HorizAlign)
        
    worksheet.write(LastRowAvailable, 2, Cy, HorizAlign)
    worksheet.write(LastRowAvailable, 14, len(Matrix[g][p][Cy]), HorizAlign)
    
    Mi = GetMi(ClassCount, len(Matrix[g][p][Cy]))
    worksheet.write(LastRowAvailable, 15, Mi, HorizAlign)
        
    worksheet.write(LastRowAvailable, 16, ClassUpParticles[g][p][Cy], HorizAlign)
    worksheet.write(LastRowAvailable, 17, PercentageOfParticlesUp, HorizAlign)
    worksheet.write(LastRowAvailable, 18, ClassDownParticles[g][p][Cy], HorizAlign)
    worksheet.write(LastRowAvailable, 19, PercentageOfParticlesDown, HorizAlign)
        
#    LastRowAvailable += 1
    
    if Cy == Cycles - 1:
        for i in range(len(InfectionWarnings)):
            worksheet.write((LastRowAvailable - Cycles) + 5 + i, 0, InfectionWarnings[i])
    
    LastPatient = p
    
def GetMi(ClassCount, CycleParticles):
    
    # ClassCount = number of particles per cycle, in a 11 position array
    
    MaxPotentialParticles = 0
    
    for R in range(Classes):
        MaxPotentialParticles += ClassCount[R] * R
    
    if CycleParticles != 0:
        Mi = MaxPotentialParticles/CycleParticles
    else:
        Mi = 0
    
    return Mi
    
def GetMaxR(ClassCount):
    
    # ClassCount = number of particles per cycle, in a 11 position array
    
    MaxR = 0
    
    for R in range(Classes):
         if ClassCount[R] > 0:
             MaxR = R
             
    return MaxR
            
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
# TODO gerar gráfico boxplot com R Max (Fig.14 pré-dissertação).
# TODO Colocar opção de infectar paciente sempre com partículas das classes mais altas.
# TODO fazer um resumo de dados informando qual foi o paciente máximo com partículas virais dentro dele e qual o total de pacientes popssíveis.