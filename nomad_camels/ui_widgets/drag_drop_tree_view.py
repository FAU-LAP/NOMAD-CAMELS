from PySide6.QtWidgets import QTreeView, QAbstractItemView
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QDropEvent, QKeyEvent, QPainter, QColor


class Drag_Drop_TreeView(QTreeView):
    """This Class is used for the protocol sequence. Most importantly it
    emits the dragdrop signal when something is dragged / dropped.

    Parameters
    ----------

    Returns
    -------

    """

    dragdrop = Signal()
    del_clicked = Signal()

    def __init__(self):
        super(Drag_Drop_TreeView, self).__init__()
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, e: QDropEvent) -> None:
        """

        Parameters
        ----------
        e: QDropEvent :


        Returns
        -------

        """
        super(Drag_Drop_TreeView, self).dropEvent(e)
        self.dragdrop.emit()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """

        Parameters
        ----------
        event: QKeyEvent :


        Returns
        -------

        """
        if event.key() == Qt.Key_Delete:
            self.del_clicked.emit()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.model() is not None and self.model().rowCount() == 0:
            painter = QPainter(self.viewport())
            painter.setPen(QColor(128, 128, 128))  # Gray color
            # Set font to be larger and bold
            font = self.font()
            font.setPointSize(font.pointSize() + 2)  # Make font larger
            font.setBold(True)
            painter.setFont(font)
            rect = self.viewport().rect()
            painter.drawText(rect, Qt.AlignCenter, "Right-click to add\nyour first step here")
 
