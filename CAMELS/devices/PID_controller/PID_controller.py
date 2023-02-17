from PID_controller.PID_controller_ophyd import PID_Controller
from PID_controller.PID_controller_manual import PID_manual_control

from PID_controller.PID_controller_config_sub import subclass_config_sub

from main_classes import device_class
import main_classes.loop_step as steps

from PyQt5.QtWidgets import QComboBox

from utility import variables_handling
from main_classes import measurement_channel


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        files = ['PID_controller.db']
        req = ['std']
        super().__init__(name='PID_controller', virtual=True, tags=['PID', 'control'], files=files, directory='PID_controller', ophyd_device=PID_Controller, ophyd_class_name='PID_Controller', requirements=req, **kwargs)
        self.add_ons = {'manual control': [PID_manual_control, self]}

    def get_additional_string(self):
        inp_pv = self.config['pid_inp'].split(' ')[0]
        input_chan = measurement_channel.from_pv_name(inp_pv)
        input_chan = variables_handling.channels[input_chan].name
        add_string = f'\t\t{input_chan}.triggering = False\n'
        add_string += f'\t\tcaput("{inp_pv}.SCAN", {self.config["pid_scan"]})\n'
        return add_string

    def get_special_steps(self):
        return {'PID wait for stable': [PID_wait_for_stable, PID_wait_for_stable_config]}

    def get_substitutions_string(self, ioc_name:str, communication:str):
        substring = f'file "db/{self.name}.db" {{\n'
        substring += f'    {{SETUP = "{ioc_name}", device = "{self.custom_name}"}}\n'
        substring += '}'
        return substring



class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None):
        super().__init__(parent, 'PID_Controller', data, settings_dict,
                         config_dict, ioc_dict, additional_info)
        # self.comboBox_connection_type.addItem()
        self.layout().removeWidget(self.comboBox_connection_type)
        self.comboBox_connection_type.deleteLater()
        self.layout().removeWidget(self.label_connection)
        self.label_connection.deleteLater()
        self.sub_widget = subclass_config_sub(settings_dict=settings_dict, parent=self, config_dict=config_dict)
        self.layout().addWidget(self.sub_widget, 5, 0, 1, 5)
        self.load_settings()

    def get_settings(self):
        return self.sub_widget.get_settings()

    def get_config(self):
        return self.sub_widget.get_config()

    def get_ioc_settings(self):
        self.ioc_settings.clear()
        self.ioc_settings.update({'use_local_ioc': self.checkBox_use_local_ioc.isChecked(),
                                  'ioc_name': self.lineEdit_ioc_name.text()})
        return self.ioc_settings




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
