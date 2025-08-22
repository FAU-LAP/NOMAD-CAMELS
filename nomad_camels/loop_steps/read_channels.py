from PySide6.QtWidgets import QWidget, QTableWidgetItem, QLabel, QComboBox
from PySide6.QtCore import Qt
from nomad_camels.main_classes.loop_step import Loop_Step, Loop_Step_Config

from nomad_camels.gui.read_channels import Ui_read_channels_config

from nomad_camels.utility import variables_handling, fit_variable_renaming
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table


class Read_Channels(Loop_Step):
    """
    This step represents the bluesky plan stub `trigger_and_read`. It may also
    be split into an additional step for triggering, then doing something else
    and then reading.

    Attributes
    ----------
    read_all : bool
        If True, the step will read all available channels.
    split_trigger : bool
        If True, an additional trigger channels step may be used. This read step
        will then not use `trigger_and_read`, but only read the channels.
    channel_list : list[str]
        The list of channels that should be read in this step.
    """

    def __init__(self, name="", parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = "Read Channels"
        if step_info is None:
            step_info = {}
        self.read_all = step_info["read_all"] if "read_all" in step_info else False
        self.split_trigger = (
            step_info["split_trigger"] if "split_trigger" in step_info else False
        )
        if "channel_list" in step_info:
            self.channel_list = step_info["channel_list"]
        else:
            self.channel_list = []
        if "skip_failed" in step_info:
            self.skip_failed = step_info["skip_failed"]
        else:
            self.skip_failed = [False] * len(self.channel_list)
        if "read_variables" in step_info:
            self.read_variables = step_info["read_variables"]
        else:
            self.read_variables = True
        self.update_used_devices()

    def update_used_devices(self):
        """All devices that should be read are added to the used_devices."""
        self.used_devices = []
        channels = variables_handling.get_channels()
        for channel in channels:
            if self.read_all or channel in self.channel_list:
                device = channels[channel].device
                if device not in self.used_devices:
                    self.used_devices.append(device)

    def get_used_channels(self):
        """Returns a list of all used channels in this step, including
        the read_channels and the read_variables."""
        if self.read_all:
            used_channels = variables_handling.get_channels().keys()
        else:
            used_channels = self.channel_list.copy()
        return used_channels

    def get_channels_set(self):
        """Provides a set of `self.channel_list` to remove possible duplicates.
        Includes all available channels if `self.read_all`."""
        chan_list = []
        if self.read_all:
            for channel in variables_handling.get_channels():
                chan_list.append(channel)
        else:
            chan_list = self.channel_list
        return set(chan_list)

    def get_channels_string(self, tabs):
        """
        Gives a string of the channels that should be read. This may also be
        used by the Trigger_Channels step.

        Parameters
        ----------
        tabs : str
            A string including the tabs for intendation.
        """
        channel_string = f"{tabs}channels_{self.variable_name()} = ["
        if not self.read_all and not self.channel_list and not self.read_variables:
            raise Exception(f"Trying to read no channel in {self.full_name}!")
        if self.read_all:
            for channel in variables_handling.get_channels():
                channel_string += get_channel_string(channel)
        else:
            for channel in self.channel_list:
                channel_string += get_channel_string(channel)
        if self.read_variables:
            channel_string += f"{self.protocol.name}_variable_signal, "
        channel_string = channel_string[:-2] + "]\n"
        return channel_string

    def variable_name(self):
        """Returns the name of this step as a valid variable name, to specify
        the channels for this read."""
        return fit_variable_renaming.replace_name(self.name)

    def get_protocol_string(self, n_tabs=1):
        """In the protocol, at first a list `channels` is defined,
        including all the channels, that are selected to be read. Then
        `bps.trigger_and_read` (or `helper_functions.read_wo_trigger`) is called
        on these channels.
        The stream in which the data is written will be numbered if there are
        other read_channels that are reading different channels, since bluesky
        only allows reading the same channels inside one stream."""
        # checking compatibility with other readings
        chan_list = self.get_channels_set()
        skip_failed = list(self.skip_failed)
        if self.read_all:
            skip_failed = [False] * len(chan_list)
        if self.read_variables:
            skip_failed.append(False)
        channels_w_variables = set(list(chan_list) + [self.read_variables])
        if channels_w_variables in variables_handling.read_channel_sets:
            n = variables_handling.read_channel_sets.index(channels_w_variables)
        else:
            n = len(variables_handling.read_channel_names)
            variables_handling.read_channel_sets.append(channels_w_variables)
            if n > 0:
                variables_handling.read_channel_names.append(f'f"{{stream_name}}_{n}"')
            else:
                variables_handling.read_channel_names.append("stream_name")
        stream = variables_handling.read_channel_names[n]

        if variables_handling.preferences.get("nested_data", True):
            stream = f'{stream} if stream_name == {stream} else f"{{stream_name}}||sub_stream||{stream.replace('"', '')}"'
        tabs = "\t" * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        if self.split_trigger:
            protocol_string += f"{tabs}yield from helper_functions.read_wo_trigger(channels_{self.variable_name()}, grp_{self.variable_name()}, stream={stream}, skip_on_exception={skip_failed})\n"
        else:
            protocol_string += self.get_channels_string(tabs)
            protocol_string += f"{tabs}yield from helper_functions.trigger_and_read(channels_{self.variable_name()}, name={stream}, skip_on_exception={skip_failed})\n"
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """Includes the channel list in the string."""
        short_string = super().get_protocol_short_string(n_tabs)
        short_string = f"{short_string[:-1]} - {self.channel_list}\n"
        return short_string


def get_channel_string(channel):
    """
    Gives the string of a channel in the way it is written inside the
    protocol, i.e. "devs["<device_name>"].<component/channel_name>".

    Parameters
    ----------
    channel : str
        The channel that should be converted.
    """
    name = variables_handling.get_channels()[channel].name
    if "." in name:
        dev, chan = name.split(".")
        return f'devs["{dev}"].{chan}, '
    else:
        return f'devs["{name}"], '


class Read_Channels_Config(Loop_Step_Config):
    """ """

    def __init__(self, loop_step: Read_Channels, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = Read_Channels_Config_Sub(loop_step, self)
        self.layout().addWidget(self.sub_widget, 1, 0, 1, 5)

    def update_step_config(self):
        """ """
        super().update_step_config()
        self.sub_widget.update_step_config()


class Read_Channels_Config_Sub(Ui_read_channels_config, QWidget):
    """Config for the Read_Channels it provides a table of channels with
    a checkbox, whether to read them. Also there is a checkbox whether
    to simply read all available channels.

    Parameters
    ----------

    Returns
    -------

    """

    def __init__(self, loop_step: Read_Channels, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.loop_step = loop_step
        self.checkBox_read_all.stateChanged.connect(self.read_type_changed)
        self.checkBox_split_trigger.stateChanged.connect(self.use_trigger)

        self.load_data()
        labels = ["read?", "channel", "ignore failed"]
        info_dict = {
            "channel": self.loop_step.channel_list,
            "ignore failed": self.loop_step.skip_failed,
        }
        self.read_table = Channels_Check_Table(
            self, labels, info_dict=info_dict, title="Read-Channels", checkables=[2]
        )
        self.read_type_changed()
        self.layout().addWidget(self.read_table, 5, 0, 1, 3)

    def use_trigger(self):
        """ """
        self.loop_step.split_trigger = self.checkBox_split_trigger.isChecked()

    def read_type_changed(self):
        """If the read-all checkbox is checked, disables the table, if
        not, enables it.

        Parameters
        ----------

        Returns
        -------

        """
        read_all = self.checkBox_read_all.isChecked()
        if hasattr(self, "read_table"):
            self.read_table.setEnabled(not read_all)
        self.loop_step.read_all = read_all
        self.loop_step.update_used_devices()

    def load_data(self):
        """Putting the data from the loop_step into the widgets."""
        self.checkBox_read_all.setChecked(self.loop_step.read_all)
        self.checkBox_read_variables.setChecked(self.loop_step.read_variables)
        self.checkBox_split_trigger.setChecked(self.loop_step.split_trigger)

    def update_step_config(self):
        """ """
        info = self.read_table.get_info()
        self.loop_step.channel_list = info["channel"]
        read_variables = self.checkBox_read_variables.isChecked()
        self.loop_step.skip_failed = info["ignore failed"]
        self.loop_step.read_variables = read_variables


class Trigger_Channels_Step(Loop_Step):
    """
    This step provides a split between triggering and reading channels.

    Attributes
    ----------
    read_step : str
        The name of the Read Channels step, for which this step should do the
        triggering.
    """

    def __init__(self, name="", parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = "Trigger Channels"
        if step_info is None:
            step_info = {}
        self.read_step = step_info["read_step"] if "read_step" in step_info else ""

    def get_protocol_string(self, n_tabs=1):
        """In the protocol, at first a list `channels` is defined,
        including all the channels, that are selected to be read. Then
        these channels are triggered with `helper_functions.trigger_multi`."""
        tabs = "\t" * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        if self.read_step not in variables_handling.current_protocol.loop_step_dict:
            raise Exception(
                f'Trying to trigger channels for read_channels "{self.read_step}" but it is not there.\n{self.full_name}'
            )
        read_step = variables_handling.current_protocol.loop_step_dict[self.read_step]
        protocol_string += read_step.get_channels_string(tabs)
        step_name = read_step.variable_name()
        protocol_string += f'{tabs}grp_{step_name} = bps._short_uid("trigger")\n'
        protocol_string += f"{tabs}yield from helper_functions.trigger_multi(channels_{step_name}, grp_{step_name})\n"
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """The corresponding read step is displayed."""
        short_string = super().get_protocol_short_string(n_tabs)
        read_step = variables_handling.current_protocol.loop_step_dict[self.read_step]
        short_string = f"{short_string[:-1]} - {read_step.channel_list}\n"
        return short_string


class Trigger_Channels_Config(Loop_Step_Config):
    """ """

    def __init__(self, loop_step: Trigger_Channels_Step, parent=None):
        super().__init__(parent, loop_step)
        label = QLabel("Corresponding Read-Step:")
        self.comboBox_read_step = QComboBox()
        self.layout().addWidget(label, 1, 0)
        self.layout().addWidget(self.comboBox_read_step, 1, 1, 1, 4)
        triggerable = []
        for name, step in variables_handling.current_protocol.loop_step_dict.items():
            if step.step_type == "Read Channels" and step.split_trigger:
                triggerable.append(name)
        self.comboBox_read_step.addItems(triggerable)

    def update_step_config(self):
        """ """
        self.loop_step.read_step = self.comboBox_read_step.currentText()
        super().update_step_config()
