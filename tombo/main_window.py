'''
Created on Apr 11, 2012

@author: Mykhailo.Pershyn
'''
from PyQt4 import QtGui
from PyQt4 import QtCore
from main_window_ui import Ui_MainWindow
from core import Core


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, name=None, fl=0):
        QtGui.QMainWindow.__init__(self, parent=parent)
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.core = Core()
        self.treeView.setModel(self.core.model)

        # Actions
        self.actionExit.triggered.connect(QtGui.qApp.quit)
        self.actionSave.triggered.connect(self.save_current_note)
        self.actionModificationChanged.changed.connect(
            self.actionModificationChangedTriggered)

        self.treeView.connect(self.treeView.selectionModel(),
                              QtCore.SIGNAL("selectionChanged(QItemSelection, "
                                            "QItemSelection)"),
                              self.selectionChanged)

        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)

        #TODO: Restore previous position if in screen. if not - put in center
        self.center()
        self.show()

    def selectionChanged(self, selected, deselected):
        # TODO: if file edited - save or discard
        if self.actionSave.isEnabled() == True:
            # ask to save
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Note has been modified")
            msgBox.setInformativeText("Do you want to save your changes?")
            msgBox.setStandardButtons(QtGui.QMessageBox.Save |
                                      QtGui.QMessageBox.Discard |
                                      QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Save)
            ret = msgBox.exec_()
            # TODO: check the value
            print("User Choise os file save: {0}".format(ret))
            # if confirmed - save
            # if rejected - revert the selection

        sel = QtGui.QItemSelection(selected)
        # check that only one node is selected
        if sel.count() != 1:
            raise Exception("unknown item selected")
        # get the selected QModelIndex
        qmodelindex = sel.indexes()[0]

        node = self.core.model.getNode(qmodelindex)

        if node.typeInfo() == "SimpleNoteNode":
            path_to_file = self.core.add_parent_path_recursive(node)
            self.open_node_in_file_editor(path_to_file)

    def setWindowTitle(self, title, note_name=None):
        #        newTitle = QtGui.QApplication.translate(
#            "MainWindow",
#            "Tombo Reincarnation Prototype",
#            None,
#            QtGui.QApplication.UnicodeUTF8)
        # TODO: Set window title
        pass

    def open_node_in_file_editor(self, path_to_file):
        note_text = self.core.get_note_text(path_to_file)
        self.plainTextEdit.setPlainText(note_text)
        # TODO: add note name to window title

    def actionModificationChangedTriggered(self):
        # check for button state and print debug info
        changed = self.actionModificationChanged.isEnabled()
        # make save button active
        print("actionModificationChanged: {0}".format(changed))
        self.actionSave.setEnabled(changed)
        pass

    def save_current_note(self):
        print("save_current_note")

        content = self.plainTextEdit.toPlainText()
        print(content) # Stored as QTextDocument

        self.plainTextEdit.document().setModified(False)
        self.actionModificationChanged.setEnabled(False)
        self.actionSave.setEnabled(False)

        pass

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry(screen=1)
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def showMessage(self, msg):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(msg)
        msgBox.show()
        msgBox.exec_()

    def openMenu(self, position):
        #TODO: read this http://www.prog.org.ru/topic_21473_0.html
        # and fix implementation
        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        menu = QtGui.QMenu(self)
        if level == 0:
            menu.addAction(self.tr("Edit person"))
        elif level == 1:
            menu.addAction(self.tr("Edit object/container"))
        elif level == 2:
            menu.addAction(self.tr("Edit object"))
        menu.exec_(self.treeView.viewport().mapToGlobal(position))
