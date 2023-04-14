from ophyd import EpicsSignal, Device
from ophyd import Component as Cpt

import numpy as np

from nomad-camels_support_visa_signal import VISA_Device

from nomad-camels.bluesky_handling.custom_function_signal import Custom_Function_Signal


class Voltcraft_PPS(VISA_Device):
    setV = Cpt(Custom_Function_Signal, name='setV')
    setI = Cpt(Custom_Function_Signal, name='setI')
    setP = Cpt(Custom_Function_Signal, name='setP')
    setR = Cpt(Custom_Function_Signal, name='setR', kind='config')
    # outputMode = Cpt(EpicsSignal, 'outputMode', kind='config')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        self.resistance = 0
        self.setR.put_function = self.set_resistance
        self.setI.put_function = self.curr_func
        self.setP.put_function = self.set_power
        self.setV.put_function = self.volt_func
        maxes = self.visa_instrument.query('GMAX')
        self.visa_instrument.read()
        maxV = int(maxes[:3])
        maxI = int(maxes[3:6])
        self.visa_instrument.query(f'SOVP{maxV:03d}')
        self.visa_instrument.query(f'SOCP{maxI:03d}')

    def volt_func(self, val):
        val *= 10
        val = int(val)
        self.visa_instrument.query(f'VOLT{val:03d}')

    def curr_func(self, val):
        val *= 100
        val = int(val)
        self.visa_instrument.query(f'CURR{val:03d}')

    def set_power(self, val):
        val = np.sqrt(val * self.resistance)
        self.volt_func(val)

    def set_resistance(self, val):
        self.resistance = val



class Voltcraft_PPS_EPICS(Device):
    setV = Cpt(EpicsSignal, 'setV')
    setI = Cpt(EpicsSignal, 'setI')
    setP = Cpt(EpicsSignal, 'setP')
    setR = Cpt(EpicsSignal, 'setR', kind='config')
    # outputMode = Cpt(EpicsSignal, 'outputMode', kind='config')
