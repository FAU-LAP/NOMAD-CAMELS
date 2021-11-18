from sys import argv, excepthook

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

from utility import exception_hook, load_save_functions
from gui.mainWindow import Ui_MainWindow
from frontpanels import taskSelector


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window for the program. Connects to all the other classes.

    - task: The task to load on initialisation"""
    def __init__(self, task: str, parent=None):
        # basic setup
        self.task = task
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('CECS - Configurable Experimental Control System')
        self.setWindowIcon(QIcon('graphics/FAIRmat_S.png'))

        tasklist = load_save_functions.get_task_list()
        for t in tasklist:
            self.comboBox_task.addItem(t)
        self.comboBox_task.setCurrentText(self.task)

        # connecting buttons
        self.pushButton_save_state.clicked.connect(self.save_state)
        self.pushButton_load_state.clicked.connect(self.load_state)

        self.load_state(self.task)

    def save_state(self):
        """Saves the current state in the .task file."""


    def load_state(self, task: str):
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
    # First select a task, then start the main window. If no task is selected, abort execution (avoids loading data etc.)
    task_sel = taskSelector.TaskSelector()
    task_sel.exec_()
    task_choice = task_sel.value
    if task_choice is not None:
        ui = MainWindow(task=task_choice)
        ui.show()
        app.exec_()
