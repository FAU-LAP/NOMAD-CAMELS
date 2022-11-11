from PyQt5.QtWidgets import QComboBox, QCheckBox

from main_classes.loop_step import Loop_Step, Loop_Step_Config

from utility.add_remove_table import AddRemoveTable
from utility.channels_check_table import Channels_Check_Table
from utility import variables_handling


class Set_Channels(Loop_Step):
    """Simple loop_step to set some channels.

    Attributes
    ----------
    wait_for_set : bool
        whether to wait for setting to finish before going over to the
        next step
    channels_values : dict
        the dictionary should have the format
        {'Channels': [...], 'Values': [...]} with the corresponding
        channels and values at the same position in their lists
    """
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = 'Set Channels'
        if step_info is None:
            step_info = {}
        self.channels_values = step_info['channels_values'] if 'channels_values' in step_info else {'Channels': [], 'Values': []}
        self.wait_for_set = step_info['wait_for_set'] if 'wait_for_set' in step_info else True
        self.update_used_devices()

    def update_used_devices(self):
        """All devices with a channel that is to be set are added."""
        self.used_devices = []
        for channel in self.channels_values['Channels']:
            if channel in variables_handling.channels:
                device = variables_handling.channels[channel].device
                if device not in self.used_devices:
                    self.used_devices.append(device)

    def get_protocol_string(self, n_tabs=1):
        """If `wait_for_set` is True, then after setting, bps.wait for
        the set group is called."""
        tabs = '\t' * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        for i, channel in enumerate(self.channels_values['Channels']):
            if channel not in variables_handling.channels:
                raise Exception(f'Trying to set channel {channel} in {self.full_name}, but it does not exist!')
            dev, chan = variables_handling.channels[channel].name.split('.')
            val = self.channels_values['Values'][i]
            protocol_string += f'{tabs}yield from bps.abs_set(devs["{dev}"].{chan}, {val}, group="A")\n'
        if self.wait_for_set:
            protocol_string += f'{tabs}yield from bps.wait("A")\n'
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        short_string = super().get_protocol_short_string(n_tabs)
        short_string = f'{short_string[:-1]} - {self.channels_values}\n'
        return short_string


class Set_Channels_Config(Loop_Step_Config):
    """The configuration consists of the checkbox for waiting and a
    simple AddRemoveTable that works with the channels."""
    def __init__(self, loop_step:Set_Channels, parent=None):
        super().__init__(parent, loop_step)
        box = []
        for channel in variables_handling.channels:
            if variables_handling.channels[channel].output:
                box.append(channel)
        info_dict = {'channel': self.loop_step.channels_values['Channels'],
                     'value': self.loop_step.channels_values['Values']}
        # self.sub_widget = AddRemoveTable(headerLabels=['Channels', 'Values'],
        #                                  comboBoxes={'Channels': box},
        #                                  tableData=loop_step.channels_values,
        #                                  checkstrings=1)
        self.sub_widget = Channels_Check_Table(self, ['set', 'channel', 'value'], True, info_dict, [2])
        self.checkBox_wait_for_set = QCheckBox('Wait for set')
        self.checkBox_wait_for_set.setChecked(True)
        self.checkBox_wait_for_set.stateChanged.connect(self.check_change)
        self.layout().addWidget(self.checkBox_wait_for_set, 1, 0, 1, 5)
        self.layout().addWidget(self.sub_widget, 2, 0, 1, 5)

    def check_change(self):
        self.loop_step.wait_for_set = self.checkBox_wait_for_set.isChecked()

    def update_step_config(self):
        super().update_step_config()
        info = self.sub_widget.get_info()
        self.loop_step.channels_values = {'Channels': info['channel'],
                                          'Values': info['value']}
        # self.sub_widget.update_table_data()
        # self.loop_step.channels_values = self.sub_widget.tableData

