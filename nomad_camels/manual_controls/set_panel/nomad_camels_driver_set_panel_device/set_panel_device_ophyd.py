from ophyd import Component as Cpt
from ophyd import Device

from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal
from nomad_camels.utility import device_handling

import time as ttime


class Set_Panel_Device(Device):
    group_1 = Cpt(Custom_Function_Signal, name="group_1")
    group_2 = Cpt(Custom_Function_Signal, name="group_2")
    group_3 = Cpt(Custom_Function_Signal, name="group_3")
    group_4 = Cpt(Custom_Function_Signal, name="group_4")
    group_5 = Cpt(Custom_Function_Signal, name="group_5")
    group_6 = Cpt(Custom_Function_Signal, name="group_6")
    group_7 = Cpt(Custom_Function_Signal, name="group_7")
    group_8 = Cpt(Custom_Function_Signal, name="group_8")
    group_9 = Cpt(Custom_Function_Signal, name="group_9")
    group_10 = Cpt(Custom_Function_Signal, name="group_10")
    group_11 = Cpt(Custom_Function_Signal, name="group_11")
    group_12 = Cpt(Custom_Function_Signal, name="group_12")
    group_13 = Cpt(Custom_Function_Signal, name="group_13")
    group_14 = Cpt(Custom_Function_Signal, name="group_14")
    group_15 = Cpt(Custom_Function_Signal, name="group_15")
    group_16 = Cpt(Custom_Function_Signal, name="group_16")
    group_17 = Cpt(Custom_Function_Signal, name="group_17")
    group_18 = Cpt(Custom_Function_Signal, name="group_18")
    group_19 = Cpt(Custom_Function_Signal, name="group_19")
    group_20 = Cpt(Custom_Function_Signal, name="group_20")

    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        set_vals=None,
        group_names=None,
        channels=None,
        **kwargs,
    ):
        if "channel_names" in kwargs:
            kwargs.pop("channel_names")
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs,
        )
        self.set_vals = set_vals or {}
        self.group_names = group_names or []
        self.channels = channels or {}
        self.order = [
            self.group_1,
            self.group_2,
            self.group_3,
            self.group_4,
            self.group_5,
            self.group_6,
            self.group_7,
            self.group_8,
            self.group_9,
            self.group_10,
            self.group_11,
            self.group_12,
            self.group_13,
            self.group_14,
            self.group_15,
            self.group_16,
            self.group_17,
            self.group_18,
            self.group_19,
            self.group_20,
        ]
        for i, group in enumerate(self.order):
            group.put_function = lambda x, n=i: self.set_value(x, n)

        comps = list(self.component_names)
        for i, comp in enumerate(self.component_names):
            if i <= len(self.group_names):
                continue
            comps.remove(comp)
        self.component_names = tuple(comps)

    def set_value(self, i, n):
        for j, channel in enumerate(self.set_vals[n][i]["channel"]):
            value = self.set_vals[n][i]["value"][j]
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    try:
                        value = bool(value)
                    except ValueError:
                        pass
            chan = self.channels[channel]
            if isinstance(chan, str):
                chan = device_handling.get_channel_from_string(chan)
            chan.put(value)
