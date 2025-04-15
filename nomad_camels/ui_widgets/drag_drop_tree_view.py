from PySide6.QtWidgets import QTreeView, QAbstractItemView
from PySide6.QtCore import Signal, Qt, QTimer, QItemSelectionModel, QModelIndex
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
        super().__init__()
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self._dragged_item_data = None  # store data of the dragged item

    def startDrag(self, supportedActions):
        # Capture the data of the item(s) that are about to be dragged.
        indexes = self.selectionModel().selectedIndexes()
        if indexes:
            # Assuming single selection; you can extend this to multiple items.
            self._dragged_item_data = indexes[0].data()
        super().startDrag(supportedActions)

    def dropEvent(self, e: QDropEvent) -> None:
        super().dropEvent(e)
        # Use a short delay to allow the internal move to finish updating the model.
        if self._dragged_item_data is not None:
            QTimer.singleShot(0, self._select_dragged_item)
        self.dragdrop.emit()

    def _select_dragged_item(self):
        new_index = self._find_index_by_data(self._dragged_item_data, self.model())
        if new_index.isValid():
            self.selectionModel().setCurrentIndex(
                new_index,
                QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows,
            )
        # Clear stored data after selection update.
        self._dragged_item_data = None

    def _find_index_by_data(self, data, model, parent_index=QModelIndex()):
        """Recursively searches the model for an index with matching data."""
        for row in range(model.rowCount(parent_index)):
            index = model.index(row, 0, parent_index)
            if index.data() == data:
                return index
            child_index = self._find_index_by_data(data, model, index)
            if child_index.isValid():
                return child_index
        return QModelIndex()

    def keyPressEvent(self, event: QKeyEvent) -> None:
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
            painter.drawText(
                rect, Qt.AlignCenter, "Right-click to add\nyour first step here"
            )
