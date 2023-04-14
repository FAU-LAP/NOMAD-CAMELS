from nomad_camels_support_ni_daq_signal import DAQ_Signal_Input, DAQ_Signal_Output, \
    close_tasks
from ophyd import Component as Cpt
from ophyd.status import Status
from ophyd import Signal, Device

import time


class B_field_sign(Signal):
    def __init__(self,  name, value=0., timestamp=None, parent=None, labels=None, kind='hinted', tolerance=None, rtolerance=None, metadata=None, cl=None, attr_name='', reverse_time=25):
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent, labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance, metadata=metadata, cl=cl, attr_name=attr_name)
        self.reverse_time = reverse_time
        self.reverse = None
        self.polarity = None
        self.power_on = None
        self.power_off = None

    def change_setup(self, reverse_time=25, power_on=None, power_off=None,
                     reverse=None, polarity=None):
        self.reverse_time = reverse_time
        self.reverse = reverse
        self.polarity = polarity
        self.power_on = power_on
        self.power_off = power_off


    def set(self, value, **kwargs):
        if not isinstance(value, bool):
            value = True if value < 0 else False
        is_rev = self.polarity.get()
        if value == is_rev:
            st = Status(self)
            st.set_finished()
            return st
        for i in range(3):
            self.power_on.put(True)
            self.power_off.put(True)
            self.reverse.put(False)
            time.sleep(0.3)
            self.power_on.put(True)
            self.power_off.put(True)
            self.reverse.put(True)
            time.sleep(self.reverse_time)
            is_rev = self.polarity.get()
            if value == is_rev:
                break
        st = Status(self)
        st.set_finished()
        return st

    def read(self):
        pol = self.polarity.read()
        dictionary = pol[self.polarity.name]
        dictionary['value'] = -1 if dictionary['value'] > 0 else 1
        return {self.name: dictionary}

class B_field_enable(Signal):
    def __init__(self,  name, value=0., timestamp=None, parent=None, labels=None, kind='hinted', tolerance=None, rtolerance=None, metadata=None, cl=None, attr_name='', wait_time=5):
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent, labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance, metadata=metadata, cl=cl, attr_name=attr_name)
        self.wait_time = wait_time
        self.reverse = None
        self.power_read = None
        self.power_on = None
        self.power_off = None

    def change_setup(self, wait_time=5, power_on=None, power_off=None,
                     reverse=None, power_read=None):
        self.wait_time = wait_time
        self.reverse = reverse
        self.power_read = power_read
        self.power_on = power_on
        self.power_off = power_off

    def set(self, value, **kwargs):
        if not isinstance(value, bool):
            value = True if value > 0 else False
        is_on = self.power_read.get()
        if value == is_on:
            st = Status(self)
            st.set_finished()
            return st
        for i in range(3):
            self.power_on.put(not value)
            self.power_off.put(value)
            self.reverse.put(True)
            time.sleep(0.3)
            self.power_on.put(True)
            self.power_off.put(True)
            self.reverse.put(True)
            time.sleep(self.wait_time)
            is_on = self.power_read.get()
            if value == is_on:
                break
        st = Status(self)
        st.set_finished()
        return st

    def read(self):
        power = self.power_read.read()
        dictionary = power[self.power_read.name]
        return {self.name: dictionary}


class Bruker_Magnet_NI_DAQ(Device):
    power_read = Cpt(DAQ_Signal_Input, name='power_read', digital=True,
                     kind='config')
    polarity = Cpt(DAQ_Signal_Input, name='polarity', digital=True,
                   kind='config')
    power_on = Cpt(DAQ_Signal_Output, name='power_on', digital=True,
                   terminal_config='open_collector', kind='config')
    power_off = Cpt(DAQ_Signal_Output, name='power_off', digital=True,
                    terminal_config='open_collector', kind='config')
    reverse = Cpt(DAQ_Signal_Output, name='reverse', digital=True,
                  terminal_config='open_collector', kind='config')

    enable = Cpt(B_field_enable, name='enable', kind='normal')
    sign = Cpt(B_field_sign, name='sign', kind='normal')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, power_read_line='',
                 polarity_read_line='', power_on_line='', power_off_line='',
                 reverse_line='', reverse_time=25, wait_time=5, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        if reverse_line:
            self.reverse.setup_line(reverse_line)
        if power_read_line:
            self.power_read.setup_line(power_read_line)
        if power_on_line:
            self.power_on.setup_line(power_on_line)
        if power_off_line:
            self.power_off.setup_line(power_off_line)
        if polarity_read_line:
            self.polarity.setup_line(polarity_read_line)
        self.enable.change_setup(wait_time=wait_time,
                                 power_read=self.power_read,
                                 power_on=self.power_on,
                                 power_off=self.power_off,
                                 reverse=self.reverse)
        self.sign.change_setup(reverse_time=reverse_time,
                               polarity=self.polarity,
                               power_on=self.power_on,
                               power_off=self.power_off,
                               reverse=self.reverse)

    def finalize_steps(self):
        for c in [self.polarity, self.power_on, self.power_off, self.power_read,
                  self.reverse]:
            c.close_task()



if __name__ == '__main__':
    import bluesky.plan_stubs as bps
    from bluesky import RunEngine
    from bluesky.callbacks.best_effort import BestEffortCallback
    from databroker.databroker import Broker

    db = Broker.named('temp')
    RE = RunEngine()
    RE.subscribe(db.insert)
    bec = BestEffortCallback()
    RE.subscribe(bec)

    try:
        magnet = Bruker_Magnet_NI_DAQ(name='magnet', power_read_line='Bruker/port0/line0', polarity_read_line='Bruker/port0/line1', power_on_line='Bruker/port1/line0', power_off_line='Bruker/port1/line1', reverse_line='Bruker/port1/line2')


        def testplan(dev):
            yield from bps.open_run()
            yield from bps.trigger_and_read([dev.enable, dev.sign])
            yield from bps.abs_set(dev.enable, 1)
            yield from bps.trigger_and_read([dev.enable, dev.sign])
            yield from bps.abs_set(dev.sign, -1)
            yield from bps.trigger_and_read([dev.enable, dev.sign])
            yield from bps.abs_set(dev.sign, 1)
            yield from bps.trigger_and_read([dev.enable, dev.sign])
            yield from bps.abs_set(dev.enable, 0)
            yield from bps.trigger_and_read([dev.enable, dev.sign])
            yield from bps.close_run()

        RE(testplan(magnet))
    finally:
        close_tasks()
    header = db[-1]
    tab = header.table()
    print(header.start)
    print(header.table())
    print(header.config_data('magnet'))
