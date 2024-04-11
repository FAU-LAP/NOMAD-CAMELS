from .test_dynamic_ophyd import Test_Dynamic
from .test_dynamic_ophyd import make_ophyd_class

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="test_dynamic",
            virtual=False,
            tags=[],
            directory="test_dynamic",
            ophyd_device=None,
            ophyd_class_name="make_ophyd_instance",
            **kwargs,
        )
        self.settings["channel_numbers"] = "3"  # default number of channels should be 3

    def update_driver(self):
        if (
            not "channel_numbers" in self.settings
            or not self.settings["channel_numbers"]
        ):
            return
        # make_ophyd_class is a function that returns a class with components that are generated at runtime
        # here we pass the channel_numbers to the make_ophyd_class which creates the class
        self.ophyd_class = make_ophyd_class(self.settings["channel_numbers"])
        # now we create an instance of the class
        # name="test" prevents the instrument driver from actually trying to connect directly to the physical instrument
        self.ophyd_instance = self.ophyd_class(
            channel_numbers=self.settings["channel_numbers"], name="test"
        )
        config, passive_config = get_configs_from_ophyd(self.ophyd_instance)
        for key, value in config.items():
            if key not in self.config:
                self.config[key] = value
        for key, value in passive_config.items():
            if key not in self.passive_config:
                self.passive_config[key] = value

    def get_channels(self):
        self.update_driver()
        return super().get_channels()


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        comboBoxes = {"channel_numbers": ["1", "2", "3", "4", "5"]}
        super().__init__(
            parent,
            "test_dynamic",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboBoxes,
        )
        self.load_settings()
    



def get_configs_from_ophyd(ophyd_instance):
    config = {}
    passive_config = {}
    for comp in ophyd_instance.walk_components():
        name = comp.item.attr
        dev_class = comp.item.cls
        if name in ophyd_instance.configuration_attrs:
            if device_class.check_output(dev_class):
                config.update({f"{name}": 0})
            else:
                passive_config.update({f"{name}": 0})
    return config, passive_config
