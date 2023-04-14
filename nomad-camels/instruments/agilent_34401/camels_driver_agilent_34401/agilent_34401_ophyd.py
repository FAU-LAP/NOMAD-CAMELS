from ophyd import EpicsSignal, EpicsSignalRO, Device
from ophyd import Component as Cpt

from nomad-camels.bluesky_handling import TriggerEpicsSignalRO

from nomad-camels_support_visa_signal import VISA_Signal_Write, VISA_Signal_Read, VISA_Device


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
    mesDCV = Cpt(VISA_Signal_Read, name='mesDCV', query_text="MEAS:VOLT:DC?", metadata={'units': 'V'})
    mesDCI = Cpt(VISA_Signal_Read, name='mesDCI', query_text="MEAS:CURR:DC?", metadata={'units': 'A'})
    mesACV = Cpt(VISA_Signal_Read, name='mesACV', query_text="MEAS:VOLT:AC?", metadata={'units': 'V'})
    mesACI = Cpt(VISA_Signal_Read, name='mesACI', query_text="MEAS:CURR:AC?", metadata={'units': 'A'})
    mesR = Cpt(VISA_Signal_Read, name='mesR', query_text="MEAS:RES?", metadata={'units': 'Ohm'})
    mesR4w = Cpt(VISA_Signal_Read, name='mesR4w', query_text="MEAS:FRES?", metadata={'units': 'Ohm'})
    idn = Cpt(VISA_Signal_Read, name='idn', kind='config', query_text='*IDN?')
    nPLC = Cpt(VISA_Signal_Write, name='nPLC', kind='config')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 read_termination='\r\n', write_termination='\r\n',
                 baud_rate=9600, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, baud_rate=baud_rate,
                         write_termination=write_termination,
                         read_termination=read_termination, **kwargs)
