from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QCheckBox,
)

from nomad_camels.main_classes.loop_step import Loop_Step, Loop_Step_Config


class Prompt_Loop_Step(Loop_Step):
    """
    This step displays a prompt (QMessageBox) at runtime and pauses the
    execution of the protocol until the user clicks "ok" in the prompt. This may
    be used for example to prompt the user to do something at the setup.

    Attributes
    ----------
    short_test : str
        This will be the window title of the prompt.
    long_test : str
        This will be the full text, displayed inside the window.
    icon : str
        If 'Error', the `QMessagebox.Critical` icon is displayed, if 'Warning',
        then `QMessagebox.Warning` is used, otherwise `QMessagebox.Information`.
    """

    def __init__(self, name="", parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = "Prompt"
        if step_info is None:
            step_info = {}
        self.short_text = step_info["short_text"] if "short_text" in step_info else ""
        self.long_text = step_info["long_text"] if "long_text" in step_info else ""
        self.icon = step_info["icon"] if "icon" in step_info else "Info"
        self.abortable = step_info["abortable"] if "abortable" in step_info else False

    def get_protocol_string(self, n_tabs=1):
        """Sets the prompt's `done_flag` to False, then starts execution of the
        prompt and waits until it is done_flag."""
        tabs = "\t" * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        protocol_string += f'{tabs}boxes["prompt_{self.name}"].done_flag = False\n'
        protocol_string += f'{tabs}boxes["prompt_{self.name}"].helper.executor.emit()\n'
        protocol_string += f'{tabs}while not boxes["prompt_{self.name}"].done_flag:\n'
        protocol_string += f"{tabs}\tyield from bps.sleep(0.1)\n"
        if self.abortable:
            protocol_string += f'{tabs}\tif boxes["prompt_{self.name}"].abort_flag:\n'
            protocol_string += f"{tabs}\t\treturn\n"
        return protocol_string

    def get_add_main_string(self):
        """Adds the setup of the box to the `steps_add_main` function of the
        protocol."""
        long_text = self.long_text.replace("\n", "\\n").replace('"', '\\"')
        short_text = self.short_text.replace('"', '\\"').replace("\n", "\\n")
        add_main_string = super().get_add_main_string()
        add_main_string += f'\tboxes["prompt_{self.name}"] = helper_functions.Prompt_Box("{self.icon}", "{long_text}", "{short_text}", abortable={self.abortable})\n'
        return add_main_string


class Prompt_Loop_Step_Config(Loop_Step_Config):
    """ """

    def __init__(self, loop_step: Prompt_Loop_Step, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = Prompt_Loop_Step_Config_Sub(loop_step, self)
        self.layout().addWidget(self.sub_widget, 1, 0, 1, 5)


class Prompt_Loop_Step_Config_Sub(QWidget):
    """The QLineEdit and labels to make everything clear are provided."""

    def __init__(self, loop_step: Prompt_Loop_Step, parent=None):
        super().__init__(parent)
        self.loop_step = loop_step

        label1 = QLabel("Title:")
        label2 = QLabel("Text:")
        label3 = QLabel("Icon:")
        self.lineEdit_short = QLineEdit(self)
        self.lineEdit_short.setText(loop_step.short_text)
        self.lineEdit_short.textChanged.connect(self.update_info)

        self.textEdit_long = QTextEdit(self)
        self.textEdit_long.setText(loop_step.long_text)
        self.textEdit_long.textChanged.connect(self.update_info)

        self.comboBox_icon = QComboBox()
        icons = ["Information", "Warning", "Critical"]
        self.comboBox_icon.addItems(icons)
        self.comboBox_icon.setCurrentText(loop_step.icon)
        self.comboBox_icon.currentTextChanged.connect(self.update_info)

        self.checkBox_abortable = QCheckBox("can abort protocol")
        self.checkBox_abortable.setChecked(loop_step.abortable)
        self.checkBox_abortable.stateChanged.connect(self.update_info)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label3, 0, 0)
        layout.addWidget(self.comboBox_icon, 0, 1)
        layout.addWidget(self.checkBox_abortable, 1, 0, 1, 2)
        layout.addWidget(label1, 2, 0)
        layout.addWidget(self.lineEdit_short, 2, 1)
        layout.addWidget(label2, 3, 0)
        layout.addWidget(self.textEdit_long, 3, 1)
        self.setLayout(layout)

    def update_info(self):
        """ """
        self.loop_step.short_text = self.lineEdit_short.text()
        self.loop_step.long_text = self.textEdit_long.toPlainText()
        self.loop_step.icon = self.comboBox_icon.currentText()
        self.loop_step.abortable = self.checkBox_abortable.isChecked()
