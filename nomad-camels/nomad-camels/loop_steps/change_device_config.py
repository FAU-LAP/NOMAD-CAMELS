import importlib
from PySide6.QtWidgets import QComboBox, QLabel

from nomad-camels.main_classes.loop_step import Loop_Step, Loop_Step_Config
from nomad-camels.main_classes.device_class import Device_Config_Sub

from nomad-camels.utility import variables_handling

class Change_DeviceConf(Loop_Step):
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = 'Change Device Config'
        if step_info is None:
            step_info = {}
        self.device = step_info['device'] if 'device' in step_info else ''
        self.config_dict = step_info['config_dict'] if 'config_dict' in step_info else {}
        self.settings_dict = step_info['settings_dict'] if 'settings_dict' in step_info else {}

    def update_used_devices(self):
        self.used_devices = [self.device]

    def get_protocol_string(self, n_tabs=1):
        tabs = '\t' * n_tabs
        dev_name = self.device
        device = variables_handling.devices[dev_name]
        dev_type = device.name
        py_package = importlib.import_module(f'{dev_type}.{dev_type}')
        dev_instance = py_package.subclass()
        dev_instance.config = self.config_dict
        config_dict = dev_instance.get_config()
        protocol_string = super().get_protocol_string(n_tabs)
        protocol_string += f'{tabs}config = {config_dict}\n'
        protocol_string += f'{tabs}devs["{self.device}"].configure(config)\n'
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        short_string = super().get_protocol_short_string(n_tabs)
        short_string = f'{short_string[:-1]} - {self.device}\n'
        return short_string


class Change_DeviceConf_Config(Loop_Step_Config):
    def __init__(self, loop_step:Change_DeviceConf, parent=None):
        super().__init__(parent, loop_step)
        self.loop_step = loop_step
        label_dev = QLabel('Device:')
        self.comboBox_device = QComboBox()
        devs = variables_handling.devices.keys()
        self.comboBox_device.addItems(devs)
        if loop_step.device in devs:
            self.comboBox_device.setCurrentText(loop_step.device)

        self.config_widget = Device_Config_Sub(parent=self)

        self.layout().addWidget(label_dev, 1, 0)
        self.layout().addWidget(self.comboBox_device, 1, 1)
        self.layout().addWidget(self.config_widget, 2, 0, 1, 5)
        self.comboBox_device.currentTextChanged.connect(self.device_changed)
        self.device_changed()

    def device_changed(self):
        dev_name = self.comboBox_device.currentText()
        device = variables_handling.devices[dev_name]
        dev_type = device.name
        py_package = importlib.import_module(f'{dev_type}.{dev_type}')
        if dev_name == self.loop_step.device:
            settings = self.loop_step.settings_dict
            config = self.loop_step.config_dict
        else:
            settings = dict(device.settings)
            config = dict(device.config)
        try:
            config_widge = py_package.subclass_config_sub(parent=self,
                                                          settings_dict=settings,
                                                          config_dict=config)
        except AttributeError:
            config_widge = Device_Config_Sub(parent=self)
        self.layout().replaceWidget(self.config_widget, config_widge)
        self.config_widget.deleteLater()
        self.config_widget = config_widge

    def update_step_config(self):
        super().update_step_config()
        self.loop_step.device = self.comboBox_device.currentText()
        self.loop_step.config_dict = self.config_widget.get_config()
        self.loop_step.settings_dict = self.config_widget.get_settings()
