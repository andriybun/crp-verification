# Created:  09/03/2010
# Author:   Andriy Bun
# Modified: 
# Name:     GUI for comparison of global cropland cover scripts

import time, sys
from PyQt4 import QtCore, QtGui
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from gui.mainWindow import Ui_MainWindow
from iterableStruct import iterableStruct
from runAll import runAll

# main window class
class mainWin(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.pushRunAll,QtCore.SIGNAL("clicked()"),self._runAll)
    
    # run all computations
    def _runAll(self):
        runAll(self)
    
    # print status with time to text box
    def printTextTime(self, textToAppend):
        self.ui.textEdit.append(time.strftime("%H:%M:%S", time.localtime()) + '\t' + textToAppend)
        self.ui.textEdit.setAlignment(QtCore.Qt.AlignLeft)
        
    # print status to text box
    def printText(self, textToAppend):
        self.ui.textEdit.append(textToAppend)
        self.ui.textEdit.setAlignment(QtCore.Qt.AlignCenter)
        
    def setProgress(self, value):
        self.ui.progressBar.setProperty("value", value)
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = mainWin()
    ui.show()
    sys.exit(app.exec_())
