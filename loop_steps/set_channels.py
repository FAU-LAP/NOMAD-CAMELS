from PyQt5.QtWidgets import QComboBox, QCheckBox

from main_classes.loop_step import Loop_Step, Loop_Step_Config

from utility.add_remove_table import AddRemoveTable
from utility import variables_handling


class Set_Channels(Loop_Step):
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, **kwargs)
        self.step_type = 'Set Channels'
        if step_info is None:
            step_info = {}
        self.channels_values = step_info['channels_values'] if 'channels_values' in step_info else {'Channels': [], 'Values': []}
        self.wait_for_set = step_info['wait_for_set'] if 'wait_for_set' in step_info else True
        self.update_used_devices()

    def update_used_devices(self):
        self.used_devices = []
        for channel in self.channels_values['Channels']:
            device = variables_handling.channels[channel].device
            if device not in self.used_devices:
                self.used_devices.append(device)

    def get_protocol_string(self, n_tabs=1):
        tabs = '\t' * n_tabs
        protocol_string = f'{tabs}print("starting loop_step {self.full_name}")\n'
        for i, channel in enumerate(self.channels_values['Channels']):
            if channel not in variables_handling.channels:
                raise Exception(f'Trying to set channel {channel} in {self.full_name}, but it does not exist!')
            dev, chan = variables_handling.channels[channel].name.split('.')
            val = self.channels_values['Values'][i]
            protocol_string += f'{tabs}yield from bps.abs_set(devs["{dev}"].{chan}, {val}, group="A")\n'
        if self.wait_for_set:
            protocol_string += f'{tabs}yield from bps.wait("A")\n'
        return protocol_string


class Set_Channels_Config(Loop_Step_Config):
    def __init__(self, loop_step:Set_Channels, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = Set_Channels_Config_Sub(parent=self, loop_step=loop_step)
        box = []
        for channel in variables_handling.channels:
            if variables_handling.channels[channel].output:
                box.append(channel)
        self.sub_widget = AddRemoveTable(headerLabels=['Channels', 'Values'],
                                         comboBoxes={'Channels': box},
                                         tableData=loop_step.channels_values, checkstrings=1)
        self.checkBox_wait_for_set = QCheckBox('Wait for set')
        self.checkBox_wait_for_set.setChecked(True)
        self.checkBox_wait_for_set.stateChanged.connect(self.check_change)
        self.layout().addWidget(self.checkBox_wait_for_set, 1, 0)
        self.layout().addWidget(self.sub_widget, 2, 0)

    def check_change(self):
        self.loop_step.wait_for_set = self.checkBox_wait_for_set.isChecked()

    def update_step_config(self):
        super().update_step_config()
        self.sub_widget.update_table_data()
        self.loop_step.channels_values = self.sub_widget.tableData

class Set_Channels_Config_Sub(AddRemoveTable):
    def __init__(self, loop_step:Set_Channels, parent=None):
        self.boxes = []
        self.loop_step = loop_step
        super().__init__(parent=parent, headerLabels=['Channel', 'Value'], tableData=loop_step.channels_values)

    def add(self, vals=None):
        super().add(vals)
        index = self.table_model.index(self.table_model.rowCount()-1, 0)
        box = QComboBox()
        for channel in variables_handling.channels:
            if variables_handling.channels[channel].output:
                box.addItem(channel)
        box.currentTextChanged.connect(self.update_table_data)
        self.boxes.append(box)
        self.table.setIndexWidget(index, box)
        self.table.resizeColumnsToContents()
        if vals is not None:
            box.setCurrentText(vals[0])
        self.update_table_data()

    def update_table_data(self):
        self.tableData = {'Channels': [],
                          'Values': []}
        for i in range(self.table_model.rowCount()):
            self.tableData['Values'].append(self.table_model.item(i, 1).text())
            ind = self.table_model.index(i, 0)
            self.tableData['Channels'].append(self.table.indexWidget(ind).currentText())
        self.loop_step.channels_values = self.tableData
        self.loop_step.update_used_devices()
