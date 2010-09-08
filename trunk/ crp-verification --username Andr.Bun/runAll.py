# Created:  07/09/2010
# Author:   Andriy Bun
# Modified: 
# Name:     Comparison of global cropland cover script modified for use with GUI

from iterableStruct import iterableStruct
from utils import utils
from processLevel import processLevel
from calibrateLevel import calibrateLevel
from PyQt4 import QtGui, QtCore, Qt

def runAll(gui):
    gui.printTextTime('Calculations started')
    # coordinates for clipping rasters:
    coords = "-18 4 0 17"
    #coords = "-18 -35 52 38"
    
    # minimum and maximum classes of territory in "mark high"
    minMaxClass = iterableStruct()
    minMaxClass.minClass = 1
    minMaxClass.maxClass = 31

    # initialize paths
    pathsAndUtilities = utils(gui);
    paramsStruct = pathsAndUtilities.paramsStruct;
    inputsNotClipped = pathsAndUtilities.inputsNotClipped
    inputsClipped = pathsAndUtilities.inputsClipped
    outputs = pathsAndUtilities.outputs
    tmp = pathsAndUtilities.tmp
    
    gui.printTextTime('-- Preprocessing rastsers --')
    
    # clip rasters and convert to int(if necessary) 
    pathsAndUtilities.clipRasterInt(inputsNotClipped.countries, inputsClipped.countries, coords)
    pathsAndUtilities.clipRasterInt(inputsNotClipped.subnationalUnits, inputsClipped.subnationalUnits, coords)
    pathsAndUtilities.clipRasterInt(inputsNotClipped.subregionalUnits, inputsClipped.subregionalUnits, coords)
    pathsAndUtilities.clipRaster(inputsNotClipped.mark_high_32, inputsClipped.mark_high_32, coords)
    pathsAndUtilities.clipRaster(inputsNotClipped.cell_area, inputsClipped.cell_area, coords)
    pathsAndUtilities.clipRaster(inputsNotClipped.statLayer, inputsClipped.statLayer, coords)
    
    # convert rasters to proper measurement units
    pathsAndUtilities.prepareRasters()
    
    # Processing level 0 (countries):
    gui.printTextTime('-- National level --')
    processLevel(paramsStruct, pathsAndUtilities, minMaxClass, inputsClipped.levelStatisticsName[0],
                 outputs.resultLevel[0], gui)
    #verify.checkZonalSums(resultLevel[0])
    
    # Processing level 1 (subnational - regions):
    gui.printTextTime('-- Subnational level --')
    processLevel(paramsStruct, pathsAndUtilities, minMaxClass, inputsClipped.levelStatisticsName[1],
                 outputs.resultLevel[1], gui)
    #verify.checkZonalSums(resultLevel[1])
    
    # calibrate subnational layer
    gui.printTextTime('-- Calibrating subnational level --')
    calibrateLevel(paramsStruct, pathsAndUtilities, minMaxClass, 1, gui)
    #verify.checkZonalSums(outputs.combinedResult[1])
    
    # Processing level 2:
    gui.printTextTime('-- Subregional level --')
    processLevel(paramsStruct, pathsAndUtilities, minMaxClass, inputsClipped.levelStatisticsName[2],
                 outputs.resultLevel[2], gui)
    
    # calibrate subregional layer
    gui.printTextTime('-- Calibrating subregional level --')
    calibrateLevel(paramsStruct, pathsAndUtilities, minMaxClass, 2, gui)
    #verify.checkZonalSums(outputs.combinedResult[2])
    
    pathsAndUtilities.processResults()
    
    # Delete tmp files
    gui.printTextTime('-- Cleanup temporary files --')
    pathsAndUtilities.cleanUp(inputsClipped)
    pathsAndUtilities.cleanUp(tmp)
    
    gui.printTextTime('Finished')
