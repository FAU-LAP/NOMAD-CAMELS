from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QTabWidget,
    QPushButton,
    QWidget,
    QGridLayout,
    QLineEdit,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal

from nomad_camels.main_classes.loop_step import Loop_Step_Config, Loop_Step
from nomad_camels.utility import variables_handling
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table
from nomad_camels.utility.load_save_helper_functions import load_plots
from nomad_camels.bluesky_handling import builder_helper_functions
from nomad_camels.frontpanels.plot_definer import Plot_Button_Overview

from nomad_camels.loop_steps.for_while_loops import (
    For_Loop_Step_Config_Sub,
    For_Loop_Step,
)


class ND_Sweep(Loop_Step):
    """
    An n-dimensional sweep with the read values. Useful for e.g. an xy-scan.

    Attributes
    ----------
    sweep_channels : list[str]
        From outer to inner sweep, the names of the channels that should be
        sweeped through.
    data_output : str
        Whether the data is put into its own stream('sub-stream') or the primary
        stream ('main-stream').
    plots : list[Plot_Info]
        List of the plots that should be created for the sweep.
    read_channels : list[str]
        List of the channels that should be read during the sweep.
    sweep_values : list[Sweep_Step]
        List of sub-steps containing the information about the sweeps.
    """

    def __init__(self, name="", parent_step=None, step_info=None, **kwargs):
        super().__init__(
            name=name, parent_step=parent_step, step_info=step_info, **kwargs
        )
        step_info = step_info or {}
        self.step_type = "ND Sweep"
        self.has_children = False
        self.sweep_channels = (
            step_info["sweep_channels"] if "sweep_channels" in step_info else []
        )
        self.data_output = (
            step_info["data_output"] if "data_output" in step_info else "sub-stream"
        )
        self.plots = load_plots([], step_info["plots"]) if "plots" in step_info else []
        self.read_channels = (
            step_info["read_channels"] if "read_channels" in step_info else []
        )
        self.sweep_values = (
            step_info["sweep_values"] if "sweep_values" in step_info else []
        )

    def update_used_devices(self):
        """Includes the devices from the read_channels and the sweep_channels"""
        self.used_devices = []
        for channel in self.read_channels:
            if channel in variables_handling.channels:
                device = variables_handling.channels[channel].device
                if device not in self.used_devices:
                    self.used_devices.append(device)
        for channel in self.sweep_channels:
            if channel in variables_handling.channels:
                device = variables_handling.channels[channel].device
                if device not in self.used_devices:
                    self.used_devices.append(device)

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
        """The channels to be read are set up. Then a for loop for each sweep is
        started, with the channels each being set inside it."""
        tabs = "\t" * n_tabs

        stream = f'"{self.name}"'
        if self.data_output == "main stream":
            stream = "stream_name"

        protocol_string = super().get_protocol_string(n_tabs)
        protocol_string += f"{tabs}channels = ["
        for i, channel in enumerate(self.read_channels):
            if channel not in variables_handling.channels:
                raise Exception(
                    f"Trying to read channel {channel} in {self.full_name}, but it does not exist!"
                )
            if i > 0:
                protocol_string += ", "
            name = variables_handling.channels[channel].name
            if "." in name:
                dev, chan = name.split(".")
                protocol_string += f'devs["{dev}"].{chan}'
            else:
                protocol_string += f'devs["{name}"]'
        protocol_string += "]\n"
        protocol_string += f"{tabs}helper_functions.clear_plots(plots, {stream})"

        if not self.sweep_values:
            raise Exception(f"Trying to sweep nothing!\n{self.full_name}")
        i = 0
        for i, sweep in enumerate(self.sweep_values):
            if not isinstance(sweep, Sweep_Step):
                sweep = Sweep_Step(sweep)
            sweep.name = f"sub_step_{i}"
            sweep.update_full_name()
            protocol_string += sweep.get_protocol_string(n_tabs + i)

        tabs = "\t" * (n_tabs + i)
        protocol_string += f'{tabs}\tyield from bps.wait("A")\n'
        protocol_string += (
            f"{tabs}\tyield from bps.trigger_and_read(channels, name={stream})\n"
        )
        protocol_string += f"{tabs}yield from helper_functions.get_fit_results(all_fits, namespace, True, {stream})\n"
        self.update_time_weight()
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """The read channels and the sweeps are specified."""
        short_string = super().get_protocol_short_string(n_tabs)
        tabs = "\t" * (n_tabs + 1)
        short_string += f"{tabs}Read: {self.read_channels}\n"
        for i, channel in enumerate(self.sweep_channels):
            sweep = self.sweep_values[i]
            if not isinstance(sweep, Sweep_Step):
                sweep = Sweep_Step(sweep)
            short_string += f"{tabs}Sweep {i}: {channel}\n{tabs}Values {i}: {sweep.get_protocol_short_string()}\n"
        return short_string


class Sweep_Step(For_Loop_Step):
    """
    One single sweep for the ND sweep. Inherits from For_Loop_Step regarding the
    steps of the sweep.

    Attributes
    ----------
    sweep_channel : str
        The channel which is used in this sweep-part.
    wait_time : str, float
        The time in seconds, how long to wait after setting the channel.
    """

    def __init__(self, step_info=None):
        step_info = step_info or {}
        super().__init__(step_info=step_info)
        self.step_type = "ND Sweep Part"
        self.sweep_channel = (
            step_info["sweep_channel"] if "sweep_channel" in step_info else ""
        )
        self.wait_time = step_info["wait_time"] if "wait_time" in step_info else ""

    def get_protocol_string(self, n_tabs=1):
        """Creates a for loop over the sweep_channel and waits for wait_time
        after setting the channel."""
        tabs = "\t" * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        name = variables_handling.channels[self.sweep_channel].name
        if "." in name:
            dev, chan = name.split(".")
            setter = f'devs["{dev}"].{chan}'
        else:
            setter = f'devs["{name}"]'
        protocol_string += f'{tabs}\tyield from bps.abs_set({setter}, {self.name.replace(" ", "_")}_Value, group="A")\n'
        if self.wait_time:
            protocol_string += (
                f'{tabs}\tyield from bps.sleep(eva.eval("{self.wait_time}"))\n'
            )
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """Specifies the same way as the foor loop."""
        return super().get_protocol_short_string(n_tabs)[:-1].split(" for ")[-1]


class ND_Sweep_Config(Loop_Step_Config):
    """ """

    def __init__(self, loop_step: ND_Sweep, parent=None):
        super().__init__(parent, loop_step)
        self.loop_step = loop_step

        label_data = QLabel("Data Output:")
        font = QFont()
        font.setBold(True)
        label_data.setStyleSheet("font-size: 9pt")
        label_data.setFont(font)
        self.comboBox_data_output = QComboBox()
        output_types = ["sub-stream", "main stream", "own file"]
        self.comboBox_data_output.addItems(output_types)
        self.comboBox_data_output.setCurrentText(loop_step.data_output)

        labels = ["read", "channel"]
        info_dict = {"channel": self.loop_step.read_channels}
        self.read_table = Channels_Check_Table(
            self, labels, info_dict=info_dict, title="Read-Channels"
        )

        self.plot_widge = Plot_Button_Overview(self, self.loop_step.plots)

        self.addSweepChannelButton = QPushButton("Add sweep channel")
        self.addSweepChannelButton.clicked.connect(self.add_sweep_channel)

        self.tabs = []
        self.tab_widget = QTabWidget()
        for sweep in loop_step.sweep_values:
            self.add_sweep_channel(sweep)
        if not self.tabs:
            self.add_sweep_channel()

        self.layout().addWidget(self.plot_widge, 1, 0, 1, 5)
        self.layout().addWidget(label_data, 2, 0)
        self.layout().addWidget(self.comboBox_data_output, 2, 1, 1, 4)
        self.layout().addWidget(self.read_table, 6, 0, 1, 5)
        self.layout().addWidget(self.addSweepChannelButton, 10, 0, 1, 5)
        self.layout().addWidget(self.tab_widget, 11, 0, 1, 5)

    def remove_sweep_channel(self):
        """ """
        ind = self.tab_widget.currentIndex()
        self.tab_widget.removeTab(ind)
        self.tabs.pop(ind)
        self.change_tab_name()

    def add_sweep_channel(self, sweep_info=None):
        """

        Parameters
        ----------
        sweep_info :
             (Default value = None)

        Returns
        -------

        """
        if isinstance(sweep_info, Sweep_Step):
            sweep_step = sweep_info
        else:
            sweep_step = Sweep_Step(sweep_info)
        tab = Single_Sweep_Tab(sweep_step, self)
        tab.signal_change_sweep.connect(self.change_tab_name)
        tab.signal_remove.connect(self.remove_sweep_channel)
        tab.signal_move_left.connect(lambda: self.move_tab(-1))
        tab.signal_move_right.connect(lambda: self.move_tab(1))
        self.tabs.append(tab)
        self.tab_widget.addTab(tab, "")
        self.change_tab_name()

    def change_tab_name(self):
        """ """
        for i, tab in enumerate(self.tabs):
            if i == 0:
                pos = "outer"
            elif i == len(self.tabs) - 1:
                pos = "inner"
            else:
                pos = "mid"
            name = tab.get_name(pos)
            self.tab_widget.setTabText(i, name)

    def move_tab(self, direction=1):
        """

        Parameters
        ----------
        direction :
             (Default value = 1)

        Returns
        -------

        """
        ind = self.tab_widget.currentIndex()
        self.tab_widget.tabBar().moveTab(ind, ind + direction)
        self.tabs[ind + direction], self.tabs[ind] = (
            self.tabs[ind],
            self.tabs[ind + direction],
        )
        self.change_tab_name()

    def update_step_config(self):
        """ """
        self.loop_step.sweep_values = []
        self.loop_step.sweep_channels = []
        for tab in self.tabs:
            info = tab.get_info()
            chan = info.sweep_channel
            if chan in self.loop_step.sweep_channels:
                raise Exception(f"Can only scan same channel once in ND-sweep!\n{chan}")
            self.loop_step.sweep_channels.append(chan)
            self.loop_step.sweep_values.append(info)
        super().update_step_config()
        self.loop_step.plots = self.plot_widge.plot_data
        self.loop_step.read_channels = self.read_table.get_info()["channel"]
        self.loop_step.data_output = self.comboBox_data_output.currentText()


class Single_Sweep_Tab(QWidget):
    """ """

    signal_remove = Signal()
    signal_move_left = Signal()
    signal_move_right = Signal()
    signal_change_sweep = Signal(str)

    def __init__(self, loop_step: Sweep_Step, parent=None):
        super().__init__(parent)
        self.loop_step = loop_step
        label_sweep = QLabel("Sweep Channel:")
        out_channels = variables_handling.get_output_channels()
        self.comboBox_sweep_channel = QComboBox()
        self.comboBox_sweep_channel.addItems(out_channels)
        if loop_step.sweep_channel in out_channels:
            self.comboBox_sweep_channel.setCurrentText(loop_step.sweep_channel)
        self.comboBox_sweep_channel.currentTextChanged.connect(
            self.signal_change_sweep.emit
        )

        label_wait = QLabel("Wait after setting:")
        self.lineEdit_wait_time = QLineEdit("0")
        if loop_step.wait_time:
            self.lineEdit_wait_time.setText(loop_step.wait_time)

        self.sweep_widget = For_Loop_Step_Config_Sub(parent=self, loop_step=loop_step)

        self.moveLeftButton = QPushButton("Move left/out")
        self.moveRightButton = QPushButton("Move right/in")
        self.removeButton = QPushButton("Remove")

        self.moveRightButton.clicked.connect(self.signal_move_right.emit)
        self.moveLeftButton.clicked.connect(self.signal_move_left.emit)
        self.removeButton.clicked.connect(self.signal_remove.emit)

        layout = QGridLayout()
        layout.addWidget(self.moveLeftButton, 2, 0)
        layout.addWidget(self.moveRightButton, 2, 1)
        layout.addWidget(self.removeButton, 2, 2)
        layout.addWidget(label_sweep, 4, 0)
        layout.addWidget(self.comboBox_sweep_channel, 4, 1, 1, 2)
        layout.addWidget(label_wait, 6, 0)
        layout.addWidget(self.lineEdit_wait_time, 6, 1, 1, 2)
        layout.addWidget(self.sweep_widget, 10, 0, 1, 3)
        self.setLayout(layout)

    def get_name(self, pos):
        """

        Parameters
        ----------
        pos :


        Returns
        -------

        """
        self.moveLeftButton.setEnabled(True)
        self.moveRightButton.setEnabled(True)
        if pos == "outer":
            self.moveLeftButton.setEnabled(False)
        elif pos == "inner":
            self.moveRightButton.setEnabled(False)
        p = f"{pos}: " if pos != "mid" else ""
        return f"{p}{self.comboBox_sweep_channel.currentText()}"

    def get_info(self):
        """ """
        self.loop_step.sweep_channel = self.comboBox_sweep_channel.currentText()
        self.loop_step.wait_time = self.lineEdit_wait_time.text()
        return self.loop_step
