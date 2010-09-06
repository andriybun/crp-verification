# Created:  09/03/2010
# Author:   Andriy Bun
# Modified: 19/08/2010
# Name:     Comparison of global cropland cover

import time
from iterableStruct import iterableStruct
from utils import utils
from processLevel import processLevel
from calibrateLevel import calibrateLevel

# coordinates for clipping rasters:
#coords = "6.5 45.4 7.5 46.5"
coords = "-18 4 0 17"
#coords = "-18 -35 52 38"

# minimum and maximum classes of territory in "mark high"
minMaxClass = iterableStruct()
minMaxClass.minClass = 1
minMaxClass.maxClass = 31

print time.strftime("%H:%M:%S", time.localtime())

# initialize paths
pathsAndUtilities = utils();
paramsStruct = pathsAndUtilities.paramsStruct;
inputsNotClipped = pathsAndUtilities.inputsNotClipped
inputsClipped = pathsAndUtilities.inputsClipped
outputs = pathsAndUtilities.outputs
tmp = pathsAndUtilities.tmp

# calibrate subregional layer
calibrateLevel(paramsStruct, pathsAndUtilities, minMaxClass, 2)
#verify.checkZonalSums(outputs.combinedResult[2])

pathsAndUtilities.processResults()

print time.strftime("%H:%M:%S", time.localtime()) + ' Finished'