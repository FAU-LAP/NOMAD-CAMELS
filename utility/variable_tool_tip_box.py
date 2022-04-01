from PyQt5.QtWidgets import QLineEdit, QAction, QMenu
from PyQt5.QtCore import Qt

from utility import variables_handling

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
        if variables_handling.check_eval(self.text()):
            self.setStyleSheet('background-color: rgb(0, 100, 0)')
        else:
            self.setStyleSheet('background-color: rgb(50, 0, 0)')


    def context_menu(self, pos):
        menu = self.createStandardContextMenu()
        variable_menu = QMenu('Insert Variable')
        channel_menu = QMenu('Insert Channel-Value')
        function_menu = QMenu('Insert Function')
        operator_menu = QMenu('Insert Operator')
        channel_actions = []
        operator_actions = []
        actions = []
        function_actions = []
        for channel in sorted(variables_handling.channels, key=lambda x: x.lower()):
            action = QAction(channel)
            action.triggered.connect(lambda state, x=channel: self.insert_variable(x))
            channel_actions.append(action)
        for variable in sorted(variables_handling.protocol_variables, key=lambda x: x.lower()):
            action = QAction(variable)
            action.triggered.connect(lambda state, x=variable: self.insert_variable(x))
            actions.append(action)
        for variable in sorted(variables_handling.loop_step_variables, key=lambda x: x.lower()):
            action = QAction(variable)
            action.triggered.connect(lambda state, x=variable: self.insert_variable(x))
            actions.append(action)
        for op in variables_handling.operator_names:
            action = QAction(f'{op}\t{variables_handling.operator_names[op]}')
            action.triggered.connect(lambda state, x=op: self.insert_variable(x))
            operator_actions.append(action)
        for foo in sorted(variables_handling.evaluation_functions_names, key=lambda x: x.lower()):
            action = QAction(variables_handling.evaluation_functions_names[foo])
            action.triggered.connect(lambda state, x=foo: self.insert_variable(x))
            function_actions.append(action)
        channel_menu.addActions(channel_actions)
        variable_menu.addActions(actions)
        operator_menu.addActions(operator_actions)
        function_menu.addActions(function_actions)
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
