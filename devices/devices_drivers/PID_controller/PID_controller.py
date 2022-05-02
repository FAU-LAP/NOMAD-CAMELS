import pandas as pd

from PID_controller.PID_controller_ophyd import PID_Controller

from main_classes import device_class
from utility.number_formatting import format_number

from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QComboBox, QLabel

from utility.add_remove_table import AddRemoveTable
from utility.path_button_edit import Path_Button_Edit
from utility import variables_handling
from main_classes import measurement_channel


class subclass(device_class.Device):
    def __init__(self):
        files = ['PID_controller.db']
        req = ['std']
        super().__init__(name='PID_controller', virtual=True, tags=['PID', 'control'], files=files, directory='PID_controller', ophyd_device=PID_Controller, ophyd_class_name='PID_Controller', requirements=req)

    # def get_channels(self):
    #     channel = Measurement_Channel(self.name, output=True, device=self.name)
    #     return {self.name: channel}


class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None, config_dict=None):
        super().__init__(parent, 'PID_Controller', data, settings_dict, config_dict)
        # self.comboBox_connection_type.addItem()
        self.layout().removeWidget(self.comboBox_connection_type)
        self.comboBox_connection_type.deleteLater()
        self.layout().removeWidget(self.label_connection)
        self.label_connection.deleteLater()
        self.sub_widget = subclass_config_sub(settings_dict=settings_dict, parent=self, config_dict=config_dict)
        self.layout().addWidget(self.sub_widget, 3, 0, 1, 2)
        self.load_settings()

    def get_settings(self):
        return self.sub_widget.get_settings()

    def get_config(self):
        return self.sub_widget.get_config()



class subclass_config_sub(QWidget):
    def __init__(self, settings_dict=None, parent=None, config_dict=None):
        super().__init__(parent)
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
        headerlabels = ['setpoint', 'kp', 'ki', 'kd', 'maxval', 'minval', 'bias']
        tableData = None
        if 'pid_val_table' in settings_dict:
            tableData = settings_dict['pid_val_table']
        self.val_table = AddRemoveTable(editables=range(len(headerlabels)), headerLabels=headerlabels, parent=self, tableData=tableData)

        input_label = QLabel('Input Channel:')
        output_label = QLabel('Output Channel:')
        bias_label = QLabel('Bias Channel:')
        self.comboBox_input = QComboBox()
        self.comboBox_output = QComboBox()
        self.comboBox_bias = QComboBox()
        self.comboBox_input.addItems(sorted(variables_handling.channels.keys(), key=lambda x: x.lower()))
        for chan in sorted(variables_handling.channels.keys(), key=lambda x: x.lower()):
            if variables_handling.channels[chan].output:
                self.comboBox_output.addItem(chan)
                self.comboBox_bias.addItem(chan)

        # if 'pid_inp' in config_dict and config_dict['pid_inp']:
        #     self.comboBox_input.setCurrentText()

        layout.addWidget(input_label, 0, 0)
        layout.addWidget(self.comboBox_input, 0, 1)
        layout.addWidget(output_label, 1, 0)
        layout.addWidget(self.comboBox_output, 1, 1)
        layout.addWidget(self.checkBox_auto_select_values, 2, 0)
        layout.addWidget(self.checkBox_interpolate_auto, 2, 1)
        layout.addWidget(self.comboBox_pid_vals, 3, 0)
        layout.addWidget(self.file_box, 3, 1)
        layout.addWidget(self.val_table, 4, 0, 1, 2)

        self.checkBox_auto_select_values.stateChanged.connect(self.auto_selection_switch)
        self.comboBox_pid_vals.currentTextChanged.connect(self.val_choice_switch)
        self.val_choice_switch()
        self.auto_selection_switch()
        self.file_box.path_changed.connect(self.file_changed)

    def val_choice_switch(self):
        table = self.comboBox_pid_vals.currentText() == 'Table'
        # self.val_table.setEnabled(table)
        self.file_box.setEnabled(not table)
        if not table:
            self.file_changed()

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
        return self.settings_dict

    def get_config(self):
        inp_chan = variables_handling.channels[self.comboBox_input.currentText()]
        self.config_dict['pid_inp'] = inp_chan.get_pv_name()
        return self.config_dict