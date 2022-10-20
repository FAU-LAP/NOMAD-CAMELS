from ophyd import EpicsSignal, EpicsSignalRO, Device
from ophyd import Component as Cpt

from bluesky_handling import TriggerEpicsSignalRO

from bluesky_handling.visa_signal import VISA_Signal_Write, VISA_Signal_Read, VISA_Device


class Agilent_34401_EPICS(Device):
    mesDCV = Cpt(TriggerEpicsSignalRO, 'mesDCV')
    mesDCI = Cpt(TriggerEpicsSignalRO, 'mesDCI')
    mesACV = Cpt(TriggerEpicsSignalRO, 'mesACV')
    mesACI = Cpt(TriggerEpicsSignalRO, 'mesACI')
    mesR = Cpt(TriggerEpicsSignalRO, 'mesR')
    mesR4w = Cpt(TriggerEpicsSignalRO, 'mesR4w')
    idn = Cpt(EpicsSignalRO, 'idn', kind='config')
    nPLC = Cpt(EpicsSignal, 'nPLC', kind='config')



class Agilent_34401(VISA_Device):
    mesDCV = Cpt(VISA_Signal_Read, name='mesDCV', query_text="MEAS:VOLT:DC?")
    mesDCI = Cpt(VISA_Signal_Read, name='mesDCI', query_text="MEAS:CURR:DC?")
    mesACV = Cpt(VISA_Signal_Read, name='mesACV', query_text="MEAS:VOLT:AC?")
    mesACI = Cpt(VISA_Signal_Read, name='mesACI', query_text="MEAS:CURR:AC?")
    mesR = Cpt(VISA_Signal_Read, name='mesR', query_text="MEAS:RES?")
    mesR4w = Cpt(VISA_Signal_Read, name='mesR4w', query_text="MEAS:FRES?")
    idn = Cpt(VISA_Signal_Read, name='idn', kind='config', query_text='*IDN?')
    nPLC = Cpt(VISA_Signal_Write, name='nPLC', kind='config')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, **kwargs)
