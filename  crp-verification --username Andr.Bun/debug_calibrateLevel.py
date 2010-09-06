# Date:   01/09/2010
# Author: Andriy Bun
# Name:   Process level function

import arcgisscripting, time

from processLevel import processLevel

def calibrateLevel(paramsStruct, pathsAndUtilities, minMaxClass, level):
    gp = arcgisscripting.create()
    gp.CheckOutExtension("Spatial")
    gp.OverWriteOutput = 1 # allow overwriting rasters:

    inputsClipped = pathsAndUtilities.inputsClipped
    tmp = pathsAndUtilities.tmp
    tmpDir = paramsStruct.tmpDir
    outputs = pathsAndUtilities.outputs

    statisticsLevel1 = tmpDir + inputsClipped.levelStatisticsName[level-1]
    statisticsLevel2 = tmpDir + inputsClipped.levelStatisticsName[level]

    # temporary rasters
    differName = "differ"
    differ = tmpDir + differName
    zones = tmpDir + "zones"
    areaUnits = tmpDir + "unit"
    sumLevel1 = tmpDir + "sum_l1"
    sumLevel2 = tmpDir + "sum_l2"
    OutRaster1 = tmp.OutRaster1
    OutRaster2 = tmp.OutRaster2
    OutRaster3 = tmp.OutRaster3

    gp.Copy_management(differ, OutRaster2)
    gp.Int_sa(OutRaster2,differ)
    gp.BuildRasterAttributeTable_management(differ,"OVERWRITE")
    cursor=gp.SearchCursor(differ)
    print cursor
    if cursor:
        # Processing calibrated raster:
        processLevel(paramsStruct, pathsAndUtilities, minMaxClass, differName,
                     outputs.resultForCalibratedLevel[level])

    gp.Delete_management(differ)
    #===============================================================================
    # combining final map
    #===============================================================================
    print time.strftime("%H:%M:%S", time.localtime()) + ' Combining final map...'

    gp.Con_sa(zones, outputs.resultLevel[level-1], OutRaster1, "#", "VALUE = 0")
    gp.Con_sa(zones, outputs.resultLevel[level], OutRaster2, OutRaster1, "VALUE = 1")
    gp.Con_sa(zones, outputs.resultForCalibratedLevel[level], outputs.combinedResult[level], OutRaster2, "VALUE = -1")
    
    

