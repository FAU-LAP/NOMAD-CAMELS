from ophyd import EpicsSignal, Device
from ophyd import Component as Cpt


class Voltcraft_PPS(Device):
    setV = Cpt(EpicsSignal, 'setV', metadata={'units': 'V'})
    setI = Cpt(EpicsSignal, 'setI', metadata={'units': 'A'})
    setP = Cpt(EpicsSignal, 'setP', metadata={'units': 'W'})
    setR = Cpt(EpicsSignal, 'setR', kind='config', metadata={'units': 'Ohm'})
    outputMode = Cpt(EpicsSignal, 'outputMode', kind='config')
