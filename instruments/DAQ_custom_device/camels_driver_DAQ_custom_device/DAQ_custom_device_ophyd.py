from CAMELS.bluesky_handling.daq_signal import DAQ_Signal_Input, DAQ_Signal_Output

from ophyd import Component as Cpt
from ophyd import Device

import time as ttime


class Custom_DAQ_Device(Device):
    in1 = Cpt(DAQ_Signal_Input, name='in1')
    in2 = Cpt(DAQ_Signal_Input, name='in2')
    in3 = Cpt(DAQ_Signal_Input, name='in3')
    in4 = Cpt(DAQ_Signal_Input, name='in4')
    in5 = Cpt(DAQ_Signal_Input, name='in5')
    in6 = Cpt(DAQ_Signal_Input, name='in6')
    in7 = Cpt(DAQ_Signal_Input, name='in7')
    in8 = Cpt(DAQ_Signal_Input, name='in8')
    out1 = Cpt(DAQ_Signal_Output, name='out1')
    out2 = Cpt(DAQ_Signal_Output, name='out2')
    out3 = Cpt(DAQ_Signal_Output, name='out3')
    out4 = Cpt(DAQ_Signal_Output, name='out4')
    out5 = Cpt(DAQ_Signal_Output, name='out5')
    out6 = Cpt(DAQ_Signal_Output, name='out6')
    out7 = Cpt(DAQ_Signal_Output, name='out7')
    out8 = Cpt(DAQ_Signal_Output, name='out8')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None,
                 component_setups=None, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        self.component_setups = component_setups or {}
        if component_setups:
            comps = list(self.component_names)
            for comp in self.component_names:
                if comp not in self.component_setups.keys():
                    comps.remove(comp)
                    break
            self.component_names = tuple(comps)

        self.comps = {'in1': self.in1, 'in2': self.in2, 'in3': self.in3,
                 'in4': self.in4, 'in5': self.in5, 'in6': self.in6,
                 'in7': self.in7, 'in8': self.in8,
                 'out1': self.out1, 'out2': self.out2, 'out3': self.out3,
                 'out4': self.out4, 'out5': self.out5, 'out6': self.out6,
                 'out7': self.out7, 'out8': self.out8}
        for nam, info in self.component_setups.items():
            comp = self.comps[nam]
            comp.setup_line(info['line_name'], digital=info['digital'],
                            terminal_config=info['terminal_config'],
                            minV=info['minV'], maxV=info['maxV'])


    def finalize_steps(self):
        for nam in self.component_setups:
            self.comps[nam].close_task()



    def wait_for_connection(self, all_signals=False, timeout=2.0):
        self.wait_conn_sub(all_signals, timeout)

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
            if name not in self.component_setups.keys():
                use = False
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
