# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import nidaqmx

from ophyd import Device, Signal
from ophyd.signal import SignalRO
from ophyd import Component as Cpt

from bluesky import RunEngine
from bluesky.plans import count, scan
import bluesky.plan_stubs as bps
from databroker.databroker import Broker

import time

#with nidaqmx.Task() as task:
#    task.di_channels.add_di_chan('Bruker/port0/line0')
#    print(task.read())
    
def get_dig_config(output_config='default'):
    if output_config.lower() == 'open_collector':
        return nidaqmx.constants.DigitalDriveType.OPEN_COLLECTOR
    return nidaqmx.constants.DigitalDriveType.ACTIVE_DRIVE

def get_an_config(output_config='default'):
    if output_config.lower() == 'bal_diff':
        return nidaqmx.constants.TerminalConfiguration.BAL_DIFF
    if output_config.lower() == 'nrse':
        return nidaqmx.constants.TerminalConfiguration.NRSE
    if output_config.lower() == 'pseudodifferential':
        return nidaqmx.constants.TerminalConfiguration.PSEUDODIFFERENTIAL
    if output_config.lower() == 'rse':
        return nidaqmx.constants.TerminalConfiguration.RSE
    return nidaqmx.constants.TerminalConfiguration.DEFAULT
    

class DAQ_Signal_Output(Signal):
    def __init__(self,  name, value=0., timestamp=None, parent=None, labels=None, kind='hinted', tolerance=None, rtolerance=None, metadata=None, cl=None, attr_name='', line_name='', digital=False, minV=-10, maxV=10, output_config='default', wait_time=0):
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent, labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance, metadata=metadata, cl=cl, attr_name=attr_name)
        self.task = nidaqmx.Task()
        self.digital = digital
        if digital:
            if output_config != 'default':
                self.task.do_channels.add_do_chan(line_name)
                #do_channel.
            else:
                self.task.do_channels.add_do_chan(line_name)
        else:
            self.task.ao_channels.add_ao_voltage_chan(line_name, min_val=minV, max_val=maxV)
        self.wait_time = wait_time
    
    #def get(self):
        #self._readback = self.task.read()
        #return super().get()
    
    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        if self.digital and (type(value) is not bool):
            if value > 0:
                value = True
            else:
                value = False
        self.task.write(value)
        #time.sleep(self.wait_time)
        super().put(value, timestamp=timestamp, force=force, metadata=metadata, **kwargs)
        
        
        
class DAQ_Signal_Input(SignalRO):
    def __init__(self,  name, value=0., timestamp=None, parent=None, labels=None, kind='hinted', tolerance=None, rtolerance=None, metadata=None, cl=None, attr_name='', line_name='', digital=False, minV=-10, maxV=10, terminal_config='default'):
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent, labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance, metadata=metadata, cl=cl, attr_name=attr_name)
        self.task = nidaqmx.Task()
        if digital:
            self.task.di_channels.add_di_chan(line_name)
        else:
            self.task.ai_channels.add_ai_voltage_chan(line_name, terminal_config=get_an_config(terminal_config), min_val=minV, max_val=maxV)

    def destroy(self):
        self.task.close()
        super().destroy()
                        
    def get(self):
        self._readback = self.task.read()
        return super().get()

    
    

class Bruker_Magnet(Device):
    power_read = Cpt(DAQ_Signal_Input, name='power_read', digital=True, line_name='Bruker/port0/line0')
    polung = Cpt(DAQ_Signal_Input, name='polung', digital=True, line_name='Bruker/port0/line1')
    over_curr = Cpt(DAQ_Signal_Input, name='over_curr', digital=True, line_name='Bruker/port0/line2')
    ext = Cpt(DAQ_Signal_Input, name='ext', digital=True, line_name='Bruker/port0/line3')
    over_temp = Cpt(DAQ_Signal_Input, name='over_temp', digital=True, line_name='Bruker/port0/line4')
    rst = Cpt(DAQ_Signal_Input, name='rst', digital=True, line_name='Bruker/port0/line5')
    over_power = Cpt(DAQ_Signal_Input, name='over_power', digital=True, line_name='Bruker/port0/line6')
    local = Cpt(DAQ_Signal_Input, name='local', digital=True, line_name='Bruker/port0/line7')
    power_on = Cpt(DAQ_Signal_Output, name='power_on', digital=True, output_config='open_collector', line_name='Bruker/port1/line0', wait_time=5)
    power_off = Cpt(DAQ_Signal_Output, name='power_off', digital=True, output_config='open_collector', line_name='Bruker/port1/line1', wait_time=5)
    reverse = Cpt(DAQ_Signal_Output, name='reverse', digital=True, output_config='open_collector', line_name='Bruker/port1/line2', wait_time=25)
    




def testplan(dets, on, off, rev):
    yield from bps.open_run()
    yield from bps.trigger_and_read(dets)
    yield from bps.abs_set(on, 0)
    yield from bps.sleep(0.3)
    yield from bps.abs_set(on, 1)
    yield from bps.sleep(5)
    yield from bps.trigger_and_read(dets)
    yield from bps.abs_set(rev, 0)
    yield from bps.sleep(0.3)
    yield from bps.abs_set(rev, 1)
    yield from bps.sleep(25)
    yield from bps.trigger_and_read(dets)
    yield from bps.abs_set(rev, 0)
    yield from bps.sleep(0.3)
    yield from bps.abs_set(rev, 1)
    yield from bps.sleep(25)
    yield from bps.trigger_and_read(dets)
    yield from bps.abs_set(off, 0)
    yield from bps.sleep(0.3)
    yield from bps.abs_set(off, 1)
    yield from bps.sleep(5)
    yield from bps.trigger_and_read(dets)
    
    

if __name__ == '__main__':
    RE = RunEngine()
    db = Broker.named('temp')
    RE.subscribe(db.insert)
    bruker = Bruker_Magnet(name='bruker')
    valve = DAQ_Signal_Output(name='valve', line_name='Bruker/ao1', minV=0, maxV=10)
    #RE(testplan([bruker], bruker.power_on, bruker.power_off, bruker.reverse))
    #valve.put(5)
    RE(scan([valve], valve, 5, 0, 3))
    header = db[-1]
    tab = header.table()
    print(header.start)
    print(header.table())
    print(header.config_data('bruker'))
