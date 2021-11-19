from sys import argv, excepthook

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

from utility import exception_hook, load_save_functions
from gui.mainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window for the program. Connects to all the other classes.

    - task: The task to load on initialisation"""
    def __init__(self, parent=None):
        # basic setup
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('CECS - Configurable Experimental Control System')
        self.setWindowIcon(QIcon('graphics/FAIRmat_S.png'))

        self.load_state()

    def save_state(self):
        """Saves the current state in the .task file."""


    def load_state(self):
        """Loads a specific state of the provided task."""

    def close(self) -> bool:
        """Calling the save_state method when closing the window."""
        self.save_state()
        return super().close()


if __name__ == '__main__':
    excepthook = exception_hook.exception_hook
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(argv)
    ui = MainWindow()
    ui.show()
    ui.showMaximized()
    app.exec_()
