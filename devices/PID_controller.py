from ophyd import EpicsSignal, EpicsSignalRO, Device, Signal
from ophyd import Component as Cpt
from ophyd.status import Status

from epics import caput, caget

import numpy as np
from scipy.optimize import root


def helper(x, r, a, b, c):
    return 1 - r + a*x + b*x**2 + c*(x - 100) * x**3

def ptX(rMeas, rX=1000):
    r = rMeas/rX
    a = 3.9083E-3
    b = -5.775E-7
    c = -4.183E-12
    t = 273.15 + (-a + np.sqrt(a**2-4*(1-r)*b))/2/b
    if t < 273.15:
        zero = root(lambda x: helper(x, r, a, b, c), -150).x
        return zero[0] + 273.15
    return t

def ptX_inv(T, rX=1000):
    return root(lambda r: ptX(r, rX) - T, 300).x[0]


class Simple_Signal(Signal):
    def __init__(self,  read_pv_name, name, value=0., timestamp=None, parent=None, labels=None, kind='hinted', tolerance=None, rtolerance=None, metadata=None, cl=None, attr_name='', conversion_function=None, set_conversion_function=None):
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent, labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance, metadata=metadata, cl=cl, attr_name=attr_name)
        self.read_pv_name = read_pv_name
        if conversion_function is None:
            conversion_function = lambda x: x
        self.conversion_function = conversion_function
        if set_conversion_function is None:
            set_conversion_function = lambda x: x
        self.set_conversion_function = set_conversion_function

    def get(self):
        if self.read_pv_name is not None:
            self._readback = self.conversion_function(caget(self.read_pv_name))
        return super().get()

    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        val = self.set_conversion_function(value)
        if self.read_pv_name is not None:
            caput(self.read_pv_name, val, wait=True)
        super().put(val, timestamp=timestamp, force=force, metadata=metadata, **kwargs)

class PID_vals(dict):
    key_list = ['kp', 'ki', 'kd', 'min', 'max', 'bias']
    default_vals = [0, 0, 0, -np.inf, np.inf, 0]

    def __init__(self, **kwargs):
        super().__init__()
        for n, k in enumerate(self.key_list):
            val = kwargs[k] if k in kwargs else self.default_vals[n]
            self.update({k: val})

    def __setitem__(self, key, value):
        if key not in self.key_list:
            raise KeyError
        super().__setitem__(key, value)


class PID_val_table:
    def __init__(self, setpoints=None, table=None):
        if setpoints is None:
            setpoints = [0.0]
        if table is None:
            table = {str(0.0): PID_vals()}
            self.table = table
        elif type(table) is str:
            self.load_from_file(table)
        else:
            self.table = table
            self.setpoints = setpoints

    def load_from_file(self, file):
        data = np.loadtxt(file)
        self.table = {}
        self.setpoints = []
        for d in data:
            vals = PID_vals()
            vals['kp'] = d[1]
            vals['ki'] = d[2]
            vals['kd'] = d[3]
            vals['min'] = d[4]
            vals['max'] = d[5]
            vals['bias'] = d[6]
            self.table.update({str(d[0]): vals})
            self.setpoints.append(d[0])
        

    def add_setpoint(self, setpoint_vals, setpoint):
        self.setpoints.append(setpoint)
        self.table.update({str(setpoint): setpoint_vals})

    def remove_setpoint(self, setpoint):
        self.setpoints.remove(setpoint)
        self.table.pop(str(setpoint))

    def get_vals(self, setpoint, interpolate=False):
        setpoints = np.array(self.setpoints)
        if setpoint >= max(setpoints):
            return self.table[str(max(setpoints))]
        if setpoint <= min(setpoints):
            return self.table[str(min(setpoints))]
        dists = setpoint - setpoints
        dists_pos = dists[np.where(dists >= 0)]
        idx_p = np.where(dists == dists_pos.min())
        if interpolate:
            dists_neg = dists[np.where(dists < 0)]
            idx_n = np.where(dists == dists_neg.max())
            low = setpoints[idx_p][0]
            hi = setpoints[idx_n][0]
            low_vals = self.table[str(low)]
            hi_vals = self.table[str(hi)]
            intp_vals = PID_vals()
            for k in intp_vals:
                intp_vals[k] = np.interp(setpoint, [low, hi], [low_vals[k], hi_vals[k]])
            return intp_vals
        setp = setpoints[idx_p]
        return self.table[str(setp)]



class PID_controller(Device):
    pid_set = Cpt(Simple_Signal, read_pv_name='pid_controller.VAL', name='pid_set')
    pid_cval = Cpt(Simple_Signal, read_pv_name='pid_controller.CVAL', name='pid_cval')
    pid_kp = Cpt(Simple_Signal, read_pv_name='pid_controller.KP', name='pid_kp', kind='config')
    pid_ki = Cpt(Simple_Signal, read_pv_name='pid_controller.KI', name='pid_ki', kind='config')
    pid_kd = Cpt(Simple_Signal, read_pv_name='pid_controller.KD', name='pid_kd', kind='config')
    pid_min = Cpt(Simple_Signal, read_pv_name='pid_controller.DRVL', name='pid_min', kind='config')
    pid_max = Cpt(Simple_Signal, read_pv_name='pid_controller.DRVH', name='pid_max', kind='config')
    pid_fbon = Cpt(Simple_Signal, read_pv_name='pid_controller.FBON', name='pid_fbon')
    #pid_bias = Cpt(Simple_Signal, read_pv_name=None, name='pid_bias')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None, configuration_attrs=None, parent=None, pid_val_table=None, read_conv_func=None, auto_pid=True, interpolate_auto=True, set_conv_func=None, bias_signal=None, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        self.pid_set.read_pv_name = f'{prefix}pid_controller.VAL'
        self.pid_cval.read_pv_name = f'{prefix}pid_controller.CVAL'
        self.pid_kp.read_pv_name = f'{prefix}pid_controller.KP'
        self.pid_ki.read_pv_name = f'{prefix}pid_controller.KI'
        self.pid_kd.read_pv_name = f'{prefix}pid_controller.KD'
        self.pid_min.read_pv_name = f'{prefix}pid_controller.DRVL'
        self.pid_max.read_pv_name = f'{prefix}pid_controller.DRVH'
        self.pid_fbon.read_pv_name = f'{prefix}pid_controller.FBON'
        self.pid_bias = bias_signal
        if pid_val_table is None:
            pid_val_table = PID_val_table()
        elif type(pid_val_table) is str:
            pid_val_table = PID_val_table(table=pid_val_table)
        self.pid_val_table = pid_val_table
        if read_conv_func is None:
            read_conv_func = lambda x: x
        self.read_conv_func = read_conv_func
        if set_conv_func is None:
            set_conv_func = lambda x: x
        self.set_conv_func = set_conv_func
        self.pid_cval.conversion_function = self.read_conv_func
        self.pid_set.set_conversion_function = self.set_conv_func
        self.pid_set.conversion_function = self.read_conv_func
        self.auto_pid = auto_pid
        self.interpolate_auto = interpolate_auto
        setpoint = self.pid_set.get()
        self.pid_vals = None
        self.update_PID_vals(setpoint)

    def update_PID_vals(self, setpoint):
        self.pid_vals = self.pid_val_table.get_vals(setpoint, self.auto_pid)
        for key in self.pid_vals:
            if key == 'bias' and self.pid_bias is None:
                continue
            att = getattr(self, f'pid_{key}')
            att.put(self.pid_vals[key])

    def set(self, value, **kwargs):
        self.update_PID_vals(value)
        self.pid_set.put(value, **kwargs)
        st = Status(self, timeout=5, settle_time=0)
        st.set_finished()
        return st

    def stage(self):
        self.pid_fbon.put(1)
        return super().stage()

    def unstage(self):
        self.pid_fbon.put(0)
        return super().unstage()




if __name__ == '__main__':
    from bluesky.run_engine import RunEngine
    from databroker.databroker import Broker
    import bluesky.plan_stubs as bps
    from bluesky.plans import count, scan

    from Keysight_34401 import Keysight_34401
    
    import daq_signal


    # def testplan(dets, mot, start, stop, n, delay=0, md=None):
    #     yield from bps.open_run()
    #     yield from bps.trigger_and_read(dets, name='sec')
    #     for i in np.linspace(start, stop, n):
    #         yield from bps.abs_set(mot, i, wait=True)
    #         yield from bps.sleep(delay)
    #         yield from trigger_and_read_devices(dets)
    #     yield from bps.close_run()
    RE = RunEngine()
    db = Broker.named('temp')
    RE.subscribe(db.insert)
    # # mesI = TriggerEpicsSignalRO('Hall:e5270:mesI1')
    # mesV = TriggerEpicsSignalRO('Hall:e5270:mesV1')
    # setV = EpicsSignal('Hall:e5270:setV1')
    # setV.wait_for_connection()
    # # mesI.wait_for_connection()
    # mesV.wait_for_connection()
    # # RE(scan([mesV], setV, 0, 1, 3))
    # RE(testplan([mesV], setV, 0, 1, 3))
    valve = daq_signal.DAQ_Signal_Output(name='valve', line_name='Bruker/ao1', minV=0, maxV=10)
    valve.put(0)
    dmm = Keysight_34401('Hall:34401:', name='dmm')
    pid = PID_controller('Hall:', name='pid', read_conv_func=ptX, set_conv_func=ptX_inv, bias_signal=valve, pid_val_table=r"C:\Users\fulapuser\Desktop\ioc_pid_vals.txt")
    pid.wait_for_connection()
    # RE(count([pid], num=3))
    #RE(scan([pid, valve], pid, 50, 300, 3))
    header = db[-1]
    tab = header.table()
    print(header.start)
    print(header.table())
    print(header.config_data('pid'))
    # camonitor('Hall:e5270:mesV1', callback=mesV.callback_method)
    # while True:
    #     time.sleep(0.1)

