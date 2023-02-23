from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QTabWidget
from PyQt5.QtCore import Qt

from CAMELS.frontpanels import instrument_installer, instrument_config


class ManageInstruments(QDialog):
    def __init__(self, active_instruments=None, parent=None):
        super().__init__(parent=parent)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        self.active_instruments = active_instruments or {}

        layout = QGridLayout()
        self.setLayout(layout)

        self.tabs = QTabWidget()

        self.installer = instrument_installer.Instrument_Installer()
        self.tabs.addTab(self.installer, 'Install Instruments')

        self.config_widget = instrument_config.Instrument_Config(active_instruments)
        self.tabs.addTab(self.config_widget, 'Configure Instruments')

        settab = 1 if instrument_installer.getInstalledDevices() else 0
        self.tabs.setCurrentIndex(settab)

        layout.addWidget(self.tabs, 0, 0)
        layout.addWidget(self.buttonBox, 1, 0)

    def accept(self) -> None:
        self.active_instruments = self.config_widget.get_config()
        super().accept()



if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])

    widge = ManageInstruments()
    widge.show()
    app.exec_()
