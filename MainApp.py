from sys import argv, excepthook

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUiType

from utility import exception_hook

QMainWindow, Ui_MainWindow = loadUiType('gui/mainWindow.ui')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('CECS - Configurable Experimental Control System')
        self.setWindowIcon(QIcon('graphics/FAIRmat_S.png'))




if __name__ == '__main__':
    excepthook = exception_hook.exception_hook
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(argv)
    ui = MainWindow()
    # ui.showMaximized()
    ui.show()

    app.exec()
