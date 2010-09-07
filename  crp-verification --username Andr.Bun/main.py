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
print '\n                              -- National level --\n'
processLevel(paramsStruct, pathsAndUtilities, minMaxClass, inputsClipped.levelStatisticsName[0],
             outputs.resultLevel[0])
#verify.checkZonalSums(resultLevel[0])

# Processing level 1 (subnational - regions):
print '\n                            -- Subnational level --\n'
processLevel(paramsStruct, pathsAndUtilities, minMaxClass, inputsClipped.levelStatisticsName[1],
             outputs.resultLevel[1])
#verify.checkZonalSums(resultLevel[1])

print '\n                            -- Final calculations --\n'
print time.strftime("%H:%M:%S", time.localtime()) + ' Calculations started'
print 'Preparing calibrated national zones'

# calibrate subnational layer
calibrateLevel(paramsStruct, pathsAndUtilities, minMaxClass, 1)
#verify.checkZonalSums(outputs.combinedResult[1])

print time.strftime("%H:%M:%S", time.localtime()) + ' Finished'

# Processing level 1:
print '\n                            -- Subnational level --\n'
#gp.ZonalStatistics_sa(subnationalUnits, "Value", resSubnational, sumSubnational, "SUM", "DATA")

print '\n                            -- Subregional level --\n'
# Processing level 2:
processLevel(paramsStruct, pathsAndUtilities, minMaxClass, inputsClipped.levelStatisticsName[2],
             outputs.resultLevel[2])

# calibrate subregional layer
calibrateLevel(paramsStruct, pathsAndUtilities, minMaxClass, 2)
#verify.checkZonalSums(outputs.combinedResult[2])

pathsAndUtilities.processResults()

# Delete tmp files
print '         Cleanup temporary files'
pathsAndUtilities.cleanUp(inputsClipped)
pathsAndUtilities.cleanUp(tmp)

print time.strftime("%H:%M:%S", time.localtime()) + ' Finished'