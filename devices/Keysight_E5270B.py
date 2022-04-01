from ophyd import EpicsSignal, EpicsSignalRO, Device
from ophyd import Component as Cpt

from bluesky_handling import TriggerEpicsSignalRO


class Keysight_E5270B(Device):
    setV1 = Cpt(EpicsSignal, 'setV1')
    setI1 = Cpt(EpicsSignal, 'setI1')
    mesI1 = Cpt(TriggerEpicsSignalRO, 'mesI1')
    mesV1 = Cpt(TriggerEpicsSignalRO, 'mesV1')
    enable1 = Cpt(EpicsSignal, 'enable1')
    err = Cpt(TriggerEpicsSignalRO, 'err', no_mdel=True)
    currComp1 = Cpt(EpicsSignal, 'currComp1', kind='config')
    voltComp1 = Cpt(EpicsSignal, 'voltComp1', kind='config')
    VoutRange1 = Cpt(EpicsSignal, 'VoutRange1', kind='config')
    IoutRange1 = Cpt(EpicsSignal, 'IoutRange1', kind='config')
    VmeasRange1 = Cpt(EpicsSignal, 'VmeasRange1', kind='config')
    ImeasRange1 = Cpt(EpicsSignal, 'ImeasRange1', kind='config')
    setADC1 = Cpt(EpicsSignal, 'setADC1', kind='config')
    outputFilter1 = Cpt(EpicsSignal, 'outputFilter1', kind='config')
    speedADCPLC = Cpt(EpicsSignal, 'speedADCPLC', kind='config')
    speedADCmode = Cpt(EpicsSignal, 'speedADCmode', kind='config')
    resADCPLC = Cpt(EpicsSignal, 'resADCPLC', kind='config')
    resADCmode = Cpt(EpicsSignal, 'resADCmode', kind='config')
    idn = Cpt(EpicsSignalRO, 'idn', kind='config')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, configuration=None, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, **kwargs)


if __name__ == "__main__":
    import numpy as np
    from ophyd.signal import EpicsSignal, EpicsSignalRO
    from bluesky import RunEngine
    from bluesky.callbacks.best_effort import BestEffortCallback
    import bluesky.plan_stubs as bps
    from bluesky.utils import install_kicker
    from databroker import Broker
    RE = RunEngine({})
    bec = BestEffortCallback()
    RE.subscribe(bec)
    db = Broker.named("temp")
    RE.subscribe(db.insert)
    keysight_e5270b = Keysight_E5270B("Hall:e5270:", name="keysight_e5270b")
    keysight_e5270b.wait_for_connection()

    def test(devs):
        bps.open_run()
        bps.trigger_and_read(devs)
        bps.close_run()

    print(RE(test([keysight_e5270b.mesI1])))