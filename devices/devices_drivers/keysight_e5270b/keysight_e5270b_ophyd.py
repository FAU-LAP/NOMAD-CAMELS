from ophyd import EpicsSignal, EpicsSignalRO, Device
from ophyd import Component as Cpt

from bluesky_handling import TriggerEpicsSignalRO



class Keysight_E5270B(Device):
    setV1 = Cpt(EpicsSignal, 'setV1')
    setI1 = Cpt(EpicsSignal, 'setI1')
    mesI1 = Cpt(TriggerEpicsSignalRO, 'mesI1')
    mesV1 = Cpt(TriggerEpicsSignalRO, 'mesV1')
    enable1 = Cpt(EpicsSignal, 'enable1')
    measMode1 = Cpt(EpicsSignal, 'measMode1', kind='config')
    currComp1 = Cpt(EpicsSignal, 'currComp1', kind='config')
    voltComp1 = Cpt(EpicsSignal, 'voltComp1', kind='config')
    VoutRange1 = Cpt(EpicsSignal, 'VoutRange1', kind='config')
    IoutRange1 = Cpt(EpicsSignal, 'IoutRange1', kind='config')
    VmeasRange1 = Cpt(EpicsSignal, 'VmeasRange1', kind='config')
    ImeasRange1 = Cpt(EpicsSignal, 'ImeasRange1', kind='config')
    setADC1 = Cpt(EpicsSignal, 'setADC1', kind='config')
    outputFilter1 = Cpt(EpicsSignal, 'outputFilter1', kind='config')

    setV8 = Cpt(EpicsSignal, 'setV8')
    setI8 = Cpt(EpicsSignal, 'setI8')
    mesI8 = Cpt(TriggerEpicsSignalRO, 'mesI8')
    mesV8 = Cpt(TriggerEpicsSignalRO, 'mesV8')
    enable8 = Cpt(EpicsSignal, 'enable8')
    measMode8 = Cpt(EpicsSignal, 'measMode8', kind='config')
    currComp8 = Cpt(EpicsSignal, 'currComp8', kind='config')
    voltComp8 = Cpt(EpicsSignal, 'voltComp8', kind='config')
    VoutRange8 = Cpt(EpicsSignal, 'VoutRange8', kind='config')
    IoutRange8 = Cpt(EpicsSignal, 'IoutRange8', kind='config')
    VmeasRange8 = Cpt(EpicsSignal, 'VmeasRange8', kind='config')
    ImeasRange8 = Cpt(EpicsSignal, 'ImeasRange8', kind='config')
    setADC8 = Cpt(EpicsSignal, 'setADC8', kind='config')
    outputFilter8 = Cpt(EpicsSignal, 'outputFilter8', kind='config')

    speedADCPLC = Cpt(EpicsSignal, 'speedADCPLC', kind='config')
    speedADCmode = Cpt(EpicsSignal, 'speedADCmode', kind='config')
    resADCPLC = Cpt(EpicsSignal, 'resADCPLC', kind='config')
    resADCmode = Cpt(EpicsSignal, 'resADCmode', kind='config')
    idn = Cpt(EpicsSignalRO, 'idn', kind='config')
    err = Cpt(TriggerEpicsSignalRO, 'err', no_mdel=True)

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, **kwargs)

    def wait_for_connection(self, all_signals=False, timeout=2.0):
        super().wait_for_connection(all_signals=all_signals, timeout=timeout)
        self.measMode1.put(1)


if __name__ == '__main__':
    e5270b = Keysight_E5270B('Default:', name='e5270b', channels=[1,8])
    comps = e5270b.walk_components()
    for comp in comps:
        print(comp)