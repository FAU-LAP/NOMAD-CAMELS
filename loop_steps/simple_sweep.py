from PyQt5.QtWidgets import QComboBox, QLabel, QCheckBox

from main_classes.loop_step import Loop_Step_Config
from utility import variables_handling
from utility.add_remove_table import AddRemoveTable

from loop_steps.for_while_loops import For_Loop_Step_Config_Sub, For_Loop_Step,\
    get_space_string

class Simple_Sweep(For_Loop_Step):
    def __init__(self, name='', children=None, parent_step=None, step_info=None,
                 **kwargs):
        super().__init__(name, children, parent_step, step_info, **kwargs)
        self.step_type = 'Simple Sweep'
        self.has_children = False
        self.sweep_channel = step_info['sweep_channel'] if 'sweep_channel' in step_info else ''
        self.data_output = step_info['data_output'] if 'data_output' in step_info else 'sub-stream'
        self.plots = step_info['plots'] if 'plots' in step_info else {}
        self.read_channels = step_info['read_channels'] if 'read_channels' in step_info else []
        self.use_own_plots = step_info['use_own_plots'] if 'use_own_plots' in step_info else False

    def update_used_devices(self):
        self.used_devices = []
        set_device = variables_handling.channels[self.sweep_channel].device
        self.used_devices.append(set_device)
        for channel in self.read_channels:
            if channel in variables_handling.channels:
                device = variables_handling.channels[channel].device
                if device not in self.used_devices:
                    self.used_devices.append(device)

    def get_protocol_string(self, n_tabs=1):
        """The loop is enumerating over the selected points."""
        tabs = '\t'*n_tabs
        if self.loop_type in ['start - stop', 'start - min - max - stop',
                              'start - max - min - stop']:
            enumerator = get_space_string(self.start_val, self.stop_val,
                                          self.n_points, self.min_val,
                                          self.max_val, self.loop_type,
                                          self.sweep_mode,
                                          self.include_end_points)
        elif self.loop_type == 'Value-List':
            enumerator = self.val_list
        else:
            enumerator = f'np.loadtxt("{self.file_path}")'

        protocol_string = f'{tabs}print("starting loop_step {self.full_name}")\n'

        protocol_string += f'{tabs}channels = ['
        for i, channel in enumerate(self.read_channels):
            if channel not in variables_handling.channels:
                raise Exception(f'Trying to read channel {channel} in {self.full_name}, but it does not exist!')
            if i > 0:
                protocol_string += ', '
            name = variables_handling.channels[channel].name
            if '.' in name:
                dev, chan = name.split('.')
                protocol_string += f'devs["{dev}"].{chan}'
            else:
                protocol_string += f'devs["{name}"]'
        protocol_string += ']\n'

        name = variables_handling.channels[self.sweep_channel].name
        if '.' in name:
            dev, chan = name.split('.')
            setter = f'devs["{dev}"].{chan}'
        else:
            setter = f'devs["{name}"]'

        protocol_string += f'{tabs}for {self.name.replace(" ", "_")}_Count, {self.name.replace(" ", "_")}_Value in enumerate({enumerator}):\n'
        protocol_string += f'{tabs}\tnamespace.update({{"{self.name.replace(" ", "_")}_Count": {self.name.replace(" ", "_")}_Count, "{self.name.replace(" ", "_")}_Value": {self.name.replace(" ", "_")}_Value}})\n'
        protocol_string += f'{tabs}\tyield from bps.abs_set({setter}, {self.name.replace(" ", "_")}_Value, group="A")\n'
        protocol_string += f'{tabs}\tyield from bps.wait("A")\n'
        protocol_string += f'{tabs}\tyield from bps.trigger_and_read(channels)\n'
        self.update_time_weight()
        return protocol_string

class Simple_Sweep_Config(Loop_Step_Config):
    def __init__(self, loop_step:Simple_Sweep, parent=None):
        super().__init__(parent, loop_step)
        self.loop_step = loop_step
        label_sweep_channel = QLabel('Sweep Channel')
        out_box = []
        in_box = []
        for channel in variables_handling.channels:
            in_box.append(channel)
            if variables_handling.channels[channel].output:
                out_box.append(channel)
        self.comboBox_sweep_channel = QComboBox()
        self.comboBox_sweep_channel.addItems(out_box)
        if loop_step.sweep_channel in out_box:
            self.comboBox_sweep_channel.setCurrentText(loop_step.sweep_channel)

        label_data = QLabel('Data Output:')
        self.comboBox_data_output = QComboBox()
        output_types = ['sub-stream', 'main stream', 'own file']
        self.comboBox_data_output.addItems(output_types)
        self.comboBox_data_output.setCurrentText(loop_step.data_output)

        self.sweep_widget = For_Loop_Step_Config_Sub(parent=self,
                                                   loop_step=loop_step)

        self.read_table = AddRemoveTable(title='Read Channels', headerLabels=[],
                                         tableData=loop_step.read_channels,
                                         comboBoxes=in_box)

        self.checkBox_use_own_plots = QCheckBox('Use own Plots')
        self.checkBox_use_own_plots.setChecked(loop_step.use_own_plots)

        comboBoxes = {'plot-type': ['X-Y plot', 'Value-List', '2D plot']}
        subtables = {'Y-axes': []}
        cols = ['plot-type', 'X-axis', 'Y-axes', 'title', 'x-label', 'y-label']
        self.plot_table = AddRemoveTable(headerLabels=cols, title='Plots',
                                         comboBoxes=comboBoxes,
                                         subtables=subtables,
                                         tableData=loop_step.plots,
                                         checkstrings=[1,2])

        self.layout().addWidget(label_sweep_channel, 1, 0)
        self.layout().addWidget(self.comboBox_sweep_channel, 1, 1)
        self.layout().addWidget(label_data, 2, 0)
        self.layout().addWidget(self.comboBox_data_output, 2, 1)
        self.layout().addWidget(self.sweep_widget, 5, 0, 1, 2)
        self.layout().addWidget(self.read_table, 6, 0, 1, 2)
        self.layout().addWidget(self.checkBox_use_own_plots, 7, 0, 1, 2)
        self.layout().addWidget(self.plot_table, 8, 0, 1, 2)
        self.checkBox_use_own_plots.clicked.connect(self.use_plot_change)
        self.use_plot_change()

    def use_plot_change(self):
        use_plots = self.checkBox_use_own_plots.isChecked()
        self.plot_table.setEnabled(use_plots)

    def update_step_config(self):
        super().update_step_config()
        self.loop_step.use_own_plots = self.checkBox_use_own_plots.isChecked()
        self.loop_step.plots = self.plot_table.update_table_data()
        self.loop_step.read_channels = self.read_table.update_table_data()
        self.loop_step.data_output = self.comboBox_data_output.currentText()
        self.loop_step.sweep_channel = self.comboBox_sweep_channel.currentText()
