from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QComboBox, QCheckBox

from nomad_camels.main_classes.loop_step import Loop_Step_Config, Loop_Step
from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table

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
        self.condition = step_info["condition"] if "condition" in step_info else ""
        self.read_channels = (
            step_info["read_channels"] if "read_channels" in step_info else []
        )

    def get_add_main_string(self):
        add_main_string = super().get_add_main_string()
        if self.wait_type == "wait with progress bar":
            add_main_string += f'\tboxes["bar_{self.name}"] = helper_functions.Waiting_Bar(title="{self.name} waiting...", skipable={self.skipable}, with_timer=True)\n'
        elif self.wait_type == "wait for condition":
            from nomad_camels.bluesky_handling import builder_helper_functions

            add_main_string += builder_helper_functions.get_plot_add_string(
                self.name, f'"{self.full_name}"'
            )
        return add_main_string

    def get_outer_string(self):
        outer_string = super().get_outer_string()
        if self.wait_type == "wait for condition":
            from nomad_camels.bluesky_handling import builder_helper_functions
            from nomad_camels.frontpanels.plot_definer import Plot_Info

            y_axes = [self.condition]
            for comparison in ["<=", ">=", "<", ">", "=="]:
                if comparison in self.condition:
                    y_axes += self.condition.split(comparison)
                    break
            plot_data = [
                Plot_Info(
                    "Value-List", title=self.full_name, y_axes={"formula": y_axes}
                )
            ]
            outer_string += builder_helper_functions.plot_creator(
                plot_data,
                f"create_plots_{self.name}",
                plot_is_box=True,
                box_names=f"bar_{self.name}",
                skip_box=self.skipable,
            )[0]
        return outer_string

    def update_used_devices(self):
        """All devices that should be read are added to the used_devices."""
        self.used_devices = []
        if not self.wait_type == "wait for condition":
            return
        from nomad_camels.utility import variables_handling

        for channel in variables_handling.channels:
            if channel in self.read_channels:
                device = variables_handling.channels[channel].device
                if device not in self.used_devices:
                    self.used_devices.append(device)

    def get_protocol_string(self, n_tabs=1):
        """The protocol just calls `bps.wait(`wait_time`)`, where `wait_time` is
        evaluated by the protocol's evaluator."""
        tabs = "\t" * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        if self.wait_type == "simple wait":
            protocol_string += (
                f'{tabs}yield from bps.sleep(eva.eval("{self.wait_time}"))\n'
            )
        elif self.wait_type == "wait with progress bar":
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
        elif self.wait_type == "wait for condition":
            protocol_string += self.get_channels_string(tabs)
            protocol_string += f"{tabs}yield from bps.trigger_and_read(channels_{self.variable_name()}, name='{self.full_name}')\n"
            protocol_string += (
                f'{tabs}boxes["bar_{self.name}_0"].helper.executor.emit()\n'
            )
            protocol_string += f'{tabs}while not eva.eval("{self.condition}") and not boxes["bar_{self.name}_0"].skip:\n'
            protocol_string += (
                f'{tabs}\tyield from bps.sleep(eva.eval("{self.wait_time}"))\n'
            )
            protocol_string += f"{tabs}\tyield from bps.trigger_and_read(channels_{self.variable_name()}, name='{self.full_name}')\n"
            protocol_string += (
                f'{tabs}boxes["bar_{self.name}_0"].setter.hide_signal.emit()\n'
            )
        return protocol_string

    def variable_name(self):
        """Returns the name of this step as a valid variable name, to specify
        the channels for this read."""
        from nomad_camels.utility import fit_variable_renaming

        return fit_variable_renaming.replace_name(self.name)

    def get_channels_string(self, tabs):
        """
        Gives a string of the channels that should be read. This may also be
        used by the Trigger_Channels step.

        Parameters
        ----------
        tabs : str
            A string including the tabs for intendation.
        """
        from nomad_camels.loop_steps.read_channels import get_channel_string

        channel_string = f"{tabs}channels_{self.variable_name()} = ["
        if not self.read_channels:
            return channel_string + "]\n"
        for channel in self.read_channels:
            channel_string += get_channel_string(channel)
        channel_string = channel_string[:-2] + "]\n"
        return channel_string

    def get_protocol_short_string(self, n_tabs=0):
        """Tells the wait time."""
        short_string = super().get_protocol_short_string(n_tabs)
        if self.wait_type != "wait for condition":
            short_string = f"{short_string[:-1]} - {self.wait_time} s\n"
        else:
            short_string = f"{short_string[:-1]} - '{self.condition}'\n"
        return short_string


class Wait_Loop_Step_Config(Loop_Step_Config):
    """The configuration just provides a line to enter the time to wait."""

    def __init__(self, loop_step: Wait_Loop_Step, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = Wait_Loop_Step_Config_Sub(loop_step, self)
        self.layout().addWidget(self.sub_widget, 1, 0, 1, 5)

    def update_step_config(self):
        """ """
        super().update_step_config()
        self.loop_step.wait_time = self.sub_widget.lineEdit_duration.text()
        self.loop_step.wait_type = self.sub_widget.comboBox_type.currentText()
        self.loop_step.skipable = self.sub_widget.checkbox_skipable.isChecked()
        self.loop_step.condition = self.sub_widget.condition_line.text()
        self.loop_step.read_channels = self.sub_widget.read_channels_table.get_info()[
            "channel"
        ]


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

        self.label1 = QLabel("Wait for")
        self.label2 = QLabel("seconds")
        self.lineEdit_duration = Variable_Box(self)
        self.lineEdit_duration.setText(str(loop_step.wait_time))
        self.lineEdit_duration.textChanged.connect(self.update_duration)

        self.checkbox_skipable = QCheckBox("skipable")
        self.checkbox_skipable.setChecked(loop_step.skipable)
        self.checkbox_skipable.setToolTip("The progress bar has a skip button.")

        self.label_condition = QLabel("Wait until:")
        self.condition_line = Variable_Box(self)
        self.condition_line.setText(loop_step.condition)
        self.condition_line.setToolTip("Wait until this condition is fulfilled.")

        info_dict = {"channel": loop_step.read_channels}
        self.read_channels_table = Channels_Check_Table(
            self,
            ["read?", "channel"],
            info_dict=info_dict,
            title="Read channels",
        )

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label_type, 0, 0)
        layout.addWidget(self.comboBox_type, 0, 1, 1, 2)
        layout.addWidget(self.label1, 1, 0)
        layout.addWidget(self.lineEdit_duration, 1, 1)
        layout.addWidget(self.label2, 1, 2)
        layout.addWidget(self.checkbox_skipable, 2, 0, 1, 3)
        layout.addWidget(self.label_condition, 3, 0)
        layout.addWidget(self.condition_line, 3, 1, 1, 2)
        layout.addWidget(self.read_channels_table, 4, 0, 1, 3)
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
        else:
            self.checkbox_skipable.setHidden(False)
        if wait_type == "wait for condition":
            self.read_channels_table.setHidden(False)
            self.condition_line.setHidden(False)
            self.label_condition.setHidden(False)
            self.label1.setText("read every")
        else:
            self.read_channels_table.setHidden(True)
            self.condition_line.setHidden(True)
            self.label_condition.setHidden(True)
            self.label1.setText("Wait for")
