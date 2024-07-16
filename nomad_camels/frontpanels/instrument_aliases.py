from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QHeaderView,
    QAbstractItemView,
    QSizePolicy,
    QFileDialog,
    QMessageBox,
    QDialogButtonBox,
    QLabel,
)
from PySide6.QtCore import Qt, Signal

from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table
from nomad_camels.utility import variables_handling


class Instrument_Alias_Config(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.buttonBox, 20, 0, 1, 2)

        instrument_combos = {"Instrument": variables_handling.devices.keys()}
        self.instrument_alias_table = AddRemoveTable(
            headerLabels=["Instrument", "Alias"]
        )

    def get_aliases(self):
        return
