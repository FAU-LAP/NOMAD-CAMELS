from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QLineEdit, QTextEdit,\
    QComboBox

from nomad_camels.main_classes.loop_step import Loop_Step, Loop_Step_Config

class Prompt_Loop_Step(Loop_Step):
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = 'Prompt'
        if step_info is None:
            step_info = {}
        self.short_text = step_info['short_text'] if 'short_text' in step_info else ''
        self.long_text = step_info['long_text'] if 'long_text' in step_info else ''
        self.icon = step_info['icon'] if 'icon' in step_info else 'Info'

    def get_protocol_string(self, n_tabs=1):
        tabs = '\t' * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        protocol_string += f'{tabs}boxes["prompt_{self.name}"].done = False\n'
        protocol_string += f'{tabs}boxes["prompt_{self.name}"].helper.executor.emit()\n'
        protocol_string += f'{tabs}while not boxes["prompt_{self.name}"].done:\n'
        protocol_string += f'{tabs}\tyield from bps.sleep(0.1)\n'
        return protocol_string

    def get_add_main_string(self):
        long_text = self.long_text.replace("\n", "\\n")
        add_main_string = super().get_add_main_string()
        add_main_string += f'\tboxes["prompt_{self.name}"] = helper_functions.Prompt_Box("{self.icon}", "{long_text}", "{self.short_text}")\n'
        return add_main_string


class Prompt_Loop_Step_Config(Loop_Step_Config):
    def __init__(self, loop_step:Prompt_Loop_Step, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = Prompt_Loop_Step_Config_Sub(loop_step, self)
        self.layout().addWidget(self.sub_widget, 1, 0, 1, 5)


class Prompt_Loop_Step_Config_Sub(QWidget):
    """The QLineEdit and labels to make everything clear are provided."""
    def __init__(self, loop_step:Prompt_Loop_Step, parent=None):
        super().__init__(parent)
        self.loop_step = loop_step

        label1 = QLabel('Title:')
        label2 = QLabel('Text:')
        label3 = QLabel('Icon:')
        self.lineEdit_short = QLineEdit(self)
        self.lineEdit_short.setText(loop_step.short_text)
        self.lineEdit_short.textChanged.connect(self.update_info)

        self.textEdit_long = QTextEdit(self)
        self.textEdit_long.setText(loop_step.long_text)
        self.textEdit_long.textChanged.connect(self.update_info)

        self.comboBox_icon = QComboBox()
        icons = ['Information', 'Warning', 'Critical']
        self.comboBox_icon.addItems(icons)
        self.comboBox_icon.setCurrentText(loop_step.icon)
        self.comboBox_icon.currentTextChanged.connect(self.update_info)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label3, 0, 0)
        layout.addWidget(self.comboBox_icon, 0, 1)
        layout.addWidget(label1, 1, 0)
        layout.addWidget(self.lineEdit_short, 1, 1)
        layout.addWidget(label2, 2, 0)
        layout.addWidget(self.textEdit_long, 2, 1)
        self.setLayout(layout)

    def update_info(self):
        self.loop_step.short_text = self.lineEdit_short.text()
        self.loop_step.long_text = self.textEdit_long.toPlainText()
        self.loop_step.icon = self.comboBox_icon.currentText()