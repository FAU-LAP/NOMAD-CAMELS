from PyQt5.QtWidgets import QLineEdit, QAction, QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem

from utility import variables_handling


class VariableItem(QStandardItem):
    def __init__(self, value=None):
        super().__init__(value)
        self.setToolTip('test')


class Variable_Box(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setToolTip('test')
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.textChanged.connect(self.check_string)
        self.check_string()

    def setEnabled(self, a0: bool) -> None:
        if a0:
            self.check_string()
        else:
            self.setStyleSheet('')
        super().setEnabled(a0)

    def check_string(self):
        if not self.text():
            self.setStyleSheet(f'background-color: rgb{variables_handling.get_color("white", True)}')
        if variables_handling.check_eval(self.text()):
            self.setStyleSheet(f'background-color: rgb{variables_handling.get_color("green", True)}')
        else:
            self.setStyleSheet(f'background-color: rgb{variables_handling.get_color("red", True)}')


    def context_menu(self, pos):
        menu = self.createStandardContextMenu()
        (channel_menu, variable_menu, operator_menu, function_menu), _ = variables_handling.get_menus(self.insert_variable)
        first_act = menu.actions()[0]
        menu.insertMenu(first_act, channel_menu)
        menu.insertMenu(first_act, variable_menu)
        menu.insertMenu(first_act, function_menu)
        menu.insertMenu(first_act, operator_menu)
        menu.insertSeparator(first_act)
        menu.exec_(self.mapToGlobal(pos))

    def insert_variable(self, variable):
        self.setText(self.text() + f'{variable}')

    def get_evaluation(self):
        return variables_handling.string_eval(self.text())
