from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QTabWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QKeyEvent

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

        self.setWindowTitle('Manage Instruments - CAMELS')

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
        self.installer.instruments_updated.connect(self.config_widget.build_table)

        layout.addWidget(self.tabs, 0, 0)
        layout.addWidget(self.buttonBox, 1, 0)

    def accept(self) -> None:
        self.active_instruments = self.config_widget.get_config()
        super().accept()

    def closeEvent(self, a0: QCloseEvent) -> None:
        discard_dialog = QMessageBox.question(self, 'Discard Changes?',
                                              f'All changes to instrument configurations will be lost!',
                                              QMessageBox.Yes | QMessageBox.No)
        if discard_dialog != QMessageBox.Yes:
            a0.ignore()
            return
        super().closeEvent(a0)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """Overwrites the keyPressEvent of the QDialog so that it does
        not close when pressing Enter/Return."""
        if a0.key() == Qt.Key_Enter or a0.key() == Qt.Key_Return:
            return
        super().keyPressEvent(a0)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])

    widge = ManageInstruments()
    widge.show()
    app.exec_()
