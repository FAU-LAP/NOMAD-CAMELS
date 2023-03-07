import pandas as pd

from PyQt5.QtWidgets import QGridLayout, QCheckBox, QComboBox, QLabel, QLineEdit

from CAMELS.main_classes import device_class
from CAMELS.main_classes import measurement_channel

from utility.add_remove_table import AddRemoveTable
from utility.path_button_edit import Path_Button_Edit
from utility import variables_handling




class subclass_config_sub(device_class.Device_Config_Sub):
    def __init__(self, settings_dict=None, parent=None, config_dict=None):
        super().__init__(settings_dict=settings_dict, parent=parent,
                         config_dict=config_dict)
        self.settings_dict = settings_dict
        self.config_dict = config_dict

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.checkBox_interpolate_auto = QCheckBox('Interpolate PID values')
        self.checkBox_auto_select_values = QCheckBox('auto select values')
        self.comboBox_pid_vals = QComboBox()
        val_choice = ['Table', 'File']
        self.comboBox_pid_vals.addItems(val_choice)
        if 'interpolate_auto' in settings_dict:
            self.checkBox_interpolate_auto.setChecked(settings_dict['interpolate_auto'])
        if 'auto_pid' in settings_dict:
            self.checkBox_auto_select_values.setChecked(settings_dict['auto_pid'])
        if 'val_choice' in settings_dict and settings_dict['val_choice'] in val_choice:
            self.comboBox_pid_vals.setCurrentText(settings_dict['val_choice'])
        self.file_box = Path_Button_Edit(self)
        if 'val_file' in settings_dict:
            self.file_box.set_path(settings_dict['val_file'])
        headerlabels = ['setpoint', 'kp', 'ki', 'kd', 'max_value', 'min_value', 'bias', 'stability-delta', 'stability-time']
        tableData = None
        if 'pid_val_table' in settings_dict:
            tableData = settings_dict['pid_val_table']
        self.val_table = AddRemoveTable(editables=range(len(headerlabels)), headerLabels=headerlabels, parent=self, tableData=tableData)

        self.input_label = QLabel('Input Channel:')
        self.output_label = QLabel('Output Channel:')
        bias_label = QLabel('Bias Channel:')
        timer_label = QLabel('Time Delta:')
        self.comboBox_input = QComboBox()
        self.comboBox_output = QComboBox()
        self.comboBox_bias = QComboBox()
        self.lineEdit_time = QLineEdit('1')
        self.comboBox_input.addItems(sorted(variables_handling.channels.keys(), key=lambda x: x.lower()))
        for chan in sorted(variables_handling.channels.keys(), key=lambda x: x.lower()):
            if variables_handling.channels[chan].output:
                self.comboBox_output.addItem(chan)
                self.comboBox_bias.addItem(chan)
        if 'read_signal_name' in settings_dict and type(settings_dict['read_signal_name']) is str:
            channel = settings_dict['read_signal_name']
            if channel in variables_handling.channels:
                self.comboBox_input.setCurrentText(channel)
        if 'set_signal_name' in settings_dict and type(settings_dict['set_signal_name']) is str:
            channel = settings_dict['set_signal_name']
            if channel in variables_handling.channels:
                self.comboBox_output.setCurrentText(channel)
        if 'dt' in config_dict:
            self.lineEdit_time.setText(str(config_dict['dt']))
        read_label = QLabel('Conversion function for reading:')
        set_label = QLabel('Conversion function for setting:')
        read_conv = ''
        if 'read_conv_func' in settings_dict:
            read_conv = str(settings_dict['read_conv_func']) or ''
        set_conv = ''
        if 'set_conv_func' in settings_dict:
            set_conv = str(settings_dict['set_conv_func']) or ''
        self.lineEdit_read_function = QLineEdit(read_conv)
        self.lineEdit_set_function = QLineEdit(set_conv)

        self.checkBox_plot = QCheckBox('Plot PID values?')
        if 'show_plot' in settings_dict:
            self.checkBox_plot.setChecked(settings_dict['show_plot'])

        layout.addWidget(self.checkBox_plot, 0, 0, 1, 2)
        layout.addWidget(self.input_label, 1+0, 0)
        layout.addWidget(self.comboBox_input, 1+0, 1)
        layout.addWidget(self.output_label, 1+1, 0)
        layout.addWidget(self.comboBox_output, 1+1, 1)
        layout.addWidget(read_label, 1+2, 0)
        layout.addWidget(self.lineEdit_read_function, 1+2, 1)
        layout.addWidget(set_label, 1+3, 0)
        layout.addWidget(self.lineEdit_set_function, 1+3, 1)
        layout.addWidget(timer_label, 1+4, 0)
        layout.addWidget(self.lineEdit_time, 1+4, 1)
        layout.addWidget(self.checkBox_auto_select_values, 1+5, 0)
        layout.addWidget(self.checkBox_interpolate_auto, 1+5, 1)
        layout.addWidget(self.comboBox_pid_vals, 1+6, 0)
        layout.addWidget(self.file_box, 1+6, 1)
        layout.addWidget(self.val_table, 1+7, 0, 1, 2)

        self.checkBox_auto_select_values.stateChanged.connect(self.auto_selection_switch)
        self.comboBox_pid_vals.currentTextChanged.connect(self.val_choice_switch)
        self.val_choice_switch()
        self.auto_selection_switch()
        self.file_box.path_changed.connect(self.file_changed)

    def val_choice_switch(self):
        table = self.comboBox_pid_vals.currentText() == 'Table'
        if not table:
            self.file_changed()
        self.file_box.setEnabled(not table)
        self.val_table.setEnabled(table)

    def auto_selection_switch(self):
        sel_on = self.checkBox_auto_select_values.isChecked()
        self.checkBox_interpolate_auto.setEnabled(sel_on)

    def file_changed(self):
        try:
            df = pd.read_csv(self.file_box.get_path(), delimiter='\t')
            self.val_table.tableData = df
            self.val_table.load_table_data()
        except Exception as e:
            print(e)

    def get_settings(self):
        self.settings_dict['auto_pid'] = self.checkBox_auto_select_values.isChecked()
        self.settings_dict['interpolate_auto'] = self.checkBox_interpolate_auto.isChecked()
        self.val_table.update_table_data()
        self.settings_dict['pid_val_table'] = self.val_table.tableData
        self.settings_dict['val_choice'] = self.comboBox_pid_vals.currentText()
        self.settings_dict['val_file'] = self.file_box.get_path()
        self.settings_dict['read_conv_func'] = self.lineEdit_read_function.text()
        self.settings_dict['set_conv_func'] = self.lineEdit_set_function.text()
        inp_chan = variables_handling.channels[self.comboBox_input.currentText()]
        out_chan = variables_handling.channels[self.comboBox_output.currentText()]
        self.settings_dict['!non_string!_read_signal'] = inp_chan.get_bluesky_name()
        self.settings_dict['!non_string!_set_signal'] = out_chan.get_bluesky_name()
        self.settings_dict['read_signal_name'] = self.comboBox_input.currentText()
        self.settings_dict['set_signal_name'] = self.comboBox_output.currentText()
        self.settings_dict['show_plot'] = self.checkBox_plot.isChecked()
        return self.settings_dict

    def get_config(self):
        self.config_dict['dt'] = float(self.lineEdit_time.text())
        return self.config_dict
