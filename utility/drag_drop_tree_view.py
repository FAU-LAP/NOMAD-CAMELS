from PyQt5.QtWidgets import QTreeView, QAbstractItemView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QDropEvent, QKeyEvent



class Drag_Drop_TreeView(QTreeView):
    """This Class is used for the protocol sequence. Most importantly it
    emits the dragdrop signal when something is dragged / dropped."""
    dragdrop = pyqtSignal()
    del_clicked = pyqtSignal()

    def __init__(self):
        super(Drag_Drop_TreeView, self).__init__()
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, e: QDropEvent) -> None:
        super(Drag_Drop_TreeView, self).dropEvent(e)
        self.dragdrop.emit()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            self.del_clicked.emit()
