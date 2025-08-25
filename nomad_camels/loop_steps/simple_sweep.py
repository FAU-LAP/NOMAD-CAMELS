from PySide6.QtWidgets import QComboBox, QLabel, QCheckBox
from PySide6.QtGui import QFont

from nomad_camels.main_classes.loop_step import Loop_Step_Config
from nomad_camels.utility import variables_handling
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table
from nomad_camels.utility.load_save_helper_functions import load_plots
from nomad_camels.bluesky_handling import builder_helper_functions
from nomad_camels.frontpanels.plot_definer import Plot_Button_Overview

from nomad_camels.loop_steps.for_while_loops import (
    For_Loop_Step_Config_Sub,
    For_Loop_Step,
)


class Simple_Sweep(For_Loop_Step):
    """
    A sweep over a single channel reading arbitrary other channels. The
    information about which values to sweep through are inherited from
    For_Loop_Step.

    Attributes
    ----------
    sweep_channel : str
        The name of the channel that should be sweeped.
    data_output : str
        Whether the data is put into its own stream('sub-stream') or the primary
        stream ('main-stream').
    plots : list[Plot_Info]
        List of the plots that should be created for the sweep.
    read_channels : list[str]
        List of the channels that should be read during the sweep.
    """

    def __init__(
        self, name="", children=None, parent_step=None, step_info=None, **kwargs
    ):
        super().__init__(name, children, parent_step, step_info, **kwargs)
        step_info = step_info or {}
        self.step_type = "Simple Sweep"
        self.has_children = False
        self.sweep_channel = (
            step_info["sweep_channel"] if "sweep_channel" in step_info else ""
        )
        self.data_output = (
            step_info["data_output"] if "data_output" in step_info else "sub-stream"
        )
        self.plots = load_plots([], step_info["plots"]) if "plots" in step_info else []
        self.read_channels = (
            step_info["read_channels"] if "read_channels" in step_info else []
        )
        if "skip_failed" in step_info:
            self.skip_failed = step_info["skip_failed"]
        else:
            self.skip_failed = [False] * len(self.read_channels)

    def update_used_devices(self):
        """Includes the devices from the read_channels and the sweep_channel."""
        self.used_devices = []
        channels = variables_handling.get_channels()
        set_device = channels[self.sweep_channel].device
        self.used_devices.append(set_device)
        for channel in self.read_channels:
            if channel in channels:
                device = channels[channel].device
                if device not in self.used_devices:
                    self.used_devices.append(device)

    def get_used_channels(self):
        """Returns a list of all used channels in this step, including
        the sweep_channel and the read_channels."""
        used_channels = [self.sweep_channel] + self.read_channels
        return list(set(used_channels))

    def update_variables(self):
        """Adds the fit variables from the plots."""
        variables = {}
        stream = f"{self.name}"
        for plot in self.plots:
            variables.update(plot.get_fit_vars(stream))
        variables_handling.loop_step_variables.update(variables)
        super().update_variables()

    def get_outer_string(self):
        """Gives the string to create the plots of the sweeps"""
        if self.plots:
            return builder_helper_functions.plot_creator(
                self.plots, f"create_plots_{self.name}"
            )[0]
        return ""

    def get_add_main_string(self):
        """Calling the plot_creator from steps_add_main"""
        stream = f'"{self.name}"'
        if self.data_output == "main stream":
            stream = '"primary"'
        add_main_string = ""
        if self.plots:
            add_main_string += builder_helper_functions.get_plot_add_string(
                self.name, stream
            )
        return add_main_string

    def get_protocol_string(self, n_tabs=1):
        """The channels to be read are set up. Then a for loop for the sweep is
        started, setting the channel, then reading."""
        tabs = "\t" * n_tabs

        stream = f'"{self.name}"'
        if variables_handling.preferences.get("nested_data", True):
            stream = (
                f'{stream} if stream_name == "primary" else f"{{stream_name}}||sub_stream||'
                + stream.replace('"', "")
                + '"'
            )
        if self.data_output == "main stream":
            stream = "stream_name"

        skip_failed = list(self.skip_failed)

        protocol_string = f"{tabs}channels = ["
        channels = variables_handling.get_channels()
        for i, channel in enumerate(self.read_channels):
            if channel not in channels:
                raise Exception(
                    f"Trying to read channel {channel} in {self.full_name}, but it does not exist!"
                )
            if i > 0:
                protocol_string += ", "
            name = channels[channel].name
            if "." in name:
                dev, chan = name.split(".")
                protocol_string += f'devs["{dev}"].{chan}'
            else:
                protocol_string += f'devs["{name}"]'
        protocol_string += "]\n"
        protocol_string += f"{tabs}helper_functions.clear_plots(plots, {stream})"
        protocol_string += super().get_protocol_string(n_tabs)
        name = channels[self.sweep_channel].name
        if "." in name:
            dev, chan = name.split(".")
            setter = f'devs["{dev}"].{chan}'
        else:
            setter = f'devs["{name}"]'

        protocol_string += f'{tabs}\tyield from bps.abs_set({setter}, {self.name.replace(" ", "_")}_Value, group="A")\n'
        protocol_string += f'{tabs}\tyield from bps.wait("A")\n'
        protocol_string += f"{tabs}\tyield from helper_functions.trigger_and_read(channels, name={stream}, skip_on_exception={skip_failed})\n"
        protocol_string += f"{tabs}yield from helper_functions.get_fit_results(all_fits, namespace, True, {stream})\n"
        self.update_time_weight()
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """The read and sweep channels and the sweep values are specified."""
        vals = super().get_protocol_short_string(n_tabs)[:-1].split(" for ")[-1]
        tabs = "\t" * n_tabs
        short_string = f"{tabs}Sweep '{self.name}' {self.sweep_channel}:\n{tabs}\tRead: {self.read_channels}\n{tabs}\tValues: {vals}"
        return short_string


class Simple_Sweep_Config(Loop_Step_Config):
    """ """

    def __init__(self, loop_step: Simple_Sweep, parent=None):
        super().__init__(parent, loop_step)
        self.loop_step = loop_step
        label_sweep_channel = QLabel("Sweep Channel:")
        out_box = []
        in_box = []
        channels = variables_handling.get_channels()
        for channel in channels:
            in_box.append(channel)
            if channels[channel].output:
                out_box.append(channel)
        self.comboBox_sweep_channel = QComboBox()
        self.comboBox_sweep_channel.addItems(out_box)
        if loop_step.sweep_channel in out_box:
            self.comboBox_sweep_channel.setCurrentText(loop_step.sweep_channel)

        label_data = QLabel("Data Output:")
        self.comboBox_data_output = QComboBox()
        output_types = ["sub-stream", "main stream", "own file"]
        self.comboBox_data_output.addItems(output_types)
        self.comboBox_data_output.setCurrentText(loop_step.data_output)

        self.sweep_widget = For_Loop_Step_Config_Sub(parent=self, loop_step=loop_step)
        labels = ["read?", "channel", "ignore failed"]
        info_dict = {
            "channel": self.loop_step.read_channels,
            "ignore failed": self.loop_step.skip_failed,
        }
        self.read_table = Channels_Check_Table(
            self, labels, info_dict=info_dict, title="Read-Channels", checkables=[2]
        )

        self.plot_widge = Plot_Button_Overview(self, self.loop_step.plots)

        # label_proc = QLabel('Data processing')
        font = QFont()
        font.setBold(True)

        # this hides the selection as only sub-stream works well
        self.comboBox_data_output.hide()
        label_data.hide()
        self.comboBox_data_output.setCurrentText("sub-stream")

        self.layout().addWidget(label_sweep_channel, 1, 0)
        self.layout().addWidget(self.comboBox_sweep_channel, 1, 1, 1, 4)
        self.layout().addWidget(label_data, 2, 0)
        self.layout().addWidget(self.comboBox_data_output, 2, 1, 1, 4)
        self.layout().addWidget(self.sweep_widget, 5, 0, 1, 5)
        self.layout().addWidget(self.read_table, 6, 0, 1, 5)

        self.layout().addWidget(self.plot_widge, 8, 0, 1, 5)

    def update_step_config(self):
        """ """
        super().update_step_config()
        # self.loop_step.use_own_plots = self.checkBox_use_own_plots.isChecked()
        self.loop_step.plots = self.plot_widge.plot_data
        # self.loop_step.plots = self.plot_table.update_table_data()
        info = self.read_table.get_info()
        self.loop_step.read_channels = info["channel"]
        self.loop_step.skip_failed = info["ignore failed"]
        self.loop_step.data_output = self.comboBox_data_output.currentText()
        self.loop_step.sweep_channel = self.comboBox_sweep_channel.currentText()
