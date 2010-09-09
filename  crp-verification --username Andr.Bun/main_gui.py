# Created:  09/03/2010
# Author:   Andriy Bun
# Modified: 
# Name:     GUI for comparison of global cropland cover scripts

import time, sys, thread, threading
from PyQt4 import QtCore, QtGui
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from gui.mainWindow import Ui_MainWindow
from iterableStruct import iterableStruct
from runAll import runAll

class runAllThread(threading.Thread):
    def __init__(self, gui):
        self.__gui = gui
        self.__dummy = 0;
        threading.Thread.__init__(self)
    def run (self):
        runAll(self.__gui, self.__dummy)

# main window class
class mainWin(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.pushRunAll,QtCore.SIGNAL("clicked()"),self.__runAllInThread)
    
    # run all computations
    def __runAll(self):
        dummy = 0
        thread.start_new_thread(runAll, (self, dummy))
        self.printTextTime('thread finished')
        #runAll(self)
    
    def __runAllInThread(self):
        runAllThread(self).start()
        #runAllThread().run(self)
        self.printText('thread finished')

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
