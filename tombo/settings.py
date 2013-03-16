'''
Created on Apr 11, 2012

@author: Mykhailo.Pershyn
'''
from PyQt4 import QtGui
from PyQt4.QtGui import QDialog
from settings_ui import Ui_Dialog
import sys


class Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None, name=None, fl=0):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.show()


app = QtGui.QApplication(sys.argv)
ex = Dialog()
ex.show()

sys.exit(app.exec_())
