from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QTabWidget,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from copy import deepcopy

from nomad_camels.frontpanels import instrument_installer, instrument_config


class ManageInstruments(QDialog):
    """ """

    def __init__(self, active_instruments=None, parent=None):
        super().__init__(parent=parent)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        self.setWindowTitle("Manage Instruments - NOMAD CAMELS")
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)

        self.active_instruments = active_instruments or {}

        layout = QGridLayout()
        self.setLayout(layout)

        self.tabs = QTabWidget()

        self.installer = instrument_installer.Instrument_Installer()
        self.tabs.addTab(self.installer, "Install Instruments")

        self.config_widget = instrument_config.Instrument_Config(
            dict(self.active_instruments)
        )
        self.tabs.addTab(self.config_widget, "Configure Instruments")

        self.installer.instruments_updated.connect(self.config_widget.build_table)

        layout.addWidget(self.tabs, 0, 0)
        layout.addWidget(self.buttonBox, 1, 0)

        self.show()
        settab = 1 if instrument_installer.getInstalledDevices() else 0
        self.tabs.setCurrentIndex(settab)
        if not self.installer.all_devs:
            self.tabs.setTabEnabled(0, False)
            self.tabs.setTabToolTip(
                0,
                'Could not reach the server for list of drivers\ncheck your internet connection and try opening "Manage Instruments" again',
            )
        self.resize(1000, 700)

    def accept(self) -> None:
        """ """
        self.active_instruments = self.config_widget.get_config()
        super().accept()

    def reject(self):
        discard_dialog = QMessageBox.question(
            self,
            "Discard Changes?",
            f"All changes to instrument configurations will be lost!",
            QMessageBox.Yes | QMessageBox.No,
        )
        if discard_dialog == QMessageBox.Yes:
            self.config_widget.remove_temp_custom_names()
            return super().reject()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """Overwrites the keyPressEvent of the QDialog so that it does
        not close when pressing Enter/Return.

        Parameters
        ----------
        a0: QKeyEvent :


        Returns
        -------

        """
        if a0.key() == Qt.Key_Enter or a0.key() == Qt.Key_Return:
            return
        super().keyPressEvent(a0)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    widge = ManageInstruments()
    widge.show()
    app.exec()
