from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter
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
    """
    A widget that represents a single run in the run queue. It contains a label with the name of the protocol, a checkbox whether the protocol is ready to run, and a button to remove the protocol from the queue.

    Parameters
    ----------
    text : str
        The name of the protocol / the text to display on the label."""

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
    """
    A QListWidget that represents the run queue. It contains a list of RunWidgets, each representing a single run in the queue. When a run is removed from the queue, the corresponding RunWidget is removed from the QListWidget. The order of the runs in the queue is determined by the order of the RunWidgets in the QListWidget. The RunQueue emits a signal when a the ready status of a run is changed, so that the next run can be started automatically.

    Each run can have its own variables, the values do not change the default settings for the protocol.
    """

    protocol_signal = Signal(str, dict, str)

    def __init__(self, parent=None, protocols_dict=None, variable_table=None):
        super().__init__(parent=parent)

        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.order_list = []
        self.protocol_name_variables = {}

        # Connect the rowsMoved signal to the update_order_list slot
        self.model().rowsMoved.connect(self.update_order_list)
        self.protocols_dict = protocols_dict or {}
        self.variable_table = variable_table
        self.selectionModel().selectionChanged.connect(self.change_variable_table)
        self.last_selected = None

    def add_item(self, text, api_uuid=None):
        """
        Add a new item to the run queue. The item is represented by a RunWidget, which is added to a QListWidgetItem, which is then added to the QListWidget. The item is also added to the order list, which determines the order of the runs in the queue. The name of the protocol and its variables are stored in the protocol_name_variables dictionary.
        """
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
        self.protocol_name_variables[str(item)] = [
            text,
            self.protocols_dict[text].variables,
            api_uuid,
        ]

    def check_checkbox(self, name):
        """
        Check the checkbox of the specified item.

        Parameters
        ----------
        name : str
        string of the QListWidgetItem. The item to check.
        """
        for item in self.order_list:
            if name == str(item):
                widget = self.itemWidget(item)
                checkbox = widget.layout().itemAt(0).widget().checkbox
                checkbox.setChecked(True)
                checkbox.clicked.emit()

    def update_variables_queue(self, name, variables, index):
        """
        Update the variables for a protocol in the queue.

        Parameters
        ----------
        name : str
            The name of the protocol.
        variables : dict
            The new variables for the protocol.
        """
        item = self.order_list[index]
        if name.startswith(self.protocol_name_variables[str(item)][0]):
            item = self.order_list[index]
        else:
            raise ValueError("The name of the protocol does not match the name of the protocol at this index in the queue.")
        self.protocol_name_variables[str(item)][1] = variables
        self.change_variable_table()
    
    def check_next_protocol(self):
        """
        Check if the first protocol in the queue is ready to run. If it is, emit the protocol_signal with the name of the protocol and its variables. If the protocol is not ready to run, do nothing.

        Returns
        -------
        bool
            True if the next protocol is ready to run, False otherwise.
        """
        # Check if the next protocol is ready to run
        if len(self.order_list) == 0:
            return False

        # Get the first item in the order list
        item = self.order_list[0]
        widget = self.itemWidget(item)
        checkbox = widget.layout().itemAt(0).widget().checkbox

        # If the checkbox is checked, emit the run signal
        if checkbox.isChecked():
            self.change_variable_table()
            self.protocol_signal.emit(*self.protocol_name_variables[str(item)])
            return True
        return False

    def remove_first(self):
        """
        Remove the first item in the queue.
        """
        if len(self.order_list) == 0:
            return
        self.remove_item(self.order_list[0], ask=False)

    def remove_item(self, item, ask=True):
        """
        Remove an item from the run queue. The item is removed from the order list and the QListWidget. If `ask` is True, a QMessageBox is shown to ask the user if they are sure they want to remove the item.

        Parameters
        ----------
        item : QListWidgetItem
            The item to remove.
        ask : bool, optional
            Whether to ask the user if they are sure they want to remove the item. The default is True.
        """
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
        self.protocol_name_variables.pop(str(item))
        self.order_list.remove(item)

        # Remove the item from the QListWidget
        self.takeItem(self.row(item))

    def remove_item_by_name(self, name):
        """
        Remove an item from the run queue by name.

        Parameters
        ----------
        name : str
            The name of the item to remove.
        """
        for item in self.order_list:
            if name == str(item):
                self.remove_item(item, ask=False)

    def update_order_list(self):
        """
        Update the order list to match the current order of items in the QListWidget

        """
        self.order_list = [self.item(i) for i in range(self.count())]
        self.check_next_protocol()

    def change_variable_table(self):
        """
        Change the variables displayed in the variable table to match the selected run.
        """
        if (
            self.last_selected is not None
            and str(self.last_selected) in self.protocol_name_variables
        ):
            self.protocol_name_variables[str(self.last_selected)][
                1
            ] = self.variable_table.update_variables()
        self.variable_table.editable_names = False
        self.variable_table.clear()
        # Get the current item
        self.last_selected = self.currentItem()
        if self.last_selected is None:
            self.variable_table.setHidden(True)
            return
        # Get the variables for the current item
        name, variables, = self.protocol_name_variables[str(self.last_selected)][:2]
        self.variable_table.protocol = self.protocols_dict[name]
        for var in variables:
            self.variable_table.append_variable(var, str(variables[var]), unique=False)
        self.variable_table.setHidden(False)
        self.variable_table.resizeColumnsToContents()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            painter = QPainter(self.viewport())
            painter.setPen(Qt.gray)

            # Set the font to be larger and bold
            font = painter.font()
            font.setPointSize(16)  # Adjust the size as needed
            font.setBold(True)
            painter.setFont(font)

            painter.drawText(self.rect(), Qt.AlignCenter, "Measurement Queue")
            painter.end()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    widget = RunQueue()
    widget.show()

    app.exec()
