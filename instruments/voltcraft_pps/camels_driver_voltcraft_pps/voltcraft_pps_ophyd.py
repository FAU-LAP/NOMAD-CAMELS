from ophyd import EpicsSignal, Device
from ophyd import Component as Cpt

import numpy as np

from camels_support_visa_signal import VISA_Signal_Write, VISA_Device

from CAMELS.bluesky_handling.custom_function_signal import Custom_Function_Signal


def volt_func(val):
    val *= 10
    return f'VOLT{val:03d}'

def curr_func(val):
    val *= 10
    return f'CURR{val:03d}'


class Voltcraft_PPS(VISA_Device):
    setV = Cpt(VISA_Signal_Write, 'setV', put_conv_function=volt_func)
    setI = Cpt(VISA_Signal_Write, name='setI', put_conv_function=curr_func)
    setP = Cpt(VISA_Signal_Write, 'setP')
    setR = Cpt(Custom_Function_Signal, 'setR', kind='config')
    # outputMode = Cpt(EpicsSignal, 'outputMode', kind='config')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        self.resistance = 0
        self.setR.put_function = self.set_resistance
        self.setP.put_conv_function = self.set_power

    def set_power(self, val):
        val = np.sqrt(val, self.resistance) * 10
        return volt_func(val)

    def set_resistance(self, val):
        self.resistance = val



class Voltcraft_PPS_EPICS(Device):
    setV = Cpt(EpicsSignal, 'setV')
    setI = Cpt(EpicsSignal, 'setI')
    setP = Cpt(EpicsSignal, 'setP')
    setR = Cpt(EpicsSignal, 'setR', kind='config')
    # outputMode = Cpt(EpicsSignal, 'outputMode', kind='config')
