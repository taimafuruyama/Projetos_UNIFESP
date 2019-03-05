# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 16:31:46 2019

@author: Marcos
"""

import os
import xlsxwriter
import xlrd

def main():
    
    ExcelFileName = "Data.xlsx"
    workbook = xlsxwriter.Workbook(ExcelFileName)
    worksheet = workbook.add_worksheet()
    HorizAlign = workbook.add_format()
    HorizAlign.set_align('center')
    LastRowAvailable = 0
    
#    directory = r"E:\Taima\Mestrado\Python\Simulacoes\TestesEstatisticos\R5Cycle5\TFounderSim01-03-2019_15-59-55.xlsx"
    
#    print(sh.cell_value(rowx = 20, colx = 7))
#    
#    print(sh.cell_value(rowx = 20, colx = 14))
    
#    SourceFile = xlrd.open_workbook(directory)
#    sh = SourceFile.sheet_by_index(0)
    
    for root, dirs, files in os.walk('E:\Taima\Mestrado\Python\Simulacoes\TestesEstatisticos\R5Cycle5'):
        SourceFiles = [ _ for _ in files if _.endswith('.xlsx') ]
        
        for xlsfile in SourceFiles:
            SourceFile = xlrd.open_workbook(os.path.join(root,xlsfile))
            SourceSheet = SourceFile.sheet_by_index(0)

            RParticles = SourceSheet.cell_value(rowx = 23, colx = 6)
            CycleTotal = SourceSheet.cell_value(rowx = 23, colx = 14)
        
            worksheet.write(LastRowAvailable, 0, RParticles)
            worksheet.write(LastRowAvailable, 1, CycleTotal)
            LastRowAvailable += 1
        
    workbook.close()
    
#    for row in range(sh.nrows):
#        print(sh.row(row))
    
#    print("Worksheet name(s): {0}".format(book.sheet_names()))
    
if __name__ == '__main__':
    main()
