from PyQt5.QtWidgets import QComboBox, QLabel, QCheckBox, QTabWidget, QPushButton, QWidget, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal

from main_classes.loop_step import Loop_Step_Config, Loop_Step
from utility import variables_handling
from utility.channels_check_table import Channels_Check_Table
from utility.load_save_helper_functions import load_plots
from bluesky_handling.builder_helper_functions import plot_creator
from frontpanels.plot_definer import Plot_Button_Overview

from loop_steps.for_while_loops import For_Loop_Step_Config_Sub, For_Loop_Step



class ND_Sweep(Loop_Step):
    def __init__(self, name='', parent_step=None, step_info=None,
                 **kwargs):
        super().__init__(name=name, parent_step=parent_step, step_info=step_info,
                         **kwargs)
        step_info = step_info or {}
        self.step_type = 'N-D Sweep'
        self.has_children = False
        self.sweep_channels = step_info['sweep_channels'] if 'sweep_channels' in step_info else []
        self.data_output = step_info['data_output'] if 'data_output' in step_info else 'sub-stream'
        self.plots = load_plots([], step_info['plots']) if 'plots' in step_info else []
        self.read_channels = step_info['read_channels'] if 'read_channels' in step_info else []
        self.use_own_plots = step_info['use_own_plots'] if 'use_own_plots' in step_info else False
        self.sweep_values = step_info['sweep_values'] if 'sweep_values' in step_info else []

    def update_used_devices(self):
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

    def get_outer_string(self):
        if self.use_own_plots:
            return plot_creator(self.plots, f'create_plots_{self.name}')[0]
        return ''

    def get_add_main_string(self):
        stream = f'"{self.name}"'
        if self.data_output == 'main stream':
            stream = '"primary"'
        add_main_string = ''
        if self.use_own_plots:
            add_main_string += f'\treturner["{self.name}_plot_stuff"] = create_plots_{self.name}(RE, {stream})\n'
        return add_main_string



class Sweep_Step(For_Loop_Step):
    def __init__(self, step_info=None):
        step_info = step_info or {}
        super().__init__(step_info=step_info)
        self.sweep_channel = step_info['sweep_channel'] if 'sweep_channel' in step_info else ''




class ND_Sweep_Config(Loop_Step_Config):
    def __init__(self, loop_step:ND_Sweep, parent=None):
        super().__init__(parent, loop_step)
        self.loop_step = loop_step

        label_data = QLabel('Data Output:')
        font = QFont()
        font.setBold(True)
        label_data.setStyleSheet('font-size: 9pt')
        label_data.setFont(font)
        self.comboBox_data_output = QComboBox()
        output_types = ['sub-stream', 'main stream', 'own file']
        self.comboBox_data_output.addItems(output_types)
        self.comboBox_data_output.setCurrentText(loop_step.data_output)

        labels = ['read', 'channel']
        info_dict = {'channel': self.loop_step.read_channels}
        self.read_table = Channels_Check_Table(self, labels, info_dict=info_dict,
                                               title='Read-Channels')

        self.plot_widge = Plot_Button_Overview(self, self.loop_step.plots)

        self.addSweepChannelButton = QPushButton('Add sweep channel')
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
        ind = self.tab_widget.currentIndex()
        self.tab_widget.removeTab(ind)
        self.tabs.pop(ind)
        self.change_tab_name()

    def add_sweep_channel(self, sweep_info=None):
        if not sweep_info:
            sweep_info = Sweep_Step()
        tab = Single_Sweep_Tab(sweep_info, self)
        tab.signal_change_sweep.connect(self.change_tab_name)
        tab.signal_remove.connect(self.remove_sweep_channel)
        tab.signal_move_left.connect(lambda: self.move_tab(-1))
        tab.signal_move_right.connect(lambda: self.move_tab(1))
        self.tabs.append(tab)
        self.tab_widget.addTab(tab, '')
        self.change_tab_name()

    def change_tab_name(self):
        for i, tab in enumerate(self.tabs):
            if i == 0:
                pos = 'outer'
            elif i == len(self.tabs) - 1:
                pos = 'inner'
            else:
                pos = 'mid'
            name = tab.get_name(pos)
            self.tab_widget.setTabText(i, name)

    def move_tab(self, direction=1):
        ind = self.tab_widget.currentIndex()
        self.tab_widget.tabBar().moveTab(ind, ind + direction)
        self.tabs[ind + direction], self.tabs[ind] = self.tabs[ind], self.tabs[ind + direction]
        self.change_tab_name()

    def update_step_config(self):
        self.loop_step.sweep_values = []
        self.loop_step.sweep_channels = []
        for tab in self.tabs:
            info = tab.get_info()
            chan = info.sweep_channel
            if chan in self.loop_step.sweep_channels:
                raise Exception(f'Can only scan same channel once in ND-sweep!\n{chan}')
            self.loop_step.sweep_channels.append(chan)
            self.loop_step.sweep_values.append(info)
        super().update_step_config()
        self.loop_step.plots = self.plot_widge.plot_data
        self.loop_step.read_channels = self.read_table.get_info()['channel']
        self.loop_step.data_output = self.comboBox_data_output.currentText()





class Single_Sweep_Tab(QWidget):
    signal_remove = pyqtSignal()
    signal_move_left = pyqtSignal()
    signal_move_right = pyqtSignal()
    signal_change_sweep = pyqtSignal()

    def __init__(self, loop_step:Sweep_Step, parent=None):
        super().__init__(parent)
        self.loop_step = loop_step
        label_sweep = QLabel('Sweep Channel:')
        out_channels = variables_handling.get_output_channels()
        self.comboBox_sweep_channel = QComboBox()
        self.comboBox_sweep_channel.addItems(out_channels)
        if loop_step.sweep_channel in out_channels:
            self.comboBox_sweep_channel.setCurrentText(loop_step.sweep_channel)
        self.comboBox_sweep_channel.currentTextChanged.connect(self.signal_change_sweep.emit)

        self.sweep_widget = For_Loop_Step_Config_Sub(parent=self,
                                                     loop_step=loop_step)

        self.moveLeftButton = QPushButton('Move left/out')
        self.moveRightButton = QPushButton('Move right/in')
        self.removeButton = QPushButton('Remove')

        self.moveRightButton.clicked.connect(self.signal_move_right.emit)
        self.moveLeftButton.clicked.connect(self.signal_move_left.emit)
        self.removeButton.clicked.connect(self.signal_remove.emit)

        layout = QGridLayout()
        layout.addWidget(self.moveLeftButton, 2, 0)
        layout.addWidget(self.moveRightButton, 2, 1)
        layout.addWidget(self.removeButton, 2, 2)
        layout.addWidget(label_sweep, 4, 0)
        layout.addWidget(self.comboBox_sweep_channel, 4, 1, 1, 2)
        layout.addWidget(self.sweep_widget, 10, 0, 1, 3)
        self.setLayout(layout)

    def get_name(self, pos):
        self.moveLeftButton.setEnabled(True)
        self.moveRightButton.setEnabled(True)
        if pos == 'outer':
            self.moveLeftButton.setEnabled(False)
        elif pos == 'inner':
            self.moveRightButton.setEnabled(False)
        p = f'{pos}: ' if pos != 'mid' else ''
        return f'{p}{self.comboBox_sweep_channel.currentText()}'


    def get_info(self):
        self.loop_step.sweep_channel = self.comboBox_sweep_channel.currentText()
        return self.loop_step

