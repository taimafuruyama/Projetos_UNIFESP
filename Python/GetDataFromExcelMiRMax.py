# -*- coding: utf-8 -*-
"""
Created on Fri Mar  20 16:00:00 2019
@author: Marcos
"""

import os
import xlsxwriter
import xlrd
from datetime import datetime
import statistics
import numpy


"""
This script takes data from all the Excel files in a folder, and reads
only two cells from each file: the number of particles of one cell
"""

def main():
    
    ExcelFileName = "TFounderSim_SUMDATA_" + datetime.now().strftime('%d-%m-%Y_%H-%M-%S') + '.xlsx'
    workbook = xlsxwriter.Workbook(ExcelFileName)
    
    DataSheet = workbook.add_worksheet('Data')
    TransmissionSheet = workbook.add_worksheet('Transmission Cycles')
    RawRmaxSheet = workbook.add_worksheet('RawRmax')
    RawMiSheet = workbook.add_worksheet('RawMi')
    
    HorizAlign = workbook.add_format()
    HorizAlign.set_align('center')
    
    DataLastRowAvailable = 0   
    TransmissionLastRowAvailable = 0
    RawRmaxLastRowAvailable = 0
    RawMiLastRowAvailable = 0
    
    # set_column(column1, column2, size)
    TransmissionSheet.set_column(0, 0, 9)
    TransmissionSheet.merge_range(0, 0, 1, 0, 'Patient') # 1st row, 1st col, last row, last col, content
    TransmissionSheet.write(TransmissionLastRowAvailable, 4, "Transmission Cycle")
    TransmissionLastRowAvailable += 2

    RawRmaxSheet.set_column(0, 0, 9)
    RawRmaxSheet.merge_range(0, 0, 1, 0, 'Patient') # 1st row, 1st col, last row, last col, content
    RawRmaxSheet.write(TransmissionLastRowAvailable, 4, "Rmax")
    RawRmaxLastRowAvailable += 2

    RawMiSheet.set_column(0, 0, 9)
    RawMiSheet.merge_range(0, 0, 1, 0, 'Patient') # 1st row, 1st col, last row, last col, content
    RawMiSheet.write(TransmissionLastRowAvailable, 4, "Mi")
    RawMiLastRowAvailable += 2
    
    
    for root, dirs, files in os.walk('C:\Taima_Furuyama\Mestrado_UNIFESP\Programacao\Python\Simulacoes\TestesEstatisticos\TF_InfCycleAleat_B3.8_D3.8_101Ger_Cadeia_XSim'):
        SourceFiles = [ _ for _ in files if _.endswith('.xlsx') ]
        
        # Open a file just to get the generations amount
        FirstFile = xlrd.open_workbook(os.path.join(root,SourceFiles[0]))
        FirstSheet = FirstFile.sheet_by_index(0)
        
        Generations = int(FirstSheet.cell_value(rowx = 0, colx = 1))
        
        SimulationAmount = len(SourceFiles)
        
        DataSheet.write(DataLastRowAvailable, 0, "Mean Values of " + str(SimulationAmount) + " simulations")
        DataLastRowAvailable += 1
        
        #DataSheet.set_column(linha, coluna, tamanho)
        #DataSheet.merge_range(linha, coluna, mescla linhas, mescla colunas,"Conteúdo escrito"
        DataSheet.merge_range(1, 0, 2, 0, "Generation - Patient")
        DataSheet.set_column(0, 0, 17)
        DataSheet.merge_range(1, 4, 1, 6, "RMax Cycle 0")
        DataSheet.merge_range(1, 10, 1, 12, "Mi Cycle 0")
        
        DataLastRowAvailable += 1
        
        Labels = ["Mean", "Median", "StdDev", "Min", "Max", "Var"]
        
        for i in range(1, 7):
            DataSheet.write(DataLastRowAvailable, i + 3, Labels[i - 1])
            DataSheet.write(DataLastRowAvailable, i + 9, Labels[i - 1])
            
        DataLastRowAvailable += 1
        
        Simulation = 0
        
        if SimulationAmount > 0:
            RawRmaxSheet.write(0, 4, "Rmax")
            RawMiSheet.write(0, 4, "Mi")
            
        MiArray = [[None for i in range(SimulationAmount)] for x in range(Generations)]
        RMaxArray = [[None for i in range(SimulationAmount)] for x in range(Generations)]
            
        for xlsfile in SourceFiles:
            """Saves transmission cycles for each patient into TransmissionSheet"""
            
            SourceFile = xlrd.open_workbook(os.path.join(root,xlsfile))            
            
            for i in range(Generations):
                
                SourceSheet = SourceFile.sheet_by_index(i + 1)

                """Reading data"""
    
#                GenPatient = SourceSheet.cell_value(rowx = 1, colx = 1)
                GenerationText = SourceSheet.cell_value(rowx = 1, colx = 1)
                GenerationValue = SourceSheet.cell_value(rowx = 1, colx = 2)
                PatientText = SourceSheet.cell_value(rowx = 1, colx = 3)
                PatientValue = SourceSheet.cell_value(rowx = 1, colx = 4)
                
                if i < (Generations - 1):
                    TransmissionCycle = SourceSheet.cell_value(rowx = 50, colx = 2)
#                    LastInfectedPatient = SourceSheet.cell_value(rowx = 50, colx = 3)
                    RmaxValue = SourceSheet.cell_value(rowx = 49, colx = 1)
                    MiValue = SourceSheet.cell_value(rowx = 3, colx = 13) 
                    DataSheet.write(DataLastRowAvailable + 1, 0, GenerationText)
                    DataSheet.write(DataLastRowAvailable + 1, 1, GenerationValue)
                    DataSheet.write(DataLastRowAvailable + 1, 2, PatientText)
                    DataSheet.write(DataLastRowAvailable + 1, 3, PatientValue)

                else:
                    # Last patient doesn't have row 55
                    TransmissionCycle = 0
#                    DataSheet.write(DataLastRowAvailable + 1, 0, GenerationText)
                    DataSheet.write(DataLastRowAvailable + 1, 1, GenerationValue)
#                    DataSheet.write(DataLastRowAvailable + 1, 2, PatientText)
#                    DataSheet.write(DataLastRowAvailable + 1, 3, PatientValue)
#                    LastInfectedPatient = SourceSheet.cell_value(rowx = 50, colx = 3)
#                    RmaxValue = SourceSheet.cell_value(rowx = 49, colx = 1)
#                    MiValue = SourceSheet.cell_value(rowx = 3, colx = 13)
                
                Mi = SourceSheet.cell_value(rowx = 3, colx = 13)
                MiArray[i].pop(0)
                MiArray[i].append(Mi)
                
                RMax = SourceSheet.cell_value(rowx = 49, colx = 1)            
                RMaxArray[i].pop(0)
                RMaxArray[i].append(RMax)
                
                """Writing Transmission data"""
            
                TransmissionSheet.write(1, Simulation + 4, "Simulation " + str(Simulation))
                TransmissionSheet.set_column(Simulation + 1, Simulation + 1, 10) # set_column(column1, column2, size)
                TransmissionSheet.write(TransmissionLastRowAvailable, 0, GenerationText)
                TransmissionSheet.write(TransmissionLastRowAvailable, 1, GenerationValue)
                TransmissionSheet.write(TransmissionLastRowAvailable, 2, PatientText)
                TransmissionSheet.write(TransmissionLastRowAvailable, 3, PatientValue)
                TransmissionSheet.write(TransmissionLastRowAvailable, Simulation + 4, TransmissionCycle)
                TransmissionLastRowAvailable += 1

                RawRmaxSheet.write(1, Simulation + 4, "Simulation " + str(Simulation))
                RawRmaxSheet.set_column(Simulation + 1, Simulation + 1, 10) # set_column(column1, column2, size)
                RawRmaxSheet.write(RawRmaxLastRowAvailable, 0, GenerationText)
                RawRmaxSheet.write(RawRmaxLastRowAvailable, 1, GenerationValue)
                RawRmaxSheet.write(RawRmaxLastRowAvailable, 2, PatientText)
                RawRmaxSheet.write(RawRmaxLastRowAvailable, 3, PatientValue)
                RawRmaxSheet.write(RawRmaxLastRowAvailable, Simulation + 4, RmaxValue)
                RawRmaxLastRowAvailable += 1
                
                RawMiSheet.write(1, Simulation + 4, "Simulation " + str(Simulation))
                RawMiSheet.set_column(Simulation + 1, Simulation + 1, 10) # set_column(column1, column2, size)
                RawMiSheet.write(RawMiLastRowAvailable, 0, GenerationText)
                RawMiSheet.write(RawMiLastRowAvailable, 1, GenerationValue)
                RawMiSheet.write(RawMiLastRowAvailable, 2, PatientText)
                RawMiSheet.write(RawMiLastRowAvailable, 3, PatientValue)
                RawMiSheet.write(RawMiLastRowAvailable, Simulation + 4, MiValue)
                RawMiLastRowAvailable += 1
                
                """Writing only patient number on DataSheet
                Mi and RMax are going to be written later"""
                
                DataLastRowAvailable += 1
                
            Simulation +=1
            DataLastRowAvailable = 2            
            TransmissionLastRowAvailable = 2
            RawRmaxLastRowAvailable = 2
            RawMiLastRowAvailable = 2
            
        DataLastRowAvailable = 3
            
        MiMeanArray = [None for x in range(Generations)]
        MiMedianArray = [None for x in range(Generations)]
        MiStdDevArray = [None for x in range(Generations)]
        MiMinArray = [None for x in range(Generations)]
        MiMaxArray = [None for x in range(Generations)]
        MiVarArray = [None for x in range(Generations)]
        
        RMaxMeanArray = [None for x in range(Generations)]
        RMaxMedianArray = [None for x in range(Generations)]
        RMaxStdDevArray = [None for x in range(Generations)]
        RMaxMinArray = [None for x in range(Generations)]
        RMaxMaxArray = [None for x in range(Generations)]
        RMaxVarArray = [None for x in range(Generations)]
        
#        print(MiMeanArray.pop(0))
            
        for Gen in range(Generations):
            """calculate the statistical parameters"""
            
            MiMeanArray.pop(0)
            Mean = statistics.mean(MiArray[Gen])
            MiMeanArray.append(Mean)
            
            MiMedianArray.pop(0)
            Median = statistics.median(MiArray[Gen])
            MiMedianArray.append(Median)
            
            MiStdDevArray.pop(0)
            StdDev = statistics.pstdev(MiArray[Gen])
            MiStdDevArray.append(StdDev)
            
            MiMinArray.pop(0)
            Min = min(MiArray[Gen])
            MiMinArray.append(Min)
            
            MiMaxArray.pop(0)
            Max = max(MiArray[Gen])
            MiMaxArray.append(Max)
            
            MiVarArray.pop(0)
            Var = statistics.pvariance(MiArray[Gen])
            MiVarArray.append(Var)
            
            RMaxMeanArray.pop(0)
            Mean = statistics.mean(RMaxArray[Gen])
            RMaxMeanArray.append(Mean)
            
            RMaxMedianArray.pop(0)
            Median = statistics.median(RMaxArray[Gen])
            RMaxMedianArray.append(Median)
            
            RMaxStdDevArray.pop(0)
            StdDev = statistics.pstdev(RMaxArray[Gen])
            RMaxStdDevArray.append(StdDev)
            
            RMaxMinArray.pop(0)
            Min = min(RMaxArray[Gen])
            RMaxMinArray.append(Min)
            
            RMaxMaxArray.pop(0)
            Max = max(RMaxArray[Gen])
            RMaxMaxArray.append(Max)
            
            RMaxVarArray.pop(0)
            Var = statistics.pvariance(RMaxArray[Gen])
            RMaxVarArray.append(Var)
            
#        print(MiMedianArray)
            
        for Gen in range(Generations):
            """writes the statistical parameters"""
            
            DataSheet.write(DataLastRowAvailable, 4, RMaxMeanArray[Gen])
            DataSheet.write(DataLastRowAvailable, 5, RMaxMedianArray[Gen])
            DataSheet.write(DataLastRowAvailable, 6, RMaxStdDevArray[Gen])
            DataSheet.write(DataLastRowAvailable, 7, RMaxMinArray[Gen])
            DataSheet.write(DataLastRowAvailable, 8, RMaxMaxArray[Gen])  
            DataSheet.write(DataLastRowAvailable, 9, RMaxVarArray[Gen]) 
            
            DataSheet.write(DataLastRowAvailable, 10, MiMeanArray[Gen])
            DataSheet.write(DataLastRowAvailable, 11, MiMedianArray[Gen])
            DataSheet.write(DataLastRowAvailable, 12, MiStdDevArray[Gen])
            DataSheet.write(DataLastRowAvailable, 13, MiMinArray[Gen])
            DataSheet.write(DataLastRowAvailable, 14, MiMaxArray[Gen])  
            DataSheet.write(DataLastRowAvailable, 15, MiVarArray[Gen]) 
            
            DataLastRowAvailable += 1
        
    workbook.close()
    
if __name__ == '__main__':
    main()
