import sys
import platform
import random
import time
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import xlsxwriter
#import numpy

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QDialog, QPushButton
from PyQt5.QtWidgets import QFileDialog, QTabWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QStatusBar, QCheckBox, QVBoxLayout, QComboBox, QSpinBox, QLineEdit
from PyQt5.QtWidgets import QGroupBox, QTableView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QSize, Qt, QAbstractTableModel

SimulationTimes = None

# Number of Generations
# Generation 0 always have only 1 patient
# Generations 1 and forward have the number of patients defined in the GEN1PATIENTS variable
Generations = None

# Number of Patients in Generation 1
Gen1Patients = None

NewWorksheetEachPatient = None

# Number of Cycles
Cycles = None

# Number of Classes
Classes = None

# Matrix containing all the data (generations, patients, cycles and classes)
Matrix = []

# The "InitialParticles" is the initial amount of viral particles, that is: the initial virus population of a infection.
InitialParticles = None

ClassOfInitialParticles = None

InfectionParticles = None

# array of strings to store when infection occurs, so that it can be written to output
InfectionWarnings = []
InfectionWarningsCycle = []

InfectionUserDefined = None
UserDefindedCycleForInfection = None

# this array is called inside the RunSimulation function
NumberOfInfectionCycles = Gen1Patients

# Example:
# {4: 10, 10: 20, 20: 30, 40: 40}
# 0 - 4 = 10%
# 5 - 10 = 20%
# 11 - 20 = 30%
# 21 - 50 = 40%
DrawIntervals = {4: 0, 13: 0, 24: 0, 42: 100}
DrawIntervalsKeys = list(DrawIntervals.keys())

InfectionCycle = {}

CyclesForDrawing = [] # an array with CYCLES number of values, from 0 to CYCLES
DrawingWeights = [] # an array with CYCLES number of values, each one is a weight for the respective cycle
DrawnCycles = [] # an array the size of NumberOfInfectionCycles

# Max particles per cycle	
MaxParticles = None

DeleteriousProbability = None
BeneficialProbability = None

# if TRUE, beneficial probability will increase by INCREMENT each cycle
# if FALSE, it will change from a fixed value to another fixed value, at the chosen cycle
BeneficialIncrement = None

FirstBeneficial = None
SecondBeneficial = None

# if TRUE, deleterious probability will increase by INCREMENT each cycle
# if FALSE, it will change from a fixed value to another fixed value, at the chosen cycle
DeleteriousIncrement = False

FirstDeleterious = None
SecondDeleterious = None

ChangeCycle = None

# Maximum R Class that a patient has at cycle 0
# it is also the maximum R Class of received infection
MaxR = 0

# Lists to keep the number of particles that go up or down the classes, during mutations
# So, for example, the list ClassUpParticle[0][1, 4] will keep the number of particles
# that went up 1 class, in GENERATION 0, PATIENT 1, CYCLE 4
ClassUpParticles = []
ClassDownParticles = []

# Excel output global variables
MaxWorksheetSize = 0
workbook = None
worksheet = None
HorizAlign = None
bold = None
LastRowAvailable = 0
LastPatient = -1

# Qt
mainWin = None
ConsoleOut = None
TableOutput = None
TableView = None

class MainWindow(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(1200, 950)) # TODO open maximized
        self.setWindowTitle("T-Founder 0.0.1") # TODO not "2" actually, change this later
            
        Menu = self.menuBar()
        
        file_menu = Menu.addMenu('File')
        open_action = QtWidgets.QAction('Open', self)
        quit_action = QtWidgets.QAction('Quit', self)
        file_menu.addAction(open_action)
        file_menu.addAction(quit_action)
        quit_action.triggered.connect(self.close)
        open_action.triggered.connect(self.OpenFiles)

        edit_menu = Menu.addMenu('Edit')
        undo_action = QtWidgets.QAction('Undo', self)
        redo_action = QtWidgets.QAction('Redo', self)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        
        help_menu = Menu.addMenu('Help')
        about_action = QtWidgets.QAction('About', self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.AboutDialog)
        
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
         
        self.gridLayout = QGridLayout(self)   
        self.setLayout(self.gridLayout)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0) # int LEFT, TOP, RIGHT, BOTTOM
        
        centralWidget.setLayout(self.gridLayout)
        
#        self.statusBar().showMessage("System Status | Normal") 
        
        self.MainTabBar = TabBar(self)
#        MainTabBar.setFixedSize(QSize(800, 800))
        self.MainTabBar.setMinimumWidth(800)
        self.gridLayout.addWidget(self.MainTabBar, 0, 1)
        
    def OpenFiles(self):
      OpenFileDialog = QFileDialog()
      OpenFileDialog.setFileMode(QFileDialog.AnyFile)
      
      filenames = [] # TODO use QStringList?

      if OpenFileDialog.exec_():
          filenames = OpenFileDialog.selectedFiles()
        
    def AboutDialog(self):
       AboutDialog = QDialog(None, QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowTitleHint)
       AboutDialog.setMinimumSize(QSize(500, 700)) 
       
       gridLayout = QGridLayout(AboutDialog)   
       AboutDialog.setLayout(gridLayout)  
       
       TitleText = "T-Founder 0.0.1"
       
       InfoText = '''(C) 2019 T-Founder'''
       
       DevelopersText = '''Developers
       
       Taimá Naomi Furuyama
       
       https://github.com/taimafuruyama/Projetos_UNIFESP'''
       
       RequirementsText = '''     
       Requirements: 
       Python version 3.6 or higher 
       PyQt5 or higher 
       
       Download the Anaconda distribution to easily get all the packages:
           
           https://www.anaconda.com/distribution/'''
       
       TitelLabel = QLabel(TitleText, AboutDialog) 
       TitelLabel.setFixedSize(QSize(500, 25))
       TitelLabel.setAlignment(QtCore.Qt.AlignCenter) 
       TitelLabel.setStyleSheet("font: bold 20px;")
       gridLayout.addWidget(TitelLabel, 0, 0)
       
       InfoLabel = QLabel(InfoText, AboutDialog) 
       InfoLabel.setFixedSize(QSize(500, 300))
       InfoLabel.setAlignment(QtCore.Qt.AlignCenter) 
       InfoLabel.setStyleSheet("text-align: justify")
       gridLayout.addWidget(InfoLabel, 1, 0)
       
       DevelopersLabel = QLabel(DevelopersText, AboutDialog) 
       DevelopersLabel.setFixedSize(QSize(500, 80))
       DevelopersLabel.setAlignment(QtCore.Qt.AlignCenter) 
       gridLayout.addWidget(DevelopersLabel, 2, 0)
       
       RequirementsLabel = QLabel(RequirementsText, AboutDialog) 
       RequirementsLabel.setFixedSize(QSize(500, 150))
       RequirementsLabel.setAlignment(QtCore.Qt.AlignCenter) 
       gridLayout.addWidget(RequirementsLabel, 3, 0)

       OkButton = QPushButton("OK",AboutDialog)
       gridLayout.addWidget(OkButton, 4, 0)
       OkButton.clicked.connect(AboutDialog.close)
       
       AboutDialog.setWindowTitle("About T-Founder")
       AboutDialog.setWindowModality(Qt.ApplicationModal)
       AboutDialog.exec_()
       
class TabBar(QWidget):
 
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
         
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        
        self.SetupTab = QWidget()
        self.PlotTab = QWidget()
        self.TableTab = QWidget()
        self.ConsoleTab = QWidget()
         
        # Add tabs
        self.tabs.addTab(self.SetupTab,"Setup")
        self.tabs.addTab(self.PlotTab ,"Plot")
        self.tabs.addTab(self.TableTab,"Table Output")
        self.tabs.addTab(self.ConsoleTab,"Console Output")
        
        """ Setup Tab"""
        
        self.SetupTab.layout = QGridLayout(self)
        self.SetupTab.setLayout(self.SetupTab.layout)
        self.SetupTab.layout.setSpacing(10)
        self.SetupTab.layout.setContentsMargins(10, 5, 10, 0) # int LEFT, TOP, RIGHT, BOTTOM   
#        self.tab1.setStyleSheet("background: lightgray")
        
        self.SimulationTimesLabel = QLabel("Simulations")
        self.SetupTab.layout.addWidget(self.SimulationTimesLabel, 0, 0)
        self.SimulationTimesField = QLineEdit("5")
        self.SetupTab.layout.addWidget(self.SimulationTimesField, 0, 1)
        
        self.GenerationsLabel = QLabel("Generations")
        self.SetupTab.layout.addWidget(self.GenerationsLabel, 1, 0)
        self.GenerationsField = QLineEdit("1")
        self.SetupTab.layout.addWidget(self.GenerationsField, 1, 1)
        
        self.Gen1PatientsLabel = QLabel("Patients at Generation 1")
        self.SetupTab.layout.addWidget(self.Gen1PatientsLabel, 2, 0)
        self.Gen1PatientsField = QLineEdit("1")
        self.SetupTab.layout.addWidget(self.Gen1PatientsField, 2, 1)
        
        self.Gen1PatientsField.textChanged.connect(self.Gen1PatientsChanged)
        
        self.CyclesLabel = QLabel("Cycles")
        self.SetupTab.layout.addWidget(self.CyclesLabel, 3, 0)
        self.CyclesField = QLineEdit("10")
        self.SetupTab.layout.addWidget(self.CyclesField, 3, 1)
        
        self.ClassesLabel = QLabel("Classes")
        self.SetupTab.layout.addWidget(self.ClassesLabel, 4, 0)
        self.ClassesField = QLineEdit("11")
        self.SetupTab.layout.addWidget(self.ClassesField, 4, 1)
        
        self.InitialParticlesLabel = QLabel("Initial Particles")
        self.SetupTab.layout.addWidget(self.InitialParticlesLabel, 5, 0)
        self.InitialParticlesField = QLineEdit("5")
        self.SetupTab.layout.addWidget(self.InitialParticlesField, 5, 1)
        
        self.ClassOfInitialParticlesLabel = QLabel("Class Of Initial Particles")
        self.SetupTab.layout.addWidget(self.ClassOfInitialParticlesLabel, 6, 0)
        self.ClassOfInitialParticlesField = QLineEdit("10")
        self.SetupTab.layout.addWidget(self.ClassOfInitialParticlesField, 6, 1)
        
        self.InfectionParticlesLabel = QLabel("Infection Particles")
        self.SetupTab.layout.addWidget(self.InfectionParticlesLabel, 7, 0)
        self.InfectionParticlesField = QLineEdit("5")
        self.SetupTab.layout.addWidget(self.InfectionParticlesField, 7, 1)
        
        self.NumberOfInfectionCyclesLabel = QLabel("Infection Cycles")
        self.SetupTab.layout.addWidget(self.NumberOfInfectionCyclesLabel, 8, 0)
        self.NumberOfInfectionCyclesField = QLabel("1")
        self.SetupTab.layout.addWidget(self.NumberOfInfectionCyclesField, 8, 1)
        self.NumberOfInfectionCyclesField.setMaximumHeight(10)
        
        self.MaxParticlesLabel = QLabel("Max Particles Per Cycle")
        self.SetupTab.layout.addWidget(self.MaxParticlesLabel, 9, 0)
        self.MaxParticlesField = QLineEdit("10000")
        self.SetupTab.layout.addWidget(self.MaxParticlesField, 9, 1)
        
        self.BeneficialIncrementField = QCheckBox("Beneficial Increment")
        self.SetupTab.layout.addWidget(self.BeneficialIncrementField, 10, 0) 
        self.BeneficialIncrementField.setChecked(False)
        self.BeneficialIncrementField.stateChanged.connect(self.BeneficialIncrementChanged)
        
        self.FirstBeneficialLabel = QLabel("First Beneficial")
        self.SetupTab.layout.addWidget(self.FirstBeneficialLabel, 11, 0)
        self.FirstBeneficialField = QLineEdit("0.0003")
        self.SetupTab.layout.addWidget(self.FirstBeneficialField, 11, 1)
        
        self.SecondBeneficialLabel = QLabel("Second Beneficial")
        self.SetupTab.layout.addWidget(self.SecondBeneficialLabel, 12, 0)
        self.SecondBeneficialField = QLineEdit("0.0008")
        self.SetupTab.layout.addWidget(self.SecondBeneficialField, 12, 1)
        self.SecondBeneficialField.setReadOnly(True)
        self.SecondBeneficialField.setStyleSheet("color: gray")
        
        self.DeleteriousIncrementField = QCheckBox("Deleterious Increment")
        self.SetupTab.layout.addWidget(self.DeleteriousIncrementField, 13, 0) 
        self.DeleteriousIncrementField.setChecked(False)
        self.DeleteriousIncrementField.stateChanged.connect(self.DeleteriousIncrementChanged)
        
        self.FirstDeleteriousLabel = QLabel("First Deleterious")
        self.SetupTab.layout.addWidget(self.FirstDeleteriousLabel, 14, 0)
        self.FirstDeleteriousField = QLineEdit("0.3")
        self.SetupTab.layout.addWidget(self.FirstDeleteriousField, 14, 1)
        
        self.SecondDeleteriousLabel = QLabel("Second Deleterious")
        self.SetupTab.layout.addWidget(self.SecondDeleteriousLabel, 15, 0)
        self.SecondDeleteriousField = QLineEdit("0.8")
        self.SetupTab.layout.addWidget(self.SecondDeleteriousField, 15, 1)
        self.SecondDeleteriousField.setReadOnly(True)
        self.SecondDeleteriousField.setStyleSheet("color: gray")
        
        self.ChangeCycleLabel = QLabel("Change Cycle")
        self.SetupTab.layout.addWidget(self.ChangeCycleLabel, 16, 0)
        self.ChangeCycleField = QLineEdit("8")
        self.SetupTab.layout.addWidget(self.ChangeCycleField, 16, 1)
        
        self.InfectionUserDefinedField = QCheckBox("Infection Cycles User Defined")
        self.SetupTab.layout.addWidget(self.InfectionUserDefinedField, 17, 0) 
        self.InfectionUserDefinedField.setChecked(False)
        self.InfectionUserDefinedField.stateChanged.connect(self.InfectionUserDefinedChanged)
        
        self.UserDefindedCycleForInfectionLabel = QLabel("User Defined Cycle For Infection")
        self.SetupTab.layout.addWidget(self.UserDefindedCycleForInfectionLabel, 18, 0)
        self.UserDefindedCycleForInfectionField = QLineEdit("4")
        self.SetupTab.layout.addWidget(self.UserDefindedCycleForInfectionField, 18, 1)
        self.UserDefindedCycleForInfectionField.setReadOnly(True)
        self.UserDefindedCycleForInfectionField.setStyleSheet("color: gray")
        
        self.InfectionIntervalsGroup = QGroupBox("Infection Intervals Probabilities")
        self.SetupTab.layout.addWidget(self.InfectionIntervalsGroup, 19, 0, 2, 2)
                
        self.InfectionIntervalsGroup.layout = QGridLayout(self)
        self.InfectionIntervalsGroup.setLayout(self.InfectionIntervalsGroup.layout)      
        
        self.IntervalsLabels = []
        self.IntervalsFields = []
        self.ProbLabels = []
        self.ProbFields = []
        
        #    DrawIntervals = {4: 0, 13: 0, 24: 0, 42: 100}
        
        for i in range(4):
            if i == 0:
                Interval = 4
                p = 0
            elif i == 1:
                Interval = 13
                p = 25
            elif i == 2:
                Interval = 24
                p = 25
            else:
                Interval = 42
                p = 50
            
            self.IntervalsLabels.append(QLabel("Interval " + str(i + 1)))
            self.InfectionIntervalsGroup.layout.addWidget(self.IntervalsLabels[i], 0 + i, 0)
            
            self.IntervalsFields.append(QLineEdit(str(Interval)))
            self.InfectionIntervalsGroup.layout.addWidget(self.IntervalsFields[i], 0 + i, 1)
            
            self.ProbLabels.append(QLabel("Probability " + str(i + 1)))
            self.InfectionIntervalsGroup.layout.addWidget(self.ProbLabels[i], 0 + i, 2)
            
            self.ProbFields.append(QLineEdit(str(p)))
            self.InfectionIntervalsGroup.layout.addWidget(self.ProbFields[i], 0 + i, 3)
        
        self.NewWorksheetEachPatientField = QCheckBox("New Worksheet Each Patient")
        self.SetupTab.layout.addWidget(self.NewWorksheetEachPatientField, 0, 2) 
        self.NewWorksheetEachPatientField.setChecked(True)
        
        self.RunButton = QPushButton("Run Simulation")
        self.SetupTab.layout.addWidget(self.RunButton, 30, 0)
        
        self.RunButton.clicked.connect(Run)
        
        self.SetupTabStatusBar = QStatusBar()
        self.SetupTabStatusBar.setMaximumHeight(30)
        self.SetupTabStatusBar.setStyleSheet("background: lightgray")
        self.SetupTabStatusBar.showMessage("T-Founder Ready")
        
        # addWidget(int fromRow, int fromColumn, int rowSpan, int columnSpan)
        self.SetupTab.layout.addWidget(self.SetupTabStatusBar, 31, 0, 1, 4) 
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
        """ Plot Tab"""
        
        self.PlotTab.layout = QVBoxLayout(self)
        self.PlotTab.setLayout(self.PlotTab.layout)
        
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)

        self.PlotTab.layout.addWidget(self.canvas)
                
        """ Table Output Tab """
        
        self.TableTab.layout = QVBoxLayout(self)
        self.TableTab.setLayout(self.TableTab.layout)
        
        self.Data = QStandardItemModel(0, 10 , self)
        self.Data.setHorizontalHeaderLabels(['Cycle', 'R0', 'R1', 'R2', 'R3',
                                             'R4', 'R5', 'R6', 'R7', 'R8', 'R9',
                                             'R10', 'Cycle Particles', 'Mi',
                                             'Particles Up', 'Particles Up - %',
                                             'Particles Down', 'Particles Down - %'])
        
    
        #item = QStandardItem(str(5))
        
        '''List = []
        
        for i in range(4):
            List.append(QStandardItem(str(i)))
        
        self.Data.appendRow(List)'''
        
        #for i in range(4):
         #   self.Data.setItem(i, 0, item);
        
        self.table = QTableView(self)
        self.table.setModel(self.Data)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.TableTab.layout.addWidget(self.table)
        
        #self.table.setColumnWidth(1, 50)
        self.table.resizeColumnsToContents()
        
        #TODO Save to Excel button
        self.TableTab.SaveToExcelButton = QPushButton("Save to Excel")
        self.TableTab.layout.addWidget(self.TableTab.SaveToExcelButton)
        
        #self.TableTab.table.setItem(0,0, QTableWidgetItem("Cell (1,1)"))
        
        
        """ Console Output Tab """
        self.ConsoleTab.layout = QVBoxLayout(self)
        self.ConsoleTab.setLayout(self.ConsoleTab.layout)
        self.ConsoleTab.layout.setSpacing(0)
        self.ConsoleTab.layout.setContentsMargins(0, 0, 0, 0) # int LEFT, TOP, RIGHT, BOTTOM
        
        self.scrollArea = QtWidgets.QScrollArea(self.ConsoleTab)
        self.scrollArea.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.scrollArea.setWidgetResizable(True)
        
        widget = QWidget()
        self.scrollArea.setWidget(widget)
        self.layoutScrollArea = QVBoxLayout(widget)
        
        self.ConsoleOutput = QtWidgets.QTextEdit()
        self.ConsoleOutput.setReadOnly(True)
        self.ConsoleOutput.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        self.layoutScrollArea.addWidget(self.ConsoleOutput) 
        
        self.ConsoleTab.layout.addWidget(self.scrollArea) 
        
    def Gen1PatientsChanged(self, text):
        
        if text != "":
            if int(text) == 0:
                self.Gen1PatientsField.setText(str(1))
                text = "1"
            
            if text != "" and int(text) > 4:
                self.Gen1PatientsField.setText(str(4))
                text = "4"
        
        self.NumberOfInfectionCyclesField.setText(text)
        
    def InfectionUserDefinedChanged(self):
        if self.InfectionUserDefinedField.isChecked():
            self.UserDefindedCycleForInfectionField.setReadOnly(False)
            self.UserDefindedCycleForInfectionField.setStyleSheet("color: black")
            
            for i in range(4):   
                self.IntervalsFields[i].setReadOnly(True)
                self.IntervalsFields[i].setStyleSheet("color: gray")
                
                self.ProbFields[i].setReadOnly(True)
                self.ProbFields[i].setStyleSheet("color: gray")
                
        else:
            self.UserDefindedCycleForInfectionField.setReadOnly(True)
            self.UserDefindedCycleForInfectionField.setStyleSheet("color: gray")
            
            for i in range(4):   
                self.IntervalsFields[i].setReadOnly(False)
                self.IntervalsFields[i].setStyleSheet("color: black")
                
                self.ProbFields[i].setReadOnly(False)
                self.ProbFields[i].setStyleSheet("color: black")
            
    def BeneficialIncrementChanged(self):
        if self.BeneficialIncrementField.isChecked():
            self.SecondBeneficialField.setReadOnly(False)
            self.SecondBeneficialField.setStyleSheet("color: black")
        else:
            self.SecondBeneficialField.setReadOnly(True)
            self.SecondBeneficialField.setStyleSheet("color: gray")
            
    def DeleteriousIncrementChanged(self):
        if self.DeleteriousIncrementField.isChecked():
            self.SecondDeleteriousField.setReadOnly(False)
            self.SecondDeleteriousField.setStyleSheet("color: black")
        else:
            self.SecondDeleteriousField.setReadOnly(True)
            self.SecondDeleteriousField.setStyleSheet("color: gray")
            
def main():
    
    global ConsoleOut, mainWin, TableOutput, TableView
    
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
        
    mainWin = MainWindow()
    mainWin.show()
#    mainWin.showMaximized()
    
    ConsoleOut = mainWin.MainTabBar.ConsoleOutput
    TableOutput = mainWin.MainTabBar.Data
    TableView = mainWin.MainTabBar.table
       
    IdentifyMachine()
    
    sys.exit(app.exec_())
    
def SetupInitialParameters():
    
    global SimulationTimes, Generations, Gen1Patients, NumberOfInfectionCycles
    global Cycles, Classes, InitialParticles, ClassOfInitialParticles, InfectionParticles
    global Matrix, InfectionWarnings, InfectionWarningsCycle, InfectionCycle
    global BeneficialIncrement, DeleteriousIncrement
    global FirstBeneficial, SecondBeneficial, FirstDeleterious, SecondDeleterious
    global MaxParticles
    global CyclesForDrawing, DrawingWeights, DrawnCycles, ChangeCycle, DrawIntervals
    global DeleteriousProbability, BeneficialProbability, DrawIntervalsKeys
    global InfectionUserDefined, UserDefindedCycleForInfection
    global NewWorksheetEachPatient
    
    SimulationTimes = int(mainWin.MainTabBar.SimulationTimesField.text())
    Generations = int(mainWin.MainTabBar.GenerationsField.text())
    Gen1Patients = int(mainWin.MainTabBar.Gen1PatientsField.text())
    NumberOfInfectionCycles = int(mainWin.MainTabBar.Gen1PatientsField.text())
    
    Cycles = int(mainWin.MainTabBar.CyclesField.text())
    Classes = int(mainWin.MainTabBar.ClassesField.text())
    InitialParticles = int(mainWin.MainTabBar.InitialParticlesField.text())
    ClassOfInitialParticles = int(mainWin.MainTabBar.ClassOfInitialParticlesField.text())
    InfectionParticles = int(mainWin.MainTabBar.InfectionParticlesField.text())
    MaxParticles = int(mainWin.MainTabBar.MaxParticlesField.text())
    
    # TODO make this variables activate or not the second beneficial and deleterious
    if mainWin.MainTabBar.BeneficialIncrementField.isChecked():
        BeneficialIncrement = True
    else:
        BeneficialIncrement = False
        
    if mainWin.MainTabBar.DeleteriousIncrementField.isChecked():
        DeleteriousIncrement = True
    else:
        DeleteriousIncrement = False
    
    FirstBeneficial = float(mainWin.MainTabBar.FirstBeneficialField.text())
    SecondBeneficial = float(mainWin.MainTabBar.SecondBeneficialField.text())
    FirstDeleterious = float(mainWin.MainTabBar.FirstDeleteriousField.text())
    SecondDeleterious = float(mainWin.MainTabBar.SecondDeleteriousField.text())
    
    ChangeCycle = int(mainWin.MainTabBar.ChangeCycleField.text())
    
    if mainWin.MainTabBar.InfectionUserDefinedField.isChecked():
        InfectionUserDefined = True
    else:
        InfectionUserDefined = False
        
    UserDefindedCycleForInfection = int(mainWin.MainTabBar.UserDefindedCycleForInfectionField.text())
        
    for i in range(4):
        key = int(mainWin.MainTabBar.IntervalsFields[i].text())
        value = int(mainWin.MainTabBar.ProbFields[i].text())
        
        DrawIntervals.update({key : value})
    
#    DrawIntervals = {4: 0, 13: 0, 24: 0, 42: 100}
    
    Matrix = []
    InfectionWarnings = []
    InfectionWarningsCycle = []
    InfectionCycle = {}
    CyclesForDrawing = [] 
    DrawingWeights = []
    DrawnCycles = []
    
    DeleteriousProbability = [0] * Cycles
    BeneficialProbability = [0] * Cycles
    
    DrawIntervalsKeys = list(DrawIntervals.keys())
    
    if mainWin.MainTabBar.NewWorksheetEachPatientField.isChecked():
        NewWorksheetEachPatient = True
    else:
        NewWorksheetEachPatient = False
    
def Setup():
    
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
    
def ConfigureExcel():
    
    global MaxWorksheetSize, workbook, worksheet, HorizAlign, LastRowAvailable, bold

    MaxWorksheetSize = 1000000 # Max number of lines per worksheet
    
    ExcelFileName = "TFounderSim" + datetime.now().strftime('%d-%m-%Y_%H-%M-%S') + '.xlsx'
    workbook = xlsxwriter.Workbook(ExcelFileName, {'constant_memory': True})
    #workbook = xlsxwriter.Workbook(ExcelFileName)
    worksheet = workbook.add_worksheet()
    HorizAlign = workbook.add_format()
    HorizAlign.set_align('center')
    
    bold = workbook.add_format({'bold': True})
    LastRowAvailable = 0
    
    # set_column(column1, column2, size)
    worksheet.set_column(0, 0, 20)
    worksheet.set_column(2, 2, 8)
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
    
def MakeNewWorksheet():
    
    global MaxWorksheetSize, workbook, worksheet, HorizAlign, LastRowAvailable, bold, LastPatient
    
    worksheet = workbook.add_worksheet()
    
    HorizAlign = workbook.add_format()
    HorizAlign.set_align('center')

    bold = workbook.add_format({'bold': True})
    LastRowAvailable = 0
    LastPatient = -1

    # set_column(column1, column2, size)
    worksheet.set_column(0, 0, 20)
    worksheet.set_column(2, 2, 8)
    worksheet.set_column(14, 14, 12)
    worksheet.set_column(15, 15, 10)
    worksheet.set_column(16, 16, 13)
    worksheet.set_column(17, 17, 13)
    worksheet.set_column(18, 18, 16)
    
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
            if (DeleteriousProbability[i - 1] + Increment <= (1 - len(BeneficialProbability))):
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
            if (BeneficialProbability[i - 1] + Increment <= (1 - len(DeleteriousProbability))):
                BeneficialProbability[i] = BeneficialProbability[i - 1] + Increment
            else:
                BeneficialProbability[i] = BeneficialProbability[i - 1]

def Run():
    
    SetupInitialParameters()
    
    for i in range(SimulationTimes):
        RunSimulation(i)
 
def RunSimulation(SimulationNumber):
    
    global LastPatient, workbook, worksheet, HorizAlign, LastRowAvailable, MaxR, Simulating
    
    ConfigureExcel() 
    MakeNewWorksheet()
    
    ConsoleOut = mainWin.MainTabBar.ConsoleOutput
    
    mainWin.MainTabBar.SetupTabStatusBar.setStyleSheet("background: yellow")
    mainWin.MainTabBar.SetupTabStatusBar.showMessage("Simulation " + str(SimulationNumber + 1) + "/" + str(SimulationTimes) + " Running")
    
    ConsoleOut.append("Simulation started: " + str(datetime.now()))
    ConsoleOut.append("")
    
    startTime = datetime.now()
    
    Setup()
    
    # Populates the CyclesForDrawing array with number of cycles
    for i in range(Cycles):
        CyclesForDrawing.append(i)
    
    # Main Loop to create more particles on the next Cycles from the Cycle Zero.
    # Each matrix position will bring a value. This value will be mutiplied by its own class number. 
    for g in range(Generations):
            
        for p in range(pow(Gen1Patients, g)): # pow(Gen1Patients, g) gives the generation size
            
            print("Patient started: GEN " + str(g) + " - P " + str(p))
            ConsoleOut.append("Patient started: GEN " + str(g) + " - P " + str(p))
#            worksheet.write(LastRowAvailable + 1, 0, "Patient:")
            TableOutput.appendRow(QStandardItem("Generation: " + str(g)))
            TableOutput.appendRow(QStandardItem("Patient: " + str(p)))
            
            worksheet.write(LastRowAvailable + 1, 1, "Generation: ")
            worksheet.write(LastRowAvailable + 1, 2, str(g))
            worksheet.write(LastRowAvailable + 1, 3, "Patient: ")
            worksheet.write(LastRowAvailable + 1, 4, str(p))
            LastRowAvailable += 1
            
            RunPatient(g, p) 
            Matrix[g][p].clear()
            LastPatient = 0
            DrawingWeights.clear()
            InfectionWarnings.clear()
            InfectionWarningsCycle.clear()
            MaxR = 0
            
            if LastRowAvailable >= MaxWorksheetSize or NewWorksheetEachPatient:
                worksheet = workbook.add_worksheet()
                worksheet.set_column(0, 0, 20)
                worksheet.set_column(14, 14, 12)
                worksheet.set_column(15, 15, 10)
                worksheet.set_column(16, 16, 13)
                worksheet.set_column(17, 17, 13)
                worksheet.set_column(18, 18, 16)

                LastRowAvailable = 0
            
        LastPatient = -1 
        
    CyclesForDrawing.clear()
        
    ConsoleOut.append("")
    ConsoleOut.append("Simulation ended: " + str(datetime.now()))
    ConsoleOut.append("Total run time: " + str(datetime.now() - startTime))
    ConsoleOut.append("Date: " + str(datetime.now()))
    ConsoleOut.append("Python Implementation: " + platform.python_implementation())
    ConsoleOut.append("")
    ConsoleOut.append("*******************************************************")
    ConsoleOut.append("")
    
    TableOutput.appendRow(QStandardItem("Simulation ended: " + str(datetime.now())))
    TableOutput.appendRow(QStandardItem("Total run time: " + str(datetime.now() - startTime)))
    TableOutput.appendRow(QStandardItem("Date: " + str(datetime.now())))
    TableOutput.appendRow(QStandardItem("Python Implementation: " + platform.python_implementation()))
    
    TableView.resizeColumnsToContents()
    TableView.resizeRowsToContents()
        
    # worksheet.write(Row, Column, String, format)
    LastRowAvailable += 2
    worksheet.write(LastRowAvailable, 0, "Total run time: " + str(datetime.now() - startTime), bold)
    worksheet.write(LastRowAvailable + 1, 0, "Date: " + str(datetime.now()), bold)
    workbook.close()
        
    mainWin.MainTabBar.SetupTabStatusBar.setStyleSheet("background: lightgreen")
    mainWin.MainTabBar.SetupTabStatusBar.showMessage("Simulation " + str(SimulationNumber + 1) + "/" + str(SimulationTimes) + " Ended")
    
    # if the simulation takes less than 1 second to process
    # we may lose (overwrite) Excel files, so, we wait 1 second before next simulation
    # TODO it can't be a time.sleep because it freezes the program
    time.sleep(1.0) 
        
    mainWin.MainTabBar.SetupTabStatusBar.setStyleSheet("background: lightgray")
    mainWin.MainTabBar.SetupTabStatusBar.showMessage("T-Founder Ready")
     
def RunPatient(g, p):
    
    global LastRowAvailable, InfectionCycle
    
    if InfectionUserDefined:
        for i in range(1, NumberOfInfectionCycles + 1):
            InfectionCycle[i] = UserDefindedCycleForInfection
        
    else:
        for i in range(Cycles):
            # Populates the DrawingWeights array
            if i <= DrawIntervalsKeys[0]:
                DrawingWeights.append(DrawIntervals[4])
            elif i > DrawIntervalsKeys[0] and i <= DrawIntervalsKeys[1]:
                DrawingWeights.append(DrawIntervals[13])
            elif i > DrawIntervalsKeys[1] and i <= DrawIntervalsKeys[2]:
                DrawingWeights.append(DrawIntervals[24])
            else:
                DrawingWeights.append(DrawIntervals[42])
                
#        print(DrawingWeights)
            
        DrawnCycles = random.choices(CyclesForDrawing, DrawingWeights, k = NumberOfInfectionCycles)
        
        for i in range(1, NumberOfInfectionCycles + 1):
            InfectionCycle[i] = DrawnCycles[i - 1]
            
#        print(InfectionCycle)
    
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
        ConsoleOut.append("Patient " + str(p) + " Cycle " + str(Cy) + " has no particles.")
#        OutputFile.write("Patient " + str(p) + " Cycle " + str(Cy) + " has no particles.") 
        text = "G" + str(g) + " " + "P" + str(p) + " Cycle " + str(Cy) + " has no particles."
        InfectionWarnings.append(text)
        InfectionWarningsCycle.append(None)
        
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
#    OutputFile.write("G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy) + "\n") 
    
    text = "G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy)
    InfectionWarnings.append(text)
    InfectionWarningsCycle.append(Cy)
#    worksheet.write(LastRowAvailable, 0, "G " + str(g) + " P " + str(p) + " infected G " + str(g + 1) + " P " + str(patient) + " at cycle " + str(Cy))
#    LastRowAvailable += 1

def SaveData(g, p, Cy):
    global LastRowAvailable, LastPatient, MaxR
    
    Mi = 0
    
    PercentageOfParticlesUp = 0.0
    PercentageOfParticlesDown = 0.0
    
    LastRowAvailable += 1
    
    if LastPatient != p:
    
        for R in range(Classes):
            # fill a line in the Excel file with R0, R1, R2 .... R10
            worksheet.write(LastRowAvailable, R + 1, "R" + str(R), HorizAlign)
            
        worksheet.write(LastRowAvailable, 0, "Cycle", HorizAlign)
        worksheet.write(LastRowAvailable, 12, "Cycle Particles", HorizAlign)
        worksheet.write(LastRowAvailable, 13, "Mi", HorizAlign)
        
        
        worksheet.write(LastRowAvailable, 14, "Particles Up", HorizAlign)
        worksheet.write(LastRowAvailable, 15, "Particles Up - %", HorizAlign)
        worksheet.write(LastRowAvailable, 16, "Particles Down", HorizAlign)
        worksheet.write(LastRowAvailable, 17, "Particles Down - %", HorizAlign)

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
        
        if(len(Matrix[g][p][Cy]) > 0):       
            MaxR = GetMaxR(ClassCount)
            
        if (len(Matrix[g][p][Cy]) == 0):
            MaxR = 999
#            MaxR = str(GetMaxR(ClassCount)).replace(str(0), str(numpy.NaN))
    
    # variable to store row and write to Qt table
    Row = []
    
    Row.append(QStandardItem(str(Cy)))
    
    for R in range(Classes):
        # fill a line in the Excel file with number of particles from R0, R1, R2 .... R10
        worksheet.write(LastRowAvailable, R + 1, ClassCount[R], HorizAlign)
        Row.append(QStandardItem(str(ClassCount[R])))
        
    worksheet.write(LastRowAvailable, 0, Cy, HorizAlign)
    
    worksheet.write(LastRowAvailable, 12, len(Matrix[g][p][Cy]), HorizAlign)
    Row.append(QStandardItem(str(len(Matrix[g][p][Cy]))))
    
    Mi = GetMi(ClassCount, len(Matrix[g][p][Cy]))
    worksheet.write(LastRowAvailable, 13, Mi, HorizAlign)
    Row.append(QStandardItem(str(Mi)))
        
    worksheet.write(LastRowAvailable, 14, ClassUpParticles[g][p][Cy], HorizAlign)
    worksheet.write(LastRowAvailable, 15, PercentageOfParticlesUp, HorizAlign)
    worksheet.write(LastRowAvailable, 16, ClassDownParticles[g][p][Cy], HorizAlign)
    worksheet.write(LastRowAvailable, 17, PercentageOfParticlesDown, HorizAlign)
    
    Row.append(QStandardItem(str(ClassUpParticles[g][p][Cy])))
    Row.append(QStandardItem(str(PercentageOfParticlesUp)))
    Row.append(QStandardItem(str(ClassDownParticles[g][p][Cy])))
    Row.append(QStandardItem(str(PercentageOfParticlesDown)))
        
#    LastRowAvailable += 1
    
    TableOutput.appendRow(Row)
    
    if Cy == Cycles - 1:
        LastRowAvailable += 2
        
        worksheet.write(LastRowAvailable, 0, "Max R at Cycle 0")
        worksheet.write(LastRowAvailable, 1, MaxR, HorizAlign)
        
        TableOutput.appendRow(QStandardItem("Max R at Cycle 0: " + str(MaxR)))
        
        LastRowAvailable += 1
                
        for i in range(len(InfectionWarnings)):
            worksheet.write(LastRowAvailable, 0, InfectionWarnings[i])
            worksheet.write(LastRowAvailable, 2, InfectionWarningsCycle[i])
            
            TableOutput.appendRow(QStandardItem(InfectionWarnings[i]))
            #TableOutput.appendRow(QStandardItem(InfectionWarningsCycle[i]))
            
            LastRowAvailable += 1
        
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
    
#    global LastRowAvailable
    
#    worksheet.write(LastRowAvailable, 0, "Python Implementation", bold)
#    LastRowAvailable += 1
#    
#    worksheet.write(LastRowAvailable, 0, platform.python_implementation(), bold)
#    LastRowAvailable += 1

    try:
        import cpuinfo
        print("CPU: " + cpuinfo.cpu.info[0]['ProcessorNameString'])
        ConsoleOut.append("CPU: " + cpuinfo.cpu.info[0]['ProcessorNameString'])
#        worksheet.write(LastRowAvailable, 0, "CPU: " + cpuinfo.cpu.info[0]['ProcessorNameString'])
#        LastRowAvailable += 1
    except:
        print("No cpuinfo.py module. Download it at https://github.com/pydata/numexpr/blob/master/numexpr/cpuinfo.py")
        ConsoleOut.append("No cpuinfo.py module. Download it at https://github.com/pydata/numexpr/blob/master/numexpr/cpuinfo.py")
#        worksheet.write(LastRowAvailable, 0, "No cpuinfo.py module. Download it at https://github.com/pydata/numexpr/blob/master/numexpr/cpuinfo.py")
#        LastRowAvailable += 1
        
    print("Processor: " + platform.processor())
    print("Architecture (32 or 64 bits): " + platform.machine())
    print("OS: " + platform.platform())
    
    ConsoleOut.append("Processor: " + platform.processor())
    ConsoleOut.append("Architecture (32 or 64 bits): " + platform.machine())
    ConsoleOut.append("OS: " + platform.platform())
    ConsoleOut.append("")
    
#    worksheet.write(LastRowAvailable, 0, "Processor: " + platform.processor())
#    LastRowAvailable += 1
#    worksheet.write(LastRowAvailable, 0, "Architecture (32 or 64 bits): " + platform.machine())
#    LastRowAvailable += 1
#    worksheet.write(LastRowAvailable, 0, "OS: " + platform.platform() + "\n")
#    LastRowAvailable += 1
        
if __name__ == "__main__":
    main()

# TODO fazer gráficos com frequência relativa: porcentagem de partículas em cada classe
# TODO gerar gráfico boxplot com R Max (Fig.14 pré-dissertação).
# TODO Colocar opção de infectar paciente sempre com partículas das classes mais altas.
# TODO fazer um resumo de dados informando qual foi o paciente máximo com partículas virais dentro dele e qual o total de pacientes popssíveis.
