from PySide6.QtWidgets import (
    QDialog,
    QMessageBox,
    QPushButton,
    QGridLayout,
    QWidget,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QStyle,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table


class FlyerButton(QPushButton):
    def __init__(self, parent=None, flyer_data=None, text=None):
        super().__init__(
            text=text or "Asynchronous measurement during protocol", parent=parent
        )
        self.flyer_data = flyer_data
        self.clicked.connect(self.open_flyer_window)
        self.setToolTip(
            "Set channels that should be read asynchronously during the protocol with a defined frequency.\nWarning: If you use read the same channel in the protocol, it might cause a conflict.\nWarning: If you run this as sub-protocol, the asynchronous acquisition will NOT be started."
        )
        self._update_icon()

    def set_flyer_data(self, flyer_data):
        """Set the flyer data and update the icon accordingly."""
        self.flyer_data = flyer_data
        self._update_icon()

    def _update_icon(self):
        # set checkmark as icon if data, otherwise remove icon
        if self.flyer_data:
            self.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        else:
            self.setIcon(QIcon())

    def open_flyer_window(self):
        flyer_window = FlyerWindow(self, flyer_data=self.flyer_data)
        if flyer_window.exec_():
            self.flyer_data = flyer_window.flyer_data
            self._update_icon()


class FlyerWindow(QDialog):
    def __init__(self, parent=None, flyer_data=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Define Asynchronous Acquisition - NOMAD CAMELS")

        self.flyer_data = flyer_data or []

        table_data = {"Name": [], "Reading Rate (s)": []}
        if flyer_data is not None:
            for data in flyer_data:
                table_data["Name"].append(data["name"])
                table_data["Reading Rate (s)"].append(data["read_rate"])

        self.flyer_table = AddRemoveTable(
            parent=self,
            headerLabels=["Name", "Reading Rate (s)"],
            tableData=table_data,
            editables=[],
            default_values={"Name": "", "Reading Rate": 1},
            add_tooltip="Add a new entry",
            remove_tooltip="Remove selected entry",
        )

        self.flyer_table.table.clicked.connect(self.change_flyer_def)
        self.flyer_table.added.connect(self._add_flyer)
        self.flyer_table.removed.connect(self._remove_flyer)

        self.flyer_def = QLabel("Select an entry!")

        # Create OK/Cancel dialog buttons.
        self.dialog_buttons = QDialogButtonBox()
        self.dialog_buttons.setOrientation(Qt.Horizontal)
        self.dialog_buttons.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )
        self.dialog_buttons.accepted.connect(self.accept)
        self.dialog_buttons.rejected.connect(self.reject)

        self.currently_selected = None

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.flyer_table, 0, 0)
        layout.addWidget(self.flyer_def, 0, 1)
        layout.addWidget(self.dialog_buttons, 1, 0, 1, 2)

    def _add_flyer(self, n):
        if n >= len(self.flyer_data):
            self.flyer_data.append({"name": "", "read_rate": "", "channels": {}})

    def _remove_flyer(self, n):
        self.flyer_data.pop(n)

    def accept(self):
        if not isinstance(self.flyer_def, QLabel):
            self.flyer_data[self.currently_selected] = self.flyer_def.get_data()
        return super().accept()

    def reject(self):
        """
        Overridden reject method that asks for confirmation before discarding changes.
        """
        discard_dialog = QMessageBox.question(
            self,
            "Discard Changes?",
            "All changes will be lost!",
            QMessageBox.Yes | QMessageBox.No,
        )
        if discard_dialog != QMessageBox.Yes:
            return
        super().reject()

    def change_flyer_def(self, index):
        if index is None:
            self.flyer_def.setText("Select an entry!")
            return
        n = index.row()
        self.currently_selected = n
        if not isinstance(self.flyer_def, QLabel):
            self.flyer_data[self.currently_selected] = self.flyer_def.get_data()
        flyer_data = self.flyer_data[n]
        flyer_def = FlyerDefiner(parent=self, flyer_data=flyer_data)
        flyer_def.name_changed.connect(self._update_name)
        flyer_def.read_rate_changed.connect(self._update_read_rate)
        self.layout().replaceWidget(self.flyer_def, flyer_def)
        self.flyer_def.deleteLater()
        self.flyer_def = flyer_def

    def _update_name(self, name):
        self.flyer_table.table_model.item(self.currently_selected, 0).setText(name)

    def _update_read_rate(self, read_rate):
        self.flyer_table.table_model.item(self.currently_selected, 1).setText(read_rate)


class FlyerDefiner(QWidget):
    name_changed = Signal(str)
    read_rate_changed = Signal(str)

    def __init__(self, parent=None, flyer_data=None):
        super().__init__(parent=parent)
        layout = QGridLayout()
        self.setLayout(layout)
        label_name = QLabel("Name:")
        self.lineEdit_name = QLineEdit(flyer_data.get("name", ""))
        self.lineEdit_name.textChanged.connect(self.name_changed)
        label_read_rate = QLabel("Reading Rate (s):")
        self.lineEdit_read_rate = QLineEdit(flyer_data.get("read_rate", ""))
        self.lineEdit_read_rate.textChanged.connect(self.read_rate_changed)

        labels = ["read?", "channel", "ignore failed"]
        self.channels_table = Channels_Check_Table(
            parent=self,
            headerLabels=labels,
            info_dict=flyer_data.get("channels", {}),
            title="Channels",
            checkables=[2],
        )

        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_name, 0, 1)
        layout.addWidget(label_read_rate, 1, 0)
        layout.addWidget(self.lineEdit_read_rate, 1, 1)
        layout.addWidget(self.channels_table, 2, 0, 1, 2)

    def get_data(self):
        return {
            "name": self.lineEdit_name.text(),
            "read_rate": self.lineEdit_read_rate.text(),
            "channels": self.channels_table.get_info(),
        }
