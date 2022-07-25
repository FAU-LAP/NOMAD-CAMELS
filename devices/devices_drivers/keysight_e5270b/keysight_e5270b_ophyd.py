from ophyd import EpicsSignal, EpicsSignalRO, Device
from ophyd import Component as Cpt

from bluesky_handling import TriggerEpicsSignalRO
import time as ttime



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

    setV2 = Cpt(EpicsSignal, 'setV2')
    setI2 = Cpt(EpicsSignal, 'setI2')
    mesI2 = Cpt(TriggerEpicsSignalRO, 'mesI2')
    mesV2 = Cpt(TriggerEpicsSignalRO, 'mesV2')
    enable2 = Cpt(EpicsSignal, 'enable2')
    measMode2 = Cpt(EpicsSignal, 'measMode2', kind='config')
    currComp2 = Cpt(EpicsSignal, 'currComp2', kind='config')
    voltComp2 = Cpt(EpicsSignal, 'voltComp2', kind='config')
    VoutRange2 = Cpt(EpicsSignal, 'VoutRange2', kind='config')
    IoutRange2 = Cpt(EpicsSignal, 'IoutRange2', kind='config')
    VmeasRange2 = Cpt(EpicsSignal, 'VmeasRange2', kind='config')
    ImeasRange2 = Cpt(EpicsSignal, 'ImeasRange2', kind='config')
    setADC2 = Cpt(EpicsSignal, 'setADC2', kind='config')
    outputFilter2 = Cpt(EpicsSignal, 'outputFilter2', kind='config')

    setV3 = Cpt(EpicsSignal, 'setV3')
    setI3 = Cpt(EpicsSignal, 'setI3')
    mesI3 = Cpt(TriggerEpicsSignalRO, 'mesI3')
    mesV3 = Cpt(TriggerEpicsSignalRO, 'mesV3')
    enable3 = Cpt(EpicsSignal, 'enable3')
    measMode3 = Cpt(EpicsSignal, 'measMode3', kind='config')
    currComp3 = Cpt(EpicsSignal, 'currComp3', kind='config')
    voltComp3 = Cpt(EpicsSignal, 'voltComp3', kind='config')
    VoutRange3 = Cpt(EpicsSignal, 'VoutRange3', kind='config')
    IoutRange3 = Cpt(EpicsSignal, 'IoutRange3', kind='config')
    VmeasRange3 = Cpt(EpicsSignal, 'VmeasRange3', kind='config')
    ImeasRange3 = Cpt(EpicsSignal, 'ImeasRange3', kind='config')
    setADC3 = Cpt(EpicsSignal, 'setADC3', kind='config')
    outputFilter3 = Cpt(EpicsSignal, 'outputFilter3', kind='config')

    setV4 = Cpt(EpicsSignal, 'setV4')
    setI4 = Cpt(EpicsSignal, 'setI4')
    mesI4 = Cpt(TriggerEpicsSignalRO, 'mesI4')
    mesV4 = Cpt(TriggerEpicsSignalRO, 'mesV4')
    enable4 = Cpt(EpicsSignal, 'enable4')
    measMode4 = Cpt(EpicsSignal, 'measMode4', kind='config')
    currComp4 = Cpt(EpicsSignal, 'currComp4', kind='config')
    voltComp4 = Cpt(EpicsSignal, 'voltComp4', kind='config')
    VoutRange4 = Cpt(EpicsSignal, 'VoutRange4', kind='config')
    IoutRange4 = Cpt(EpicsSignal, 'IoutRange4', kind='config')
    VmeasRange4 = Cpt(EpicsSignal, 'VmeasRange4', kind='config')
    ImeasRange4 = Cpt(EpicsSignal, 'ImeasRange4', kind='config')
    setADC4 = Cpt(EpicsSignal, 'setADC4', kind='config')
    outputFilter4 = Cpt(EpicsSignal, 'outputFilter4', kind='config')

    setV5 = Cpt(EpicsSignal, 'setV5')
    setI5 = Cpt(EpicsSignal, 'setI5')
    mesI5 = Cpt(TriggerEpicsSignalRO, 'mesI5')
    mesV5 = Cpt(TriggerEpicsSignalRO, 'mesV5')
    enable5 = Cpt(EpicsSignal, 'enable5')
    measMode5 = Cpt(EpicsSignal, 'measMode5', kind='config')
    currComp5 = Cpt(EpicsSignal, 'currComp5', kind='config')
    voltComp5 = Cpt(EpicsSignal, 'voltComp5', kind='config')
    VoutRange5 = Cpt(EpicsSignal, 'VoutRange5', kind='config')
    IoutRange5 = Cpt(EpicsSignal, 'IoutRange5', kind='config')
    VmeasRange5 = Cpt(EpicsSignal, 'VmeasRange5', kind='config')
    ImeasRange5 = Cpt(EpicsSignal, 'ImeasRange5', kind='config')
    setADC5 = Cpt(EpicsSignal, 'setADC5', kind='config')
    outputFilter5 = Cpt(EpicsSignal, 'outputFilter5', kind='config')

    setV6 = Cpt(EpicsSignal, 'setV6')
    setI6 = Cpt(EpicsSignal, 'setI6')
    mesI6 = Cpt(TriggerEpicsSignalRO, 'mesI6')
    mesV6 = Cpt(TriggerEpicsSignalRO, 'mesV6')
    enable6 = Cpt(EpicsSignal, 'enable6')
    measMode6 = Cpt(EpicsSignal, 'measMode6', kind='config')
    currComp6 = Cpt(EpicsSignal, 'currComp6', kind='config')
    voltComp6 = Cpt(EpicsSignal, 'voltComp6', kind='config')
    VoutRange6 = Cpt(EpicsSignal, 'VoutRange6', kind='config')
    IoutRange6 = Cpt(EpicsSignal, 'IoutRange6', kind='config')
    VmeasRange6 = Cpt(EpicsSignal, 'VmeasRange6', kind='config')
    ImeasRange6 = Cpt(EpicsSignal, 'ImeasRange6', kind='config')
    setADC6 = Cpt(EpicsSignal, 'setADC6', kind='config')
    outputFilter6 = Cpt(EpicsSignal, 'outputFilter6', kind='config')

    setV7 = Cpt(EpicsSignal, 'setV7')
    setI7 = Cpt(EpicsSignal, 'setI7')
    mesI7 = Cpt(TriggerEpicsSignalRO, 'mesI7')
    mesV7 = Cpt(TriggerEpicsSignalRO, 'mesV7')
    enable7 = Cpt(EpicsSignal, 'enable7')
    measMode7 = Cpt(EpicsSignal, 'measMode7', kind='config')
    currComp7 = Cpt(EpicsSignal, 'currComp7', kind='config')
    voltComp7 = Cpt(EpicsSignal, 'voltComp7', kind='config')
    VoutRange7 = Cpt(EpicsSignal, 'VoutRange7', kind='config')
    IoutRange7 = Cpt(EpicsSignal, 'IoutRange7', kind='config')
    VmeasRange7 = Cpt(EpicsSignal, 'VmeasRange7', kind='config')
    ImeasRange7 = Cpt(EpicsSignal, 'ImeasRange7', kind='config')
    setADC7 = Cpt(EpicsSignal, 'setADC7', kind='config')
    outputFilter7 = Cpt(EpicsSignal, 'outputFilter7', kind='config')

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
                 configuration_attrs=None, parent=None, use_channels=(), **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        self.use_channels = use_channels
        if use_channels:
            comps = list(self.component_names)
            for comp in self.component_names:
                for i in range(1, 9):
                    if i not in self.use_channels and str(i) in comp:
                        comps.remove(comp)
                        break
            self.component_names = tuple(comps)

    def wait_for_connection(self, all_signals=False, timeout=2.0):
        self.wait_conn_sub(all_signals, timeout)
        self.measMode1.put(1)

    def wait_conn_sub(self, all_signals=False, timeout=2.0):
        """Wait for signals to connect

        Parameters
        ----------
        all_signals : bool, optional
            Wait for all signals to connect (including lazy ones)
        timeout : float or None
            Overall timeout
        """
        signals = []
        for walk in self.walk_signals(include_lazy=all_signals):
            name = walk.item.attr_name
            use = True
            for i in range(1, 9):
                if i not in self.use_channels and str(i) in name:
                    use = False
                    break
            if use:
                signals.append(walk.item)

        pending_funcs = {
            dev: getattr(dev, '_required_for_connection', {})
            for name, dev in self.walk_subdevices(include_lazy=all_signals)
        }
        pending_funcs[self] = self._required_for_connection

        t0 = ttime.time()
        while timeout is None or (ttime.time() - t0) < timeout:
            connected = all(sig.connected for sig in signals)
            if connected and not any(pending_funcs.values()):
                return
            ttime.sleep(min((0.05, timeout / 10.0)))

        def get_name(sig):
            sig_name = f'{self.name}.{sig.dotted_name}'
            return (f'{sig_name} ({sig.pvname})' if hasattr(sig, 'pvname')
                    else sig_name)

        reasons = []
        unconnected = ', '.join(get_name(sig)
                                for sig in signals if not sig.connected)
        if unconnected:
            reasons.append(f'Failed to connect to all signals: {unconnected}')
        if any(pending_funcs.values()):
            pending = ', '.join(description.format(device=dev)
                                for dev, funcs in pending_funcs.items()
                                for obj, description in funcs.items())
            reasons.append(f'Pending operations: {pending}')
        raise TimeoutError('; '.join(reasons))


if __name__ == '__main__':
    e5270b = Keysight_E5270B('Default:', name='e5270b', channels=[1,8])
    comps = e5270b.walk_components()
    for comp in comps:
        print(comp)