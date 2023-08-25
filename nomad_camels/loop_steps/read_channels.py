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
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = 'Read Channels'
        if step_info is None:
            step_info = {}
        self.read_all = step_info['read_all'] if 'read_all' in step_info else False
        self.split_trigger = step_info['split_trigger'] if 'split_trigger' in step_info else False
        if 'channel_list' in step_info:
            self.channel_list = step_info['channel_list']
        else:
            self.channel_list = []
        self.update_used_devices()

    def update_used_devices(self):
        """All devices that should be read are added to the used_devices."""
        self.used_devices = []
        for channel in variables_handling.channels:
            if self.read_all or channel in self.channel_list:
                device = variables_handling.channels[channel].device
                if device not in self.used_devices:
                    self.used_devices.append(device)

    def get_channels_set(self):
        """Provides a set of `self.channel_list` to remove possible duplicates.
        Includes all available channels if `self.read_all`."""
        chan_list = []
        if self.read_all:
            for channel in variables_handling.channels:
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
        channel_string = f'{tabs}channels_{self.variable_name()} = ['
        if not self.read_all and not self.channel_list:
            raise Exception(f'Trying to read no channel in {self.full_name}!')
        if self.read_all:
            for channel in variables_handling.channels:
                channel_string += get_channel_string(channel)
        else:
            for channel in self.channel_list:
                channel_string += get_channel_string(channel)
        channel_string = channel_string[:-2] + ']\n'
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
        if set(chan_list) in variables_handling.read_channel_sets:
            n = variables_handling.read_channel_sets.index(set(chan_list))
        else:
            n = len(variables_handling.read_channel_names)
            variables_handling.read_channel_sets.append(chan_list)
            if n > 0:
                variables_handling.read_channel_names.append(f'f"{{stream_name}}_{n}"')
            else:
                variables_handling.read_channel_names.append('stream_name')
        stream_name = variables_handling.read_channel_names[n]
        tabs = '\t' * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        if self.split_trigger:
            protocol_string += f'{tabs}yield from helper_functions.read_wo_trigger(channels_{self.variable_name()}, grp_{self.variable_name()}, stream={stream_name})\n'
        else:
            protocol_string += self.get_channels_string(tabs)
            protocol_string += f'{tabs}yield from bps.trigger_and_read(channels_{self.variable_name()}, name={stream_name})\n'
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """Includes the channel list in the string."""
        short_string = super().get_protocol_short_string(n_tabs)
        short_string = f'{short_string[:-1]} - {self.channel_list}\n'
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
    name = variables_handling.channels[channel].name
    if '.' in name:
        dev, chan = name.split('.')
        return f'devs["{dev}"].{chan}, '
    else:
        return f'devs["{name}"], '



class Read_Channels_Config(Loop_Step_Config):
    """ """
    def __init__(self, loop_step:Read_Channels, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = Read_Channels_Config_Sub(loop_step, self)
        self.layout().addWidget(self.sub_widget, 1, 0, 1, 5)

    def update_step_config(self):
        """ """
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
    def __init__(self, loop_step:Read_Channels, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.loop_step = loop_step
        self.checkBox_read_all.stateChanged.connect(self.read_type_changed)
        self.checkBox_split_trigger.stateChanged.connect(self.use_trigger)
        # self.comboBox_readType.addItems(['read all', 'read selected'])
        # self.comboBox_readType.currentTextChanged.connect(self.read_type_changed)
        self.load_data()
        labels = ['read', 'channel']
        info_dict = {'channel': self.loop_step.channel_list}
        self.read_table = Channels_Check_Table(self, labels, info_dict=info_dict,
                                               title='Read-Channels')
        self.read_type_changed()
        self.layout().addWidget(self.read_table, 5, 0, 1, 2)
        # self.tableWidget_channels.setHorizontalHeaderLabels(['read',
        #                                                      'channel name',
        #                                                      'use set-value'])
        # self.build_channels_table()
        # self.lineEdit_search.textChanged.connect(self.build_channels_table)
        # self.checkBox_use_set.toggled.connect(self.checkbox_toggle)
        # self.checkBox_plot.toggled.connect(self.checkbox_toggle)
        # self.checkBox_save.toggled.connect(self.checkbox_toggle)
        # self.tableWidget_channels.clicked.connect(self.table_check_changed)

    def use_trigger(self):
        """ """
        self.loop_step.split_trigger = self.checkBox_split_trigger.isChecked()

    # def checkbox_toggle(self):
    #     """When a checkbox is (un-)checked, the new value is stored
    #     inside the loop_step."""
    #     self.loop_step.use_set_val = self.checkBox_use_set.isChecked()
    #     self.loop_step.save_data = self.checkBox_save.isChecked()
    #     self.loop_step.plot_data = self.checkBox_plot.isChecked()

    def read_type_changed(self):
        """If the read-all checkbox is checked, disables the table, if
        not, enables it.

        Parameters
        ----------

        Returns
        -------

        """
        read_all = self.checkBox_read_all.isChecked()
        if hasattr(self, 'read_table'):
            self.read_table.setEnabled(not read_all)
        # if read_all:
        #     self.tableWidget_channels.setEnabled(False)
        #     self.checkBox_use_set.setEnabled(True)
        # else:
        #     self.tableWidget_channels.setEnabled(True)
        #     self.checkBox_use_set.setEnabled(False)
        self.loop_step.read_all = read_all
        self.loop_step.update_used_devices()

    def load_data(self):
        """Putting the data from the loop_step into the widgets."""
        self.checkBox_read_all.setChecked(self.loop_step.read_all)
        self.checkBox_split_trigger.setChecked(self.loop_step.split_trigger)
        # self.checkBox_save.setChecked(self.loop_step.save_data)
        # self.checkBox_plot.setChecked(self.loop_step.plot_data)
        # self.checkBox_use_set.setChecked(self.loop_step.use_set_val)
        # self.build_channels_table()

    def update_step_config(self):
        """ """
        self.loop_step.channel_list = self.read_table.get_info()['channel']
        # self.lineEdit_search.clear()
        # self.build_channels_table()
        # self.loop_step.channel_list = []
        # for i in range(self.tableWidget_channels.rowCount()):
        #     if self.tableWidget_channels.item(i, 0).checkState() > 0:
        #         name = self.tableWidget_channels.item(i, 1).text()
        #         self.loop_step.channel_list.append(name)

    def table_check_changed(self, pos):
        """If a checkbox inside the table is clicked, the value is
        stored into the loopstep.

        Parameters
        ----------
        pos :
            

        Returns
        -------

        """
        r = pos.row()
        c = pos.column()
        if c == 0:
            name = self.tableWidget_channels.item(r, 1).text()
            if self.tableWidget_channels.item(r, c).checkState() != Qt.CheckState.Unchecked:
                self.loop_step.channel_list.append(name)
                self.loop_step.channel_list = list(set(self.loop_step.channel_list))
            elif name in self.loop_step.channel_list:
                self.loop_step.channel_list.remove(name)
            self.loop_step.update_used_devices()
        #     self.loop_step.channel_dict[name]['read'] =
        #     self.loop_step.update_used_devices()
        # if c == 2 and variables_handling.channels[name].output:
        #     self.loop_step.channel_dict[name]['use set'] = self.tableWidget_channels.item(r, c).checkState() > 0


    def build_channels_table(self):
        """This creates the table for all channels."""
        self.tableWidget_channels.clear()
        self.tableWidget_channels.setColumnCount(2)
        # self.tableWidget_channels.setRowCount(len(variables_handling.channels))
        self.tableWidget_channels.setRowCount(0)
        self.tableWidget_channels.setHorizontalHeaderLabels(['read', 'channel name'])
        searchtext = self.lineEdit_search.text()
        n = 0
        for i, channel in enumerate(sorted(variables_handling.channels, key=lambda x: x.lower())):
            if searchtext not in channel:
                continue
            self.tableWidget_channels.setRowCount(n+1)
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if channel in self.loop_step.channel_list:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            self.tableWidget_channels.setItem(n, 0, item)
            item = QTableWidgetItem(channel)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.tableWidget_channels.setItem(n, 1, item)
            n += 1
            # if variables_handling.channels[channel].output:
            #     item = QTableWidgetItem()
            #     item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            #     if channel in self.loop_step.channel_dict:
            #         item.setCheckState(2 if self.loop_step.channel_dict[channel]['use set'] else False)
            #     else:
            #         item.setCheckState(False)
            # else:
            #     item = QTableWidgetItem()
            #     item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            # self.tableWidget_channels.setItem(i, 2, item)
        self.tableWidget_channels.resizeColumnsToContents()
        # for channel in self.loop_step.channel_dict:
        #     if channel not in variables_handling.channels:
        #         self.loop_step.channel_dict.pop(channel)


class Trigger_Channels_Step(Loop_Step):
    """
    This step provides a split between triggering and reading channels.

    Attributes
    ----------
    read_step : str
        The name of the Read Channels step, for which this step should do the
        triggering.
    """

    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = 'Trigger Channels'
        if step_info is None:
            step_info = {}
        self.read_step = step_info['read_step'] if 'read_step' in step_info else ''

    def get_protocol_string(self, n_tabs=1):
        """In the protocol, at first a list `channels` is defined,
        including all the channels, that are selected to be read. Then
        these channels are triggered with `helper_functions.trigger_multi`."""
        tabs = '\t' * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        if self.read_step not in variables_handling.current_protocol.loop_step_dict:
            raise Exception(f'Trying to trigger channels for read_channels "{self.read_step}" but it is not there.\n{self.full_name}')
        read_step = variables_handling.current_protocol.loop_step_dict[self.read_step]
        protocol_string += read_step.get_channels_string(tabs)
        step_name = read_step.variable_name()
        protocol_string += f'{tabs}grp_{step_name} = bps._short_uid("trigger")\n'
        protocol_string += f'{tabs}yield from helper_functions.trigger_multi(channels_{step_name}, grp_{step_name})\n'
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """The corresponding read step is displayed."""
        short_string = super().get_protocol_short_string(n_tabs)
        read_step = variables_handling.current_protocol.loop_step_dict[self.read_step]
        short_string = f'{short_string[:-1]} - {read_step.channel_list}\n'
        return short_string


class Trigger_Channels_Config(Loop_Step_Config):
    """ """
    def __init__(self, loop_step:Trigger_Channels_Step, parent=None):
        super().__init__(parent, loop_step)
        label = QLabel('Corresponding Read-Step:')
        self.comboBox_read_step = QComboBox()
        self.layout().addWidget(label, 1, 0)
        self.layout().addWidget(self.comboBox_read_step, 1, 1, 1, 4)
        triggerable = []
        for name, step in variables_handling.current_protocol.loop_step_dict.items():
            if step.step_type == 'Read Channels' and step.split_trigger:
                triggerable.append(name)
        self.comboBox_read_step.addItems(triggerable)

    def update_step_config(self):
        """ """
        self.loop_step.read_step = self.comboBox_read_step.currentText()
        super().update_step_config()
