import pandas as pd

from PyQt5.QtWidgets import QGridLayout, QCheckBox, QComboBox, QLabel, QLineEdit

from main_classes import device_class
from main_classes import measurement_channel

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
        headerlabels = ['setpoint', 'kp', 'ki', 'kd', 'maxval', 'minval', 'bias', 'stability-delta', 'stability-time']
        tableData = None
        if 'pid_val_table' in settings_dict:
            tableData = settings_dict['pid_val_table']
        self.val_table = AddRemoveTable(editables=range(len(headerlabels)), headerLabels=headerlabels, parent=self, tableData=tableData)

        input_label = QLabel('Input Channel:')
        output_label = QLabel('Output Channel:')
        bias_label = QLabel('Bias Channel:')
        timer_label = QLabel('Time Delta:')
        self.comboBox_input = QComboBox()
        self.comboBox_output = QComboBox()
        self.comboBox_bias = QComboBox()
        self.comboBox_time = QComboBox()
        self.comboBox_input.addItems(sorted(variables_handling.channels.keys(), key=lambda x: x.lower()))
        for chan in sorted(variables_handling.channels.keys(), key=lambda x: x.lower()):
            if variables_handling.channels[chan].output:
                self.comboBox_output.addItem(chan)
                self.comboBox_bias.addItem(chan)
        if 'pid_inp' in config_dict and type(config_dict['pid_inp']) is str:
            pv = config_dict['pid_inp'].split(' ')[0]
            channel = measurement_channel.from_pv_name(pv)
            if channel in variables_handling.channels:
                self.comboBox_input.setCurrentText(channel)
        if 'pid_outl' in config_dict and type(config_dict['pid_outl']) is str:
            pv = config_dict['pid_outl'].split(' ')[0]
            channel = measurement_channel.from_pv_name(pv)
            if channel in variables_handling.channels:
                self.comboBox_output.setCurrentText(channel)
        self.scan_dict = {'10 seconds': [3, 10],
                          '5 seconds': [4, 5],
                          '2 seconds': [5, 2],
                          '1 second': [6, 1],
                          '0.5 seconds': [7, 0.5],
                          '0.2 seconds': [8, 0.2],
                          '0.1 seconds': [9, 0.1]}
        self.comboBox_time.addItems(self.scan_dict.keys())
        if 'pid_scan' in config_dict:
            for key, item in self.scan_dict.items():
                if item[0] == config_dict['pid_scan']:
                    self.comboBox_time.setCurrentText(key)
                    break
        # if 'pid_inp' in config_dict and config_dict['pid_inp']:
        #     self.comboBox_input.setCurrentText()
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


        layout.addWidget(input_label, 0, 0)
        layout.addWidget(self.comboBox_input, 0, 1)
        layout.addWidget(output_label, 1, 0)
        layout.addWidget(self.comboBox_output, 1, 1)
        layout.addWidget(read_label, 2, 0)
        layout.addWidget(self.lineEdit_read_function, 2, 1)
        layout.addWidget(set_label, 3, 0)
        layout.addWidget(self.lineEdit_set_function, 3, 1)
        layout.addWidget(timer_label, 4, 0)
        layout.addWidget(self.comboBox_time, 4, 1)
        layout.addWidget(self.checkBox_auto_select_values, 5, 0)
        layout.addWidget(self.checkBox_interpolate_auto, 5, 1)
        layout.addWidget(self.comboBox_pid_vals, 6, 0)
        layout.addWidget(self.file_box, 6, 1)
        layout.addWidget(self.val_table, 7, 0, 1, 2)

        self.checkBox_auto_select_values.stateChanged.connect(self.auto_selection_switch)
        self.comboBox_pid_vals.currentTextChanged.connect(self.val_choice_switch)
        self.val_choice_switch()
        self.auto_selection_switch()
        self.file_box.path_changed.connect(self.file_changed)

    def val_choice_switch(self):
        table = self.comboBox_pid_vals.currentText() == 'Table'
        # self.val_table.setEnabled(table)
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
        return self.settings_dict

    def get_config(self):
        inp_chan = variables_handling.channels[self.comboBox_input.currentText()]
        self.config_dict['pid_inp'] = f'{inp_chan.get_pv_name()} CPP NMS'
        out_chan = variables_handling.channels[self.comboBox_output.currentText()]
        self.config_dict['pid_outl'] = f'{out_chan.get_pv_name()} CP NMS'
        self.config_dict['pid_scan'] = self.scan_dict[self.comboBox_time.currentText()][0]
        self.config_dict['pid_mdt'] = self.scan_dict[self.comboBox_time.currentText()][1]
        return self.config_dict