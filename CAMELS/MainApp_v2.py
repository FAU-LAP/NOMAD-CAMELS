import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

from CAMELS.gui.mainWindow_v2 import Ui_MainWindow
from CAMELS.utility import exception_hook

from pkg_resources import resource_filename



class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window for the program. Connects to all the other classes."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('CAMELS - Configurable Application for Measurements, Experiments and Laboratory-Systems')
        self.setWindowIcon(QIcon(resource_filename('CAMELS','graphics/CAMELS_Icon_v2.ico')))

        self.available_instruments = {}




if __name__ == '__main__':
    sys.excepthook = exception_hook.exception_hook
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    # RE = RunEngine()
    # ui.run_engine = RE
    app.exec_()