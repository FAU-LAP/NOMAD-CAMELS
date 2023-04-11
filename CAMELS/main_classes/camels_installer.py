import sys
import os

from PySide6.QtWidgets import QMainWindow, QApplication, QLabel
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon, QPixmap
from CAMELS.gui.installer_window import Ui_InstallerWindow

class InstallerWindow(QMainWindow, Ui_InstallerWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('CAMELS Installer')
        self.setWindowIcon(QIcon('../graphics/CAMELS.svg'))
        image = QPixmap()
        image.load('../graphics/CAMELS_Logo.png')
        self.image_label = QLabel()
        self.image_label.setPixmap(image)
        self.centralwidget.layout().addWidget(self.image_label, 0, 0, 4, 1)

        self.radioButton_full.clicked.connect(self.install_type_change)
        self.radioButton_custom.clicked.connect(self.install_type_change)
        self.install_type_change()

        self.pushButton_cancel.clicked.connect(self.close)
        self.pathButton_CAMELS.set_path(os.path.join(os.path.expanduser('~'), 'CAMELS'))
        # self.checkBox_wsl.clicked.connect(self.install_wsl_change)

        self.groupBox_progress.setHidden(True)
        self.resize(self.minimumSizeHint())

    def install_wsl_change(self):
        wsl = self.checkBox_wsl.isChecked()
        self.checkBox_epics.setEnabled(wsl)

    def install_type_change(self):
        full = self.radioButton_full.isChecked()
        self.groupBox_custom_install.setHidden(full)
        self.resize(self.minimumSizeHint())




if __name__ == '__main__':
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ui = InstallerWindow()
    ui.show()
    app.exec()