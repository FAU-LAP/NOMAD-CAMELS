from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from CAMELS.main_classes.loop_step import Loop_Step_Config, Loop_Step
from CAMELS.ui_widgets.variable_tool_tip_box import Variable_Box

class Wait_Loop_Step(Loop_Step):
    """A loopstep to simply wait some defined time.

    Attributes
    ----------
    wait_time : float
        The time (in seconds) for how long to wait.
    """
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = 'Wait'
        if step_info is None:
            step_info = {}
        self.wait_time = step_info['wait_time'] if 'wait_time' in step_info else 0.0

    def get_protocol_string(self, n_tabs=1):
        """The protocol just calls `bps.wait(`wait_time`)`."""
        tabs = '\t' * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        protocol_string += f'{tabs}yield from bps.sleep(eva.eval("{self.wait_time}"))\n'
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        short_string = super().get_protocol_short_string(n_tabs)
        short_string = f'{short_string[:-1]} - {self.wait_time} s\n'
        return short_string


class Wait_Loop_Step_Config(Loop_Step_Config):
    """The configuration just provides a line to enter the time to wait."""
    def __init__(self, loop_step:Wait_Loop_Step, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = Wait_Loop_Step_Config_Sub(loop_step, self)
        self.layout().addWidget(self.sub_widget, 1, 0)


class Wait_Loop_Step_Config_Sub(QWidget):
    """The QLineEdit and labels to make everything clear are provided."""
    def __init__(self, loop_step:Wait_Loop_Step, parent=None):
        super().__init__(parent)
        self.loop_step = loop_step

        label1 = QLabel('Wait for')
        label2 = QLabel('seconds')
        self.lineEdit_duration = Variable_Box(self)
        self.lineEdit_duration.setText(str(loop_step.wait_time))
        self.lineEdit_duration.textChanged.connect(self.update_duration)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.lineEdit_duration, 0, 1)
        layout.addWidget(label2, 0, 2)
        self.setLayout(layout)

    def update_duration(self):
        self.loop_step.wait_time = self.lineEdit_duration.text()

