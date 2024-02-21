import copy

from nomad_camels.main_classes import device_class
from nomad_camels.utility import variables_handling

from .set_panel_device_ophyd import Set_Panel_Device


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="set_panel_device",
            virtual=True,
            ophyd_device=Set_Panel_Device,
            ophyd_class_name="Set_Panel_Device",
            **kwargs,
        )

    def get_necessary_devices(self):
        channels = self.settings["channel_names"]
        devs = []
        for chan in channels:
            devs.append(variables_handling.channels[chan].device)
        devs = list(set(devs))
        return devs

    def get_channels(self):
        if "group_names" in self.settings:
            channels = copy.deepcopy(super().get_channels())
            n = len(self.settings["group_names"])
            chans = {}
            for i, (nam, val) in enumerate(channels.items()):
                if i >= n:
                    break
                chans[nam] = val
            return chans
        return []


class subclass_config(device_class.Device_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
        **kwargs,
    ):
        super().__init__(
            parent,
            "set_panel_device",
            data,
            settings_dict,
            config_dict,
            additional_info,
            **kwargs,
        )
