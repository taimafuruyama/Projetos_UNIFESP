# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 16:31:46 2019
@author: Marcos
"""

import os
import xlsxwriter
import xlrd
import statistics

Cycles = 10
Classes = 11

def main():
    
    ExcelFileName = "Data.xlsx"
    workbook = xlsxwriter.Workbook(ExcelFileName)
    worksheet = workbook.add_worksheet()
    HorizAlign = workbook.add_format()
    HorizAlign.set_align('center')
    LastRowAvailable = 0
    
    worksheet.write(LastRowAvailable, 0, "Cycle")
    worksheet.write(LastRowAvailable, 1, "Stats")
    
    for Class in range(Classes):
        worksheet.write(LastRowAvailable, 2 + Class, "R" + str(Class))
    
    LastRowAvailable += 1
    
    for root, dirs, files in os.walk('C:\Taima_Furuyama\Mestrado_UNIFESP\Programacao\Python\Simulacoes\TestesEstatisticos\SemCutOff_100Cycles'):
        SourceFiles = [ _ for _ in files if _.endswith('.xlsx') ]
        
        NumberOfFiles = len(SourceFiles)
        print(NumberOfFiles)
        
        PercentArray = [[[None for i in range(NumberOfFiles)] for x in range(Classes)] for y in range(Cycles)]
        
        for xlsfile in SourceFiles:
            SourceFile = xlrd.open_workbook(os.path.join(root,xlsfile))
            SourceSheet = SourceFile.sheet_by_index(0) 
            
            for Cycle in range(Cycles): #Ciclos                
                for Class in range(Classes): #Classes R   
                    RParticles = SourceSheet.cell_value(rowx = Cycle + 15, colx = Class + 2)
                    CycleTotal = SourceSheet.cell_value(rowx = Cycle + 15, colx = 14)
                                    
                    Percent = (RParticles/CycleTotal)*100
                    
                    PercentArray[Cycle][Class].pop(0)
                    PercentArray[Cycle][Class].append(Percent)
        
#        print(PercentArray[9][10][0])
#        print(len(PercentArray[9][10]))
                    
        MeanArray = [[None for x in range(Classes)] for y in range(Cycles)]
        MedianArray = [[None for x in range(Classes)] for y in range(Cycles)]
        StdDevArray = [[None for x in range(Classes)] for y in range(Cycles)]
        MinArray = [[None for x in range(Classes)] for y in range(Cycles)]
        MaxArray = [[None for x in range(Classes)] for y in range(Cycles)]
        
#        print(MeanArray)
            
    # these 2 FOR LOOPS calculate the statistical parameters
    for Cycle in range(Cycles):
        for Class in range(Classes):
            MeanArray[Cycle].pop(0)
            Mean = statistics.mean(PercentArray[Cycle][Class])
            MeanArray[Cycle].append(Mean)
            
            MedianArray[Cycle].pop(0)
            Median = statistics.median(PercentArray[Cycle][Class])
            MedianArray[Cycle].append(Median)
            
            StdDevArray[Cycle].pop(0)
            StdDev = statistics.pstdev(PercentArray[Cycle][Class])
            StdDevArray[Cycle].append(StdDev)
            
            MinArray[Cycle].pop(0)
            Min = min(PercentArray[Cycle][Class])
            MinArray[Cycle].append(Min)
            
            MaxArray[Cycle].pop(0)
            Max = max(PercentArray[Cycle][Class])
            MaxArray[Cycle].append(Max)
                
#    print(MeanArray)
#    print(MedianArray)
#    print(StdDevArray)
#    print(MinArray)
#    print(MaxArray)
                
    # these 2 FOR LOOPS write the data to a Excel file
    for Cycle in range(Cycles):
        worksheet.write(LastRowAvailable, 0, Cycle)
        
        for Class in range(Classes):
            worksheet.write(LastRowAvailable, 1, "Mean")
            worksheet.write(LastRowAvailable + 1, 1, "Median")
            worksheet.write(LastRowAvailable + 2, 1, "StdDev")
            worksheet.write(LastRowAvailable + 3, 1, "Min")
            worksheet.write(LastRowAvailable + 4, 1, "Max")
            
            worksheet.write(LastRowAvailable, Class + 2, MeanArray[Cycle][Class])
            worksheet.write(LastRowAvailable + 1, Class + 2, MedianArray[Cycle][Class])
            worksheet.write(LastRowAvailable + 2, Class + 2, StdDevArray[Cycle][Class])
            worksheet.write(LastRowAvailable + 3, Class + 2, MinArray[Cycle][Class])
            worksheet.write(LastRowAvailable + 4, Class + 2, MaxArray[Cycle][Class])       
            
        LastRowAvailable += 5
        
    workbook.close()

#    print("Worksheet name(s): {0}".format(book.sheet_names()))
    
if __name__ == '__main__':
    main()