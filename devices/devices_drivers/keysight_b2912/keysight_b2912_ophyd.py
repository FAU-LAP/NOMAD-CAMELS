from ophyd import EpicsSignal, EpicsSignalRO, Device
from ophyd import Component as Cpt

from bluesky_handling import TriggerEpicsSignalRO


class Keysight_B2912(Device):
    mesDCV = Cpt(TriggerEpicsSignalRO, 'mesDCV')
    mesDCI = Cpt(TriggerEpicsSignalRO, 'mesDCI')
    mesACV = Cpt(TriggerEpicsSignalRO, 'mesACV')
    mesACI = Cpt(TriggerEpicsSignalRO, 'mesACI')
    mesR = Cpt(TriggerEpicsSignalRO, 'mesR')
    mesR4w = Cpt(TriggerEpicsSignalRO, 'mesR4w')
    idn = Cpt(EpicsSignalRO, 'idn', kind='config')
    nPLC = Cpt(EpicsSignal, 'nPLC', kind='config')
