from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QFrame,
    QPushButton,
    QCheckBox,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QMessageBox,
)


class RunWidget(QWidget):
    def __init__(self, text):
        super().__init__()
        self.name = text

        self.layout = QHBoxLayout(self)

        self.checkbox = QCheckBox("ready")
        self.checkbox.setToolTip(
            "The next run will start automatically if it is set as ready.\nOtherwise the execution will pause."
        )
        self.label = QLabel(text)
        self.button = QPushButton("remove")
        self.button.setMaximumWidth(80)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.button)


class RunQueue(QListWidget):
    def __init__(self):
        super().__init__()

        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.order_list = []

        # Connect the rowsMoved signal to the update_order_list slot
        self.model().rowsMoved.connect(self.update_order_list)

    def add_item(self, text):
        item = QListWidgetItem(self)

        # Create a QFrame
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Sunken)

        # Create the run widget and add it to the frame
        item_widget = RunWidget(text)
        layout = QHBoxLayout(frame)
        layout.addWidget(item_widget)

        item.setSizeHint(frame.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, frame)

        item_widget.button.clicked.connect(lambda: self.remove_item(item))

        # Add the item to the order list
        self.order_list.append(item)

    def remove_item(self, item):
        # ask the user if they are sure
        name = self.itemWidget(item).layout().itemAt(0).widget().name
        dialog = QMessageBox()
        dialog.setWindowTitle("Remove run")
        dialog.setText(f"Remove {name} from the queue?")

        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)
        if dialog.exec() == QMessageBox.No:
            return

        # Remove the item from the order list
        self.order_list.remove(item)

        # Remove the item from the QListWidget
        self.takeItem(self.row(item))

    def update_order_list(self):
        # Update the order list to match the current order of items in the QListWidget
        self.order_list = [self.item(i) for i in range(self.count())]

class VariableWidget(QWidget):
    def __init__(self, text):
        super().__init__()
        self.name = text

        self.layout = QHBoxLayout(self)

        self.checkbox = QCheckBox("ready")
        self.checkbox.setToolTip(
            "The next run will start automatically if it is set as ready.\nOtherwise the execution will pause."
        )
        self.label = QLabel(text)
        self.button = QPushButton("remove")
        self.button.setMaximumWidth(80)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.button)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    widget = RunQueue()
    widget.show()

    app.exec()
