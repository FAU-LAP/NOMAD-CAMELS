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
from nomad_camels.ui_widgets.warn_popup import WarnPopup


class Instrument_Alias_Config(QDialog):
    def __init__(self, parent=None, instrument_aliases=None, channel_aliases=None):
        super().__init__(parent=parent)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.buttonBox, 20, 0, 1, 2)

        self.instrument_aliases = instrument_aliases or {}
        self.channel_aliases = channel_aliases or {}

        instrument_combos = {"Instrument": variables_handling.devices.keys()}
        self.instrument_alias_table = AddRemoveTable(
            headerLabels=["Instrument", "Alias"],
            comboBoxes=instrument_combos,
            tableData=self.instrument_aliases,
            title="Instrument Aliases",
            askdelete=True,
        )
        self.layout().addWidget(self.instrument_alias_table, 0, 0)

        self.channel_alias_table = Channels_Check_Table(
            parent=self,
            title="Channel Aliases",
            use_aliases=False,
            info_dict=self.channel_aliases,
            headerLabels=["Use?", "Channel", "Alias"],
        )
        self.layout().addWidget(self.channel_alias_table, 0, 1)

        self.adjustSize()

    def accept(self):
        self.instrument_aliases = self.instrument_alias_table.update_table_data()
        self.channel_aliases = self.channel_alias_table.get_info()
        # check if any instrument alias is repeated, either in the instrument aliases or in the channel aliases
        combined_aliases = (
            self.instrument_aliases["Alias"] + self.channel_aliases["Alias"]
        )
        if alias := has_duplicates(combined_aliases):
            WarnPopup(
                self,
                f'The alias "{alias}" is repeated in the instrument or channel aliases!',
                "Repeated alias!",
            )
            return
        if instrument := has_duplicates(self.instrument_aliases["Instrument"]):
            WarnPopup(
                self,
                f'The instrument "{instrument}" is repeated in the instrument aliases!',
                "Repeated instrument!",
            )
            return
        # check if any instrument alias is empty
        if "" in self.instrument_aliases["Instrument"]:
            WarnPopup(
                self,
                "An instrument alias is empty!",
                "Empty instrument alias!",
            )
            return
        # check if an instrument gets an alias that is also an instrument
        if set(self.instrument_aliases["Instrument"]) & set(
            self.instrument_aliases["Alias"]
        ):
            WarnPopup(
                self,
                "An instrument alias is the same as an instrument name!",
                "Alias is an instrument!",
            )
            return
        # check if any channel has an alias that belongs to an instrument which also has an alias
        for channel in self.channel_aliases["channel"]:
            instr = variables_handling.channels[channel].device
            if instr in self.instrument_aliases["Instrument"]:
                WarnPopup(
                    self,
                    f'The instrument "{instr}" has an alias and the channel "{channel}" has an alias, a channel can only have an alias if its instrument does not!',
                    "Alias conflict!",
                )
                return
        super().accept()


def has_duplicates(lst):
    seen = set()
    for item in lst:
        if item in seen:
            return item
        seen.add(item)
    return False
