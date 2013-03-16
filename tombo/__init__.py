import sys
from PyQt4 import QtGui
from main_window import MainWindow


def main():
        app = QtGui.QApplication(sys.argv)
        ex = MainWindow()
        ex.show()
        sys.exit(app.exec_())
