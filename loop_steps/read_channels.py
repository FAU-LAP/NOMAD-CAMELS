from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from main_classes.loop_step import Loop_Step, Loop_Step_Config

from gui.read_channels import Ui_read_channels_config

from utility import variables_handling


class Read_Channels(Loop_Step):
    """This step represents the bluesky plan stub `trigger_and_read`.

    Attributes
    ----------
    read_all : bool
        whether to simply read all available channels
    channel_dict : dict
        the dictionary of all channels and whether to read them. It also
        provides "use set" for using the set-value without reading, but
        that is not supported. The shape should look like:
        {channel: {'read': True, 'use set': False}}
    """
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, **kwargs)
        self.step_type = 'Read Channels'
        if step_info is None:
            step_info = {}
        self.read_all = step_info['read_all'] if 'read_all' in step_info else True
        self.plot_data = step_info['plot_data'] if 'plot_data' in step_info else True
        self.save_data = step_info['save_data'] if 'save_data' in step_info else True
        self.use_set_val = step_info['use_set_val'] if 'use_set_val' in step_info else False
        if 'channel_dict' in step_info:
            self.channel_dict = step_info['channel_dict']
        else:
            self.channel_dict = {}
        for channel in variables_handling.channels:
            if channel not in self.channel_dict:
                self.channel_dict.update({channel: {'read': False,
                                                'use set': False}})
        self.update_used_devices()

    def update_used_devices(self):
        """All devices that should be read are added to the used_devices."""
        self.used_devices = []
        for channel_name, channel_info in self.channel_dict.items():
            if (self.read_all or channel_info['read']) and channel_name in variables_handling.channels:
                device = variables_handling.channels[channel_name].device
                if device not in self.used_devices:
                    self.used_devices.append(device)



    def get_protocol_string(self, n_tabs=1):
        """In the protocol, at first a list `channels` is defined,
        including all the channels, that are selected to be read. Then
        bps.trigger_and_read is called on these channels."""
        tabs = '\t' * n_tabs
        protocol_string = f'{tabs}print("starting loop_step {self.full_name}")\n'
        protocol_string += f'{tabs}channels = ['
        inserted = False
        for channel, channel_data in self.channel_dict.items():
            if channel not in variables_handling.channels:
                raise Exception(f'Trying to read channel {channel} in {self.full_name}, but it does not exist!')
            if self.read_all or channel_data['read']:
                if inserted:
                    protocol_string += ', '
                name = variables_handling.channels[channel].name
                if '.' in name:
                    dev, chan = name.split('.')
                    protocol_string += f'devs["{dev}"].{chan}'
                else:
                    protocol_string += f'devs["{name}"]'
                inserted = True
        protocol_string += ']\n'
        protocol_string += f'{tabs}yield from bps.trigger_and_read(channels, name=stream_name)\n'
        return protocol_string




class Read_Channels_Config(Loop_Step_Config):
    def __init__(self, loop_step:Read_Channels, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = Read_Channels_Config_Sub(loop_step, self)
        self.layout().addWidget(self.sub_widget, 1, 0)

class Read_Channels_Config_Sub(QWidget, Ui_read_channels_config):
    """Config for the Read_Channels it provides a table of channels with
    a checkbox, whether to read them. Also there is a checkbox whether
    to simply read all available channels."""
    def __init__(self, loop_step:Read_Channels, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.loop_step = loop_step
        self.checkBox_read_all.stateChanged.connect(self.read_type_changed)
        # self.comboBox_readType.addItems(['read all', 'read selected'])
        # self.comboBox_readType.currentTextChanged.connect(self.read_type_changed)
        self.load_data()
        self.read_type_changed()
        self.tableWidget_channels.setHorizontalHeaderLabels(['read',
                                                             'channel name',
                                                             'use set-value'])
        self.build_channels_table()
        self.checkBox_use_set.toggled.connect(self.checkbox_toggle)
        self.checkBox_plot.toggled.connect(self.checkbox_toggle)
        self.checkBox_save.toggled.connect(self.checkbox_toggle)
        self.tableWidget_channels.clicked.connect(self.table_check_changed)

    def checkbox_toggle(self):
        """When a checkbox is (un-)checked, the new value is stored
        inside the loop_step."""
        self.loop_step.use_set_val = self.checkBox_use_set.isChecked()
        self.loop_step.save_data = self.checkBox_save.isChecked()
        self.loop_step.plot_data = self.checkBox_plot.isChecked()

    def read_type_changed(self):
        """If the read-all checkbox is checked, disables the table, if
        not, enables it."""
        read_all = self.checkBox_read_all.isChecked()
        if read_all:
            self.tableWidget_channels.setEnabled(False)
            self.checkBox_use_set.setEnabled(True)
        else:
            self.tableWidget_channels.setEnabled(True)
            self.checkBox_use_set.setEnabled(False)
        self.loop_step.read_all = read_all
        self.loop_step.update_used_devices()

    def load_data(self):
        """Putting the data from the loop_step into the widgets."""
        self.checkBox_read_all.setChecked(self.loop_step.read_all)
        self.checkBox_save.setChecked(self.loop_step.save_data)
        self.checkBox_plot.setChecked(self.loop_step.plot_data)
        self.checkBox_use_set.setChecked(self.loop_step.use_set_val)
        self.build_channels_table()

    def table_check_changed(self, pos):
        """If a checkbox inside the table is clicked, the value is
        stored into the loopstep."""
        r = pos.row()
        c = pos.column()
        name = self.tableWidget_channels.item(r, 1).text()
        if c == 0:
            self.loop_step.channel_dict[name]['read'] = self.tableWidget_channels.item(r, c).checkState() > 0
            self.loop_step.update_used_devices()
        if c == 2 and variables_handling.channels[name].output:
            self.loop_step.channel_dict[name]['use set'] = self.tableWidget_channels.item(r, c).checkState() > 0


    def build_channels_table(self):
        """This creates the table for all channels."""
        self.tableWidget_channels.clear()
        self.tableWidget_channels.setColumnCount(3)
        self.tableWidget_channels.setRowCount(len(variables_handling.channels))
        self.tableWidget_channels.setHorizontalHeaderLabels(['read', 'channel name', 'use set-value'])
        for i, channel in enumerate(sorted(variables_handling.channels, key=lambda x: x.lower())):
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if channel in self.loop_step.channel_dict:
                item.setCheckState(2 if self.loop_step.channel_dict[channel]['read'] else False)
            else:
                item.setCheckState(False)
            self.tableWidget_channels.setItem(i, 0, item)
            item = QTableWidgetItem(channel)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.tableWidget_channels.setItem(i, 1, item)
            if variables_handling.channels[channel].output:
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                if channel in self.loop_step.channel_dict:
                    item.setCheckState(2 if self.loop_step.channel_dict[channel]['use set'] else False)
                else:
                    item.setCheckState(False)
            else:
                item = QTableWidgetItem()
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.tableWidget_channels.setItem(i, 2, item)
        self.tableWidget_channels.resizeColumnsToContents()
        for channel in self.loop_step.channel_dict:
            if channel not in variables_handling.channels:
                self.loop_step.channel_dict.pop(channel)

