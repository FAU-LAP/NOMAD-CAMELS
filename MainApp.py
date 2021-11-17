from sys import argv, excepthook

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

from utility import exception_hook
from gui.mainWindow import Ui_MainWindow
from frontpanels import taskSelector


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, task, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('CECS - Configurable Experimental Control System')
        self.setWindowIcon(QIcon('graphics/FAIRmat_S.png'))
        # taskSel = taskSelector.TaskSelector(self)
        # taskSel.exec_()
        # self.task = taskSel.value



if __name__ == '__main__':
    excepthook = exception_hook.exception_hook
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(argv)
    # ui.showMaximized()
    # ui.show()
    taskerSel = taskSelector.TaskSelector()
    taskerSel.exec_()
    task_choice = taskerSel.value
    if task_choice is not None:
        ui = MainWindow(task_choice)
        ui.show()
        app.exec_()
