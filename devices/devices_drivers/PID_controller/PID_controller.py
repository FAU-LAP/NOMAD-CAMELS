import pandas as pd

from PID_controller.PID_controller_ophyd import PID_Controller

from main_classes import device_class
import main_classes.loop_step as steps
from utility.number_formatting import format_number

from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QComboBox, QLabel, QLineEdit

from utility.add_remove_table import AddRemoveTable
from utility.path_button_edit import Path_Button_Edit
from utility import variables_handling
from main_classes import measurement_channel


class subclass(device_class.Device):
    def __init__(self):
        files = ['PID_controller.db']
        req = ['std']
        super().__init__(name='PID_controller', virtual=True, tags=['PID', 'control'], files=files, directory='PID_controller', ophyd_device=PID_Controller, ophyd_class_name='PID_Controller', requirements=req)

    def get_additional_string(self):
        inp_pv = self.config['pid_inp'].split(' ')[0]
        input_chan = measurement_channel.from_pv_name(inp_pv)
        input_chan = variables_handling.channels[input_chan].name
        add_string = f'\t{input_chan}.triggering = False\n'
        add_string += f'\tcaput("{inp_pv}.SCAN", {self.config["pid_scan"]})\n'
        return add_string

    def get_special_steps(self):
        return {'PID wait for stable': [PID_wait_for_stable, PID_wait_for_stable_config]}


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


class PID_wait_for_stable(steps.Loop_Step):
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, **kwargs)
        self.step_type = 'PID wait for stable'
        if step_info is None:
            step_info = {}
        self.pid = step_info['pid'] if 'pid' in step_info else ''
        self.update_used_devices()

    def update_used_devices(self):
        if self.pid in variables_handling.devices:
            return [self.pid]
        return []

    def get_protocol_string(self, n_tabs=1):
        tabs = '\t' * n_tabs
        protocol_string = f'{tabs}print("starting loop_step {self.full_name}")\n'
        protocol_string += f'{tabs}stable_time = datetime.timedelta(0)\n'
        protocol_string += f'{tabs}delta_t = devs["{self.pid}"].pid_mdt.get()\n'
        protocol_string += f'{tabs}starttime = datetime.datetime.now()\n'
        protocol_string += f'{tabs}dt = datetime.timedelta(seconds=devs["{self.pid}"].stability_time)\n'
        protocol_string += f'{tabs}while stable_time < dt:\n'
        protocol_string += f'{tabs}\tprint(devs["{self.pid}"].pid_val.just_readback(), devs["{self.pid}"].pid_cval.just_readback())\n'
        protocol_string += f'{tabs}\tyield from bps.sleep(delta_t)\n'
        protocol_string += f'{tabs}\tif np.abs(devs["{self.pid}"].pid_val.just_readback() - devs["{self.pid}"].pid_cval.get()) > devs["{self.pid}"].stability_delta:\n'
        protocol_string += f'{tabs}\t\tstable_time = datetime.timedelta(0)\n'
        protocol_string += f'{tabs}\t\tstarttime = datetime.datetime.now()\n'
        protocol_string += f'{tabs}\telse:\n'
        protocol_string += f'{tabs}\t\tstable_time += datetime.datetime.now() - starttime\n'
        return protocol_string


class PID_wait_for_stable_config(steps.Loop_Step_Config):
    def __init__(self, loop_step:PID_wait_for_stable, parent=None):
        super().__init__(parent, loop_step)
        self.pid_box = QComboBox()
        self.layout().addWidget(self.pid_box, 1, 0)
        pids = []
        for name, device in variables_handling.devices.items():
            if isinstance(device, subclass):
                pids.append(name)
        self.pid_box.addItems(pids)
        if loop_step.pid in pids:
            self.pid_box.setCurrentText(loop_step.pid)

    def update_step_config(self):
        super().update_step_config()
        self.loop_step.pid = self.pid_box.currentText()
