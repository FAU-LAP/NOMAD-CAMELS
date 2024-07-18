from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QComboBox, QCheckBox

from nomad_camels.main_classes.loop_step import Loop_Step_Config, Loop_Step
from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box

wait_types = ["simple wait", "wait with progress bar", "wait for condition"]


class Wait_Loop_Step(Loop_Step):
    """
    A loopstep to simply wait some defined time.

    Attributes
    ----------
    wait_time : str, float
        The how long the protocol execution should pause in seconds.
    """

    def __init__(self, name="", parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = "Wait"
        if step_info is None:
            step_info = {}
        self.wait_time = step_info["wait_time"] if "wait_time" in step_info else 0.0
        self.wait_type = (
            step_info["wait_type"] if "wait_type" in step_info else "simple wait"
        )
        self.skipable = step_info["skipable"] if "skipable" in step_info else True

    def get_add_main_string(self):
        add_main_string = super().get_add_main_string()
        if self.wait_type == "wait with progress bar":
            add_main_string += f'\tboxes["bar_{self.name}"] = helper_functions.Waiting_Bar(title="{self.name} waiting...", skipable={self.skipable}, with_timer=True)\n'
        return add_main_string

    def get_protocol_string(self, n_tabs=1):
        """The protocol just calls `bps.wait(`wait_time`)`, where `wait_time` is
        evaluated by the protocol's evaluator."""
        tabs = "\t" * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        if self.wait_type == "simple wait":
            protocol_string += (
                f'{tabs}yield from bps.sleep(eva.eval("{self.wait_time}"))\n'
            )
        if self.wait_type == "wait with progress bar":
            protocol_string += f'{tabs}boxes["bar_{self.name}"].skip = False\n'
            protocol_string += (
                f'{tabs}boxes["bar_{self.name}"].helper.executor.emit()\n'
            )
            protocol_string += (
                f"{tabs}bar_{self.name}_delta_t = eva.eval('{self.wait_time} / 100')\n"
            )
            protocol_string += f'{tabs}boxes["bar_{self.name}"].setter.set_wait_time(eva.eval("{self.wait_time}"))\n'
            protocol_string += f'{tabs}while not boxes["bar_{self.name}"].skip and not boxes["bar_{self.name}"].setter.timer > eva.eval("{self.wait_time}"):\n'
            protocol_string += (
                f"{tabs}\tyield from bps.sleep(bar_{self.name}_delta_t)\n"
            )
            protocol_string += (
                f'{tabs}\tboxes["bar_{self.name}"].setter.update_timer()\n'
            )
            protocol_string += (
                f'{tabs}boxes["bar_{self.name}"].setter.hide_signal.emit()\n'
            )
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """Tells the wait time."""
        short_string = super().get_protocol_short_string(n_tabs)
        short_string = f"{short_string[:-1]} - {self.wait_time} s\n"
        return short_string


class Wait_Loop_Step_Config(Loop_Step_Config):
    """The configuration just provides a line to enter the time to wait."""

    def __init__(self, loop_step: Wait_Loop_Step, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = Wait_Loop_Step_Config_Sub(loop_step, self)
        self.layout().addWidget(self.sub_widget, 1, 0)

    def update_step_config(self):
        """ """
        super().update_step_config()
        self.loop_step.wait_time = self.sub_widget.lineEdit_duration.text()
        self.loop_step.wait_type = self.sub_widget.comboBox_type.currentText()
        self.loop_step.skipable = self.sub_widget.checkbox_skipable.isChecked()


class Wait_Loop_Step_Config_Sub(QWidget):
    """The QLineEdit and labels to make everything clear are provided."""

    def __init__(self, loop_step: Wait_Loop_Step, parent=None):
        super().__init__(parent)
        self.loop_step = loop_step

        label_type = QLabel("Wait type")
        self.comboBox_type = QComboBox(self)
        self.comboBox_type.addItems(wait_types)
        self.comboBox_type.setCurrentText(loop_step.wait_type)
        self.comboBox_type.currentTextChanged.connect(self.type_changed)

        label1 = QLabel("Wait for")
        label2 = QLabel("seconds")
        self.lineEdit_duration = Variable_Box(self)
        self.lineEdit_duration.setText(str(loop_step.wait_time))
        self.lineEdit_duration.textChanged.connect(self.update_duration)

        self.checkbox_skipable = QCheckBox("skipable")
        self.checkbox_skipable.setChecked(loop_step.skipable)
        self.checkbox_skipable.setToolTip("The progress bar has a skip button.")

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label_type, 0, 0)
        layout.addWidget(self.comboBox_type, 0, 1, 1, 2)
        layout.addWidget(label1, 1, 0)
        layout.addWidget(self.lineEdit_duration, 1, 1)
        layout.addWidget(label2, 1, 2)
        layout.addWidget(self.checkbox_skipable, 2, 0, 1, 3)
        self.setLayout(layout)
        self.type_changed()

    def update_duration(self):
        """ """
        self.loop_step.wait_time = self.lineEdit_duration.text()

    def type_changed(self):
        """ """
        wait_type = self.comboBox_type.currentText()
        if wait_type == "simple wait":
            self.checkbox_skipable.setHidden(True)
        elif wait_type == "wait with progress bar":
            self.checkbox_skipable.setHidden(False)
