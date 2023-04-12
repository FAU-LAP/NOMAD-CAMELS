from CAMELS.gui.taskSelector import Ui_TaskSelector
from CAMELS.frontpanels.helper_panels.enterTextDialog import EnterTextDialog
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QIcon
from os import getenv
from CAMELS.utility.load_save_functions import get_task_list


class TaskSelector(QDialog, Ui_TaskSelector):
    """Window that shows in the beginning to select a task.
    Use the ".value" attribute to read out the selected task."""
    def __init__(self, parent=None):
        super(TaskSelector, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Select Task - CAMELS')
        self.setWindowIcon(QIcon('graphics/FAIRmat_S.png'))
        self.cancelButton.clicked.connect(self.close)
        self.okButton.clicked.connect(self.select_task)
        self.newTaskButton.clicked.connect(self.create_task)
        self.value = None
        self.find_tasks()

    def select_task(self):
        """Called when clicking the "OK"-Button. Sets self.value to the selected task of the comboBox."""
        self.value = self.taskSelectComboBox.currentText()
        self.close()

    def find_tasks(self):
        """Reads a list of all available tasks and adds them to the comboBox."""
        tasks = get_task_list()
        self.taskSelectComboBox.clear()
        if tasks:
            self.okButton.setEnabled(True)
            for task in tasks:
                self.taskSelectComboBox.addItem(task)
        else:
            self.okButton.setEnabled(False)

    def create_task(self):
        """Creates a new empty task file."""
        text_dialog = EnterTextDialog(self, 'Create Task - CAMELS', 'Task name:')
        text_dialog.exec()
        name = text_dialog.value
        if name is not None:
            task_path = f'{getenv("LOCALAPPDATA")}/CAMELS/Tasks/'
            f = open(task_path + name + '.task', 'x')
            f.close()
        self.find_tasks()
