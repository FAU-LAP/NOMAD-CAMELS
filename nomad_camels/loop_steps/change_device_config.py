import importlib
from PySide6.QtWidgets import QComboBox, QLabel

from nomad_camels.main_classes.loop_step import Loop_Step, Loop_Step_Config
from nomad_camels.main_classes.device_class import Device_Config_Sub

from nomad_camels.utility import variables_handling


class Change_DeviceConf(Loop_Step):
    """
    With this step, one can change the config-attributes of a device.

    Attributes
    ----------
    device : str
        The name of the device that has the config changed.
    config_dict : dict
        The dictionary with the new config-attributes of the device.
    """

    def __init__(self, name="", parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = "Change Device Config"
        if step_info is None:
            step_info = {}
        self.device = step_info["device"] if "device" in step_info else ""
        self.config_dict = (
            step_info["config_dict"] if "config_dict" in step_info else {}
        )
        self.settings_dict = (
            step_info["settings_dict"] if "settings_dict" in step_info else {}
        )

    def update_used_devices(self):
        """Includes self.device to the used devices."""
        if self.device == "advanced configuration":
            self.used_devices = []
            for conf in self.config_dict["channel"]:
                dev = variables_handling.config_channels[conf].device
                if dev not in self.used_devices:
                    self.used_devices.append(dev)
        else:
            self.used_devices = [self.device]

    def get_protocol_string(self, n_tabs=1):
        """Creates an instance of `self.device` and uses `self.config_dict` to
        get a complete config_dict from the instance.
        The string consists of calling `dev.configure(config)`, where config is
        the config_dict."""
        tabs = "\t" * n_tabs
        dev_name = self.device
        protocol_string = super().get_protocol_string(n_tabs)
        if dev_name != "advanced configuration":
            device = variables_handling.devices[dev_name]
            dev_type = device.name
            py_package = importlib.import_module(
                f"nomad_camels_driver_{dev_type}.{dev_type}"
            )
            dev_instance = py_package.subclass()
            dev_instance.config = self.config_dict
            config_dict = dev_instance.get_config()
            extra_config = {}
            non_strings = []
            for key in config_dict:
                if key.startswith("!non_string!_"):
                    extra_config[key.replace("!non_string!_", "")] = config_dict[key]
                    non_strings.append(key)
            for s in non_strings:
                config_dict.pop(s)
            config_dict.update(extra_config)
            protocol_string += f"{tabs}config = {config_dict}\n"
            protocol_string += f'{tabs}devs["{self.device}"].configure(config)\n'
        else:
            self.update_used_devices()
            for dev in self.used_devices:
                protocol_string += f"{tabs}config_dict = " + "{"
                for i, conf in enumerate(self.config_dict["channel"]):
                    dev_name, conf_name = variables_handling.config_channels[
                        conf
                    ].name.split(".")
                    if dev_name != dev:
                        continue
                    if conf not in variables_handling.config_channels:
                        raise Exception(
                            f"Trying to configure {conf} in {self.full_name}, but it does not exist!"
                        )
                    val = self.config_dict["value"][i].replace('"', '\\"')
                    protocol_string += f'"{conf_name}": eva.eval("{val}"), '
                protocol_string = protocol_string[:-2] + "}\n"
                protocol_string += f'{tabs}devs["{dev}"].configure(config_dict)\n'
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """Includes the configured device in the short string."""
        short_string = super().get_protocol_short_string(n_tabs)
        short_string = f"{short_string[:-1]} - {self.device}\n"
        return short_string


class Change_DeviceConf_Config(Loop_Step_Config):
    """ """

    def __init__(self, loop_step: Change_DeviceConf, parent=None):
        super().__init__(parent, loop_step)
        self.loop_step = loop_step
        label_dev = QLabel("Device:")
        self.comboBox_device = QComboBox()
        devs = list(variables_handling.devices.keys()) + ["advanced configuration"]
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
        """ """
        dev_name = self.comboBox_device.currentText()
        if not dev_name:
            return
        if dev_name == "advanced configuration":
            from nomad_camels.ui_widgets.channels_check_table import (
                Channels_Check_Table,
            )

            if self.loop_step.device == "advanced configuration":
                config_widge = Channels_Check_Table(
                    self,
                    ["set", "config", "value"],
                    True,
                    self.loop_step.config_dict,
                    [2],
                    use_configs=True,
                )
            else:
                config_widge = Channels_Check_Table(
                    self,
                    ["set", "config", "value"],
                    True,
                    {"channel": [], "value": []},
                    [2],
                    use_configs=True,
                )
        else:
            device = variables_handling.devices[dev_name]
            dev_type = device.name
            py_package = importlib.import_module(
                f"nomad_camels_driver_{dev_type}.{dev_type}"
            )
            if dev_name == self.loop_step.device:
                settings = self.loop_step.settings_dict
                config = self.loop_step.config_dict
            else:
                settings = dict(device.settings)
                config = dict(device.config)
            try:
                config_widge = py_package.subclass_config_sub(
                    parent=self, settings_dict=settings, config_dict=config
                )
            except AttributeError:
                try:
                    widge = py_package.subclass_config(
                        parent=self, settings_dict=settings, config_dict=config
                    )
                    config_widge = widge.sub_widget
                except AttributeError:
                    config_widge = Device_Config_Sub(parent=self)
        self.layout().replaceWidget(self.config_widget, config_widge)
        self.config_widget.deleteLater()
        self.config_widget = config_widge

    def update_step_config(self):
        """ """
        super().update_step_config()
        dev_name = self.comboBox_device.currentText()
        self.loop_step.device = dev_name
        if dev_name == "advanced configuration":
            self.loop_step.config_dict = self.config_widget.get_info()
        else:
            self.loop_step.config_dict = self.config_widget.get_config()
            self.loop_step.settings_dict = self.config_widget.get_settings()
