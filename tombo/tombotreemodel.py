from PyQt4 import QtCore, QtGui


class Node(object):
    """ Represents abstract node in our model.
        Base class for FolderNode, SimpleNoteNode, etc.
    """

    def __init__(self, name, parent=None):
        """ Node initializer """
        self._name = name
        self._children = []
        self._parent = parent
        if parent is not None:
            parent.addChild(self)

    def typeInfo(self):
        return "Node"

    def addChild(self, child):
        self._children.append(child)

    def insertChild(self, position, child):
        if position < 0 or position > len(self._children):
            return False
        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self._children):
            return False
        child = self._children.pop(position)
        child._parent = None

        return True

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def log(self, tabLevel=-1):
        """ Returns text interpretation of the model """
        output = ""
        tabLevel += 1

        #add indents
        output += tabLevel * "----"
        output += self._name + "\n"
        for child in self._children:
            output += child.log(tabLevel)
        tabLevel -= 1
        return output

    def __repr__(self):
        return self.log()


class SimpleNoteNode(Node):
    def __init__(self, name, filename, parent=None):
        super(SimpleNoteNode, self).__init__(name, parent)
        self.filename = filename

    def typeInfo(self):
        return "SimpleNoteNode"


class FolderNode(Node):
    def __init__(self, name, parent=None):
        super(FolderNode, self).__init__(name, parent)

    def typeInfo(self):
        return "FolderNode"


class TreeViewModel(QtCore.QAbstractItemModel):
    """ Implementation of QAbstractItemModel for Tombo
        Items are nodes - they represent folders, notes and encoded notes
    """

    def __init__(self, root, parent=None):
        """INPUTS: Node, QObject"""
        super(TreeViewModel, self).__init__(parent)
        self._rootNode = root

    def rowCount(self, parent):
        """
            INPUTS: QModelIndex
            OUTPUT: int
        """
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent):
        """ INPUTS: QModelIndex
            OUTPUT: int
        """
        return 1

    def data(self, index, role):
        """
         OUTPUT: QVariant, strings are cast to QString which is a QVariant
         INPUTS: QModelIndex, int
        """
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.name()

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                typeInfo = node.typeInfo()

                if typeInfo == "SimpleNoteNode":
                    return QtGui.QIcon(QtGui.QPixmap(":/Note.png"))

                if typeInfo == "FolderNode":
                    return QtGui.QIcon(QtGui.QPixmap(":/folder.png"))

                if typeInfo == "Encoded":
                    return QtGui.QIcon(QtGui.QPixmap(":/Encoded.png"))

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """ INPUTS: QModelIndex, QVariant, int (flag)"""
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                node = index.internalPointer()
                node.setName(value)
                return True
        return False

    def headerData(self, section, orientation, role):
        """INPUTS: int, Qt::Orientation, int"""
        """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Scenegraph"
            else:
                return "Typeinfo"

    def flags(self, index):
        """INPUTS: QModelIndex"""
        """OUTPUT: int (flag)"""
        flags = QtCore.Qt.ItemIsEnabled
        flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEditable
        return flags

    def parent(self, index):
        """INPUTS: QModelIndex"""
        """OUTPUT: QModelIndex"""
        """Should return the parent of the node with the given QModelIndex"""
        node = self.getNode(index)
        parentNode = node.parent()

        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):
        """ INPUTS: int, int, QModelIndex
            OUTPUT: QModelIndex
            Should return a QModelIndex that corresponds to
             the given row, column and parent node
        """
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def getNode(self, index):
        """
            INPUTS: QModelIndex
        """
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._rootNode

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        """
            INPUTS: int, int, QModelIndex
        """
        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)

        for _ in range(rows):
            childCount = parentNode.childCount()
            childNode = Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)

        self.endInsertRows()

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        """
            INPUTS: int, int, QModelIndex
        """

        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)

        for _ in range(rows):
            success = parentNode.removeChild(position)

        self.endRemoveRows()

        return success

    def log(self):
        #get the first node
        return self._rootNode.log()

    def __repr__(self):
        return self.log()
