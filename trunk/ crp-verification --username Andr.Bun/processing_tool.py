'''
# Name:     ArcGIS interface for smth
# Created:  30/09/2010
# Author:   Andriy Bun, andr.bun@gmail.com
# Modified: 
'''

from iterableStruct import iterableStruct
from runAll import runAll
import sys, time
import arcgisscripting

# pass GUI arguments to variables
inputsNotClipped = iterableStruct()

inputsNotClipped.mark_high_32     = sys.argv[1]
inputsNotClipped.countries        = sys.argv[2]
inputsNotClipped.subnationalUnits = sys.argv[3]
inputsNotClipped.subregionalUnits = sys.argv[4]
inputsNotClipped.cell_area        = sys.argv[5]
inputsNotClipped.statLayer        = sys.argv[6]

coords = sys.argv[7]

output = sys.argv[8]

# Class interface for updating status in ArcGIS
class geoprocessingInfo():
    def __init__(self):
        self.gp = arcgisscripting.create()
        self.initialiseDefaultProgressor('Cropland validator working...')
    
    # print status with time
    def printTextTime(self, textToAppend):
        self.gp.AddMessage(time.strftime("%H:%M:%S", time.localtime()) + '\t' + textToAppend)
        
    # print status
    def printText(self, textToAppend):
#        self.gp.AddMessage('######################')
        self.gp.AddMessage(textToAppend)
#        self.gp.AddMessage('######################')
    
    # set default progress bar
    def initialiseDefaultProgressor(self, label):
        self.gp.SetProgressor("default", label)
        
    # set step progress bar
    def initialiseStepProgressor(self, label):
        self.gp.SetProgressor("step", label, 1, 100, 1)

    # update progress bar position
    def setProgress(self, value):
        self.gp.SetProgressorPosition(value)
        
    ''' TODO: add reset progress method '''
        
interface = geoprocessingInfo()
interface.setProgress(90)

runAll(interface, coords, inputsNotClipped, output)