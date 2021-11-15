from sys import argv, excepthook

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QGridLayout, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUiType

from utility import exception_hook

QMainWindow, Ui_MainWindow = loadUiType('gui/mainWindow.ui')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowTitle('CECS - Configurable Experimental Control System')
        # self.setWindowIcon(QIcon('graphics/FAIRmat_S.png'))
        #
        # centralWidget = QWidget(parent=self)
        # toolBar = self.addToolBar('toolBar')
        # self.toolBar = toolBar
        # toolBar.setMovable(False)
        # toolBar.addAction('Task')
        # toolBar.addAction('Add-Ons')
        # toolBar.addAction('Devices')
        # toolBar.addAction('Preferences')
        # toolBar.addAction('Help')
        #
        # layout = QGridLayout(self)
        # centralWidget.setLayout(layout)
        # self.setCentralWidget(centralWidget)
        # layout.addWidget(QPushButton('Add-Ons'))
        # layout.addWidget(QPushButton('Devices'))





if __name__ == '__main__':
    excepthook = exception_hook.exception_hook
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(argv)
    ui = MainWindow()
    # ui.showMaximized()
    ui.show()

    app.exec()
