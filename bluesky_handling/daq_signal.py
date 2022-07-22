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

tasks = []

def close_tasks():
    for task in tasks:
        task.close()
    tasks.clear()

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
        tasks.append(self.task)
        self.digital = digital
        self.output_config = output_config
        self.minV = minV
        self.maxV = maxV
        if line_name:
            self.setup_line(line_name)
        self.wait_time = wait_time

    def setup_line(self, line_name):
        if self.digital:
            if self.output_config != 'default':
                self.task.do_channels.add_do_chan(line_name)
            else:
                self.task.do_channels.add_do_chan(line_name)
        else:
            self.task.ao_channels.add_ao_voltage_chan(line_name,
                                                      min_val=self.minV,
                                                      max_val=self.maxV)
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
        tasks.append(self.task)
        self.digital = digital
        self.minV = minV
        self.maxV = maxV
        self.terminal_config = terminal_config
        if line_name:
            self.setup_line(line_name)

    def setup_line(self, line_name):
        if self.digital:
            self.task.di_channels.add_di_chan(line_name)
        else:
            self.task.ai_channels.add_ai_voltage_chan(line_name,
                                                      terminal_config=get_an_config(self.terminal_config),
                                                      min_val=self.minV,
                                                      max_val=self.maxV)


    def destroy(self):
        self.task.close()
        super().destroy()
                        
    def get(self):
        self._readback = self.task.read()
        return super().get()

    

    




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
