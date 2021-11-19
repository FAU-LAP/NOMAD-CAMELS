import pickle

from gui.taskSelector import Ui_TaskSelector
from gui.createTask import Ui_CreateTask
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from os.path import isdir
from os import makedirs, getenv, listdir

class TaskSelector(QDialog, Ui_TaskSelector):
    def __init__(self, parent=None):
        super(TaskSelector, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Select Task - CECS')
        self.setWindowIcon(QIcon('graphics/FAIRmat_S.png'))
        self.cancelButton.clicked.connect(self.close)
        self.okButton.clicked.connect(self.select_task)
        self.newTaskButton.clicked.connect(self.create_task)
        self.value = None
        self.find_tasks()

    def select_task(self):
        self.value = 'pass'
        self.close()

    def find_tasks(self):
        task_path = f'{getenv("LOCALAPPDATA")}/CECS/Tasks/'
        if isdir(task_path):
            self.taskSelectComboBox.clear()
            tasks = listdir(task_path)
            if 'Backup' not in tasks:
                makedirs(task_path + 'Backup')
            self.okButton.setEnabled(False)
            for task in tasks:
                if task.endswith('.task'):
                    self.okButton.setEnabled(True)
                    self.taskSelectComboBox.addItem(task[:-5])
        else:
            makedirs(task_path)
            self.find_tasks()

    def create_task(self):
        creator = CreateTask(self)
        creator.exec_()
        self.find_tasks()


class CreateTask(QDialog, Ui_CreateTask):
    def __init__(self, parent=None):
        super(CreateTask, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Create Task - CECS')

    def accept(self) -> None:
        name = self.lineEdit_taskName.text()
        task_path = f'{getenv("LOCALAPPDATA")}/CECS/Tasks/{name}'
        makedirs(task_path)
        super().accept()

