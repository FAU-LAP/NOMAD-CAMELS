from PySide6.QtCore import Signal
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
    protocol_signal = Signal(str, dict)

    def __init__(self, parent=None, protocols_dict=None):
        super().__init__(parent=parent)

        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.order_list = []
        self.protocol_name_variables = {}

        # Connect the rowsMoved signal to the update_order_list slot
        self.model().rowsMoved.connect(self.update_order_list)
        self.protocols_dict = protocols_dict or {}

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
        item_widget.checkbox.clicked.connect(self.check_next_protocol)
        item_widget.button.clicked.connect(self.update_order_list)

        # Add the item to the order list
        self.order_list.append(item)
        self.protocol_name_variables[str(item)] = (
            text,
            self.protocols_dict[text].variables,
        )

    def check_next_protocol(self):
        # Check if the next protocol is ready to run
        if len(self.order_list) == 0:
            return False

        # Get the first item in the order list
        item = self.order_list[0]
        widget = self.itemWidget(item)
        checkbox = widget.layout().itemAt(0).widget().checkbox

        # If the checkbox is checked, emit the run signal
        if checkbox.isChecked():
            self.protocol_signal.emit(*self.protocol_name_variables[str(item)])
            return True
        return False

    def remove_first(self):
        if len(self.order_list) == 0:
            return
        self.remove_item(self.order_list[0], ask=False)

    def remove_item(self, item, ask=True):
        # ask the user if they are sure
        name = self.itemWidget(item).layout().itemAt(0).widget().name
        if ask:
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
        self.check_next_protocol()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    widget = RunQueue()
    widget.show()

    app.exec()
