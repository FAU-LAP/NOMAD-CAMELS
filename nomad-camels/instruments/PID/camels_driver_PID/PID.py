from .PID_ophyd import PID_Controller
from .PID_manual_control import PID_manual_control, PID_Manual_Control_Config

from .PID_config_sub import subclass_config_sub

from nomad-camels.main_classes import device_class
import CAMELS.main_classes.loop_step as steps

from PySide6.QtWidgets import QComboBox

from nomad-camels.utility import variables_handling

default_pid_val_table = {'setpoint': [0],
                         'kp': [1],
                         'ki': [1],
                         'kd': [1],
                         'max_value': [2],
                         'min_value': [-2],
                         'bias': [0],
                         'stability-delta': [0.5],
                         'stability-time': [10]}

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        files = ['']
        req = ['']
        super().__init__(name='PID', virtual=True, tags=['PID', 'control'], files=files, directory='PID', ophyd_device=PID_Controller, ophyd_class_name='PID_Controller', requirements=req, **kwargs)
        self.settings['pid_val_table'] = default_pid_val_table
        self.settings['auto_pid'] = True
        self.settings['show_plot'] = True
        self.config['dt'] = 0.5


        self.controls = {'PID_manual_control': [PID_manual_control,
                                                PID_Manual_Control_Config]}

    # def get_additional_string(self):
    #     inp_pv = self.config['pid_inp'].split(' ')[0]
    #     input_chan = measurement_channel.from_pv_name(inp_pv)
    #     input_chan = variables_handling.channels[input_chan].name
    #     add_string = f'\t\t{input_chan}.triggering = False\n'
    #     add_string += f'\t\tcaput("{inp_pv}.SCAN", {self.config["pid_scan"]})\n'
    #     return add_string

    def get_special_steps(self):
        return {'PID wait for stable': [PID_wait_for_stable, PID_wait_for_stable_config]}

    def get_substitutions_string(self, ioc_name:str, communication:str):
        substring = f'file "db/{self.name}.db" {{\n'
        substring += f'    {{SETUP = "{ioc_name}", device = "{self.custom_name}"}}\n'
        substring += '}'
        return substring

    def get_necessary_devices(self):
        inp_dev = variables_handling.channels[self.settings['read_signal_name']].device
        out_dev = variables_handling.channels[self.settings['set_signal_name']].device
        devs = list({inp_dev, out_dev})
        return devs

    def get_config(self):
        if 'pid_val_table' not in self.settings:
            return super().get_config()
        for c in ['kp', 'ki', 'kd', 'min_value', 'max_value']:
            if c in self.settings['pid_val_table']:
                val = self.settings['pid_val_table'][c]
                try:
                    self.config[c] = val[0]
                except:
                    self.config[c] = val
        return super().get_config()



class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None):
        super().__init__(parent, 'PID_Controller', data, settings_dict,
                         config_dict, ioc_dict, additional_info)
        # self.comboBox_connection_type.addItem()
        # self.layout().removeWidget(self.comboBox_connection_type)
        # self.comboBox_connection_type.deleteLater()
        # self.layout().removeWidget(self.label_connection)
        # self.label_connection.deleteLater()
        self.sub_widget = subclass_config_sub(settings_dict=settings_dict, parent=self, config_dict=config_dict)
        self.layout().addWidget(self.sub_widget, 5, 0, 1, 5)
        self.load_settings()

    def get_settings(self):
        return self.sub_widget.get_settings()

    def get_config(self):
        return self.sub_widget.get_config()

    # def get_ioc_settings(self):
    #     self.ioc_settings.clear()
    #     self.ioc_settings.update({'use_local_ioc': self.checkBox_use_local_ioc.isChecked(),
    #                               'ioc_name': self.lineEdit_ioc_name.text()})
    #     return self.ioc_settings




class PID_wait_for_stable(steps.Loop_Step):
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
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
        protocol_string = super().get_protocol_string(n_tabs)
        # protocol_string += f'{tabs}stable_time = datetime.timedelta(0)\n'
        protocol_string += f'{tabs}delta_t = devs["{self.pid}"].dt.get()\n'
        # protocol_string += f'{tabs}starttime = datetime.datetime.now()\n'
        # protocol_string += f'{tabs}dt = datetime.timedelta(seconds=devs["{self.pid}"].stability_time)\n'
        protocol_string += f'{tabs}while not devs["{self.pid}"].pid_stable.get():\n'
        # protocol_string += f'{tabs}\tprint(devs["{self.pid}"].pid_val.just_readback(), devs["{self.pid}"].pid_cval.just_readback())\n'
        protocol_string += f'{tabs}\tyield from bps.sleep(delta_t)\n'
        # protocol_string += f'{tabs}\tif np.abs(devs["{self.pid}"].pid_val.just_readback() - devs["{self.pid}"].pid_cval.get()) > devs["{self.pid}"].stability_delta:\n'
        # protocol_string += f'{tabs}\t\tstable_time = datetime.timedelta(0)\n'
        # protocol_string += f'{tabs}\t\tstarttime = datetime.datetime.now()\n'
        # protocol_string += f'{tabs}\telse:\n'
        # protocol_string += f'{tabs}\t\tstable_time += datetime.datetime.now() - starttime\n'
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
