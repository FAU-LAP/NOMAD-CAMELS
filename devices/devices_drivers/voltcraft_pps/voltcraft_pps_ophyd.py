from ophyd import EpicsSignal, Device
from ophyd import Component as Cpt


class Voltcraft_PPS(Device):
    setV = Cpt(EpicsSignal, 'setV')
    setI = Cpt(EpicsSignal, 'setI')
    setP = Cpt(EpicsSignal, 'setP')
    setR = Cpt(EpicsSignal, 'setR', kind='config')
    outputMode = Cpt(EpicsSignal, 'outputMode', kind='config')
