import copy

import pandas as pd
from ophyd import Device
from ophyd import Component as Cpt
from ophyd import EpicsSignal

from bluesky_handling.EpicsFieldSignal import EpicsFieldSignal, EpicsFieldSignalRO

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

def pt1000(rMeas):
    return ptX(rMeas)

def pt1000_inv(T):
    return ptX_inv(T)


class PID_Controller(Device):
    pid_val = Cpt(EpicsFieldSignal, read_pv_name='pid_controller.VAL', name='pid_val')
    pid_cval = Cpt(EpicsFieldSignalRO, read_pv_name='pid_controller.CVAL', name='pid_cval')
    pid_kp = Cpt(EpicsFieldSignal, read_pv_name='pid_controller.KP', name='pid_kp', kind='config')
    pid_ki = Cpt(EpicsFieldSignal, read_pv_name='pid_controller.KI', name='pid_ki', kind='config')
    pid_kd = Cpt(EpicsFieldSignal, read_pv_name='pid_controller.KD', name='pid_kd', kind='config')
    pid_minval = Cpt(EpicsFieldSignal, read_pv_name='pid_controller.DRVL', name='pid_minval', kind='config')
    pid_maxval = Cpt(EpicsFieldSignal, read_pv_name='pid_controller.DRVH', name='pid_maxval', kind='config')
    pid_fbon = Cpt(EpicsFieldSignal, read_pv_name='pid_controller.FBON', name='pid_fbon')
    pid_mdt = Cpt(EpicsFieldSignal, read_pv_name='pid_controller.MDT', name='pid_mdt', kind='config')
    pid_scan = Cpt(EpicsFieldSignal, read_pv_name='pid_controller.SCAN', name='pid_scan', kind='config')
    pid_inp = Cpt(EpicsFieldSignal, read_pv_name='pid_controller.INP', name='pid_inp', kind='config')
    pid_outl = Cpt(EpicsFieldSignal, read_pv_name='pid_controller.OUTL', name='pid_outl', kind='config')
    pid_pval = Cpt(EpicsFieldSignalRO, read_pv_name='pid_controller.P', name='pid_pval')
    pid_ival = Cpt(EpicsFieldSignalRO, read_pv_name='pid_controller.I', name='pid_ival')
    pid_dval = Cpt(EpicsFieldSignalRO, read_pv_name='pid_controller.D', name='pid_dval')
    pid_oval = Cpt(EpicsFieldSignalRO, read_pv_name='pid_controller.OVAL', name='pid_oval')

    #pid_bias = Cpt(Simple_Signal, read_pv_name=None, name='pid_bias')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None, configuration_attrs=None, parent=None, pid_val_table=None, read_conv_func=None, auto_pid=True, interpolate_auto=True, set_conv_func=None, bias_signal=None, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent)
        self.pid_val.read_pv_name = f'{prefix}pid_controller.VAL'
        self.pid_cval.read_pv_name = f'{prefix}pid_controller.CVAL'
        self.pid_kp.read_pv_name = f'{prefix}pid_controller.KP'
        self.pid_ki.read_pv_name = f'{prefix}pid_controller.KI'
        self.pid_kd.read_pv_name = f'{prefix}pid_controller.KD'
        self.pid_minval.read_pv_name = f'{prefix}pid_controller.DRVL'
        self.pid_maxval.read_pv_name = f'{prefix}pid_controller.DRVH'
        self.pid_fbon.read_pv_name = f'{prefix}pid_controller.FBON'
        self.pid_mdt.read_pv_name = f'{prefix}pid_controller.MDT'
        self.pid_scan.read_pv_name = f'{prefix}pid_controller.SCAN'
        self.pid_inp.read_pv_name = f'{prefix}pid_controller.INP'
        self.pid_outl.read_pv_name = f'{prefix}pid_controller.OUTL'
        self.pid_pval.read_pv_name = f'{prefix}pid_controller.P'
        self.pid_dval.read_pv_name = f'{prefix}pid_controller.D'
        self.pid_ival.read_pv_name = f'{prefix}pid_controller.I'
        self.pid_oval.read_pv_name = f'{prefix}pid_controller.OVAL'
        self.pid_bias = bias_signal
        if not read_conv_func:
            read_conv_func = lambda x: x
        elif isinstance(read_conv_func, str):
            read_conv_func = globals()[read_conv_func]
        if read_conv_func is not None:
            self.pid_val.conversion_function = read_conv_func
            self.pid_cval.conversion_function = read_conv_func
        if not set_conv_func:
            set_conv_func = lambda x: x
        elif isinstance(set_conv_func, str):
            set_conv_func = globals()[set_conv_func]
        if set_conv_func is not None:
            self.pid_val.set_conversion_function = set_conv_func
            self.pid_cval.set_conversion_function = set_conv_func
        self.pid_val.putFunc = self.update_PID_vals
        # if pid_val_table is None:
        #     pid_val_table = PID_val_table()
        # elif type(pid_val_table) is str:
        #     pid_val_table = PID_val_table(table=pid_val_table)
        if pid_val_table is None:
            pid_val_table = pd.DataFrame({'setpoint': [0], 'kp': [0], 'ki': [0], 'kd': [0], 'maxval': [np.inf], 'minval': [-np.inf], 'bias': [0], 'stability-delta': [0], 'stability-time': [0]})
        elif type(pid_val_table) is str:
            pid_val_table = pd.read_csv(pid_val_table, delimiter='\t')
        self.pid_val_table = pid_val_table
        if read_conv_func is None:
            read_conv_func = lambda x: x
        self.read_conv_func = read_conv_func
        if set_conv_func is None:
            set_conv_func = lambda x: x
        self.set_conv_func = set_conv_func
        # self.pid_cval.conversion_function = self.read_conv_func
        # self.pid_val.set_conversion_function = self.set_conv_func
        # self.pid_val.conversion_function = self.read_conv_func
        self.auto_pid = auto_pid
        self.interpolate_auto = interpolate_auto
        # setpoint = self.pid_val.get()
        self.pid_vals = None
        self.stability_time = 0
        self.stability_delta = 0
        self.setpoint = 0
        # self.update_PID_vals(setpoint)

    def update_settings(self, **settings):
        if 'read_conv_func' in settings:
            read_conv_func = settings['read_conv_func']
            if not read_conv_func:
                read_conv_func = lambda x: x
            elif isinstance(read_conv_func, str):
                read_conv_func = globals()[read_conv_func]
            if read_conv_func is not None:
                self.pid_val.conversion_function = read_conv_func
                self.pid_cval.conversion_function = read_conv_func
        if 'set_conv_func' in settings:
            set_conv_func = settings['set_conv_func']
            if not set_conv_func:
                set_conv_func = lambda x: x
            elif isinstance(set_conv_func, str):
                set_conv_func = globals()[set_conv_func]
            if set_conv_func is not None:
                self.pid_val.set_conversion_function = set_conv_func
                self.pid_cval.set_conversion_function = set_conv_func
        if 'pid_val_table' in settings:
            pid_val_table = settings['pid_val_table']
            if pid_val_table is None:
                pid_val_table = pd.DataFrame({'setpoint': [0], 'kp': [0], 'ki': [0], 'kd': [0], 'maxval': [np.inf], 'minval': [-np.inf], 'bias': [0], 'stability-delta': [0], 'stability-time': [0]})
            elif type(pid_val_table) is str:
                pid_val_table = pd.read_csv(pid_val_table, delimiter='\t')
            self.pid_val_table = pid_val_table
        if 'auto_pid' in settings:
            self.auto_pid = settings['auto_pid']
        if 'interpolate_auto' in settings:
            self.interpolate_auto = settings['interpolate_auto']
        self.update_PID_vals(self.setpoint)


    def update_PID_vals(self, setpoint):
        # self.pid_vals = self.pid_val_table.get_vals(setpoint, self.auto_pid)
        if not self.auto_pid:
            return
        old_vals = copy.deepcopy(self.pid_vals)
        pid_val_table = pd.DataFrame(self.pid_val_table)
        setpoints = pid_val_table['setpoint']
        if setpoint >= max(setpoints):
            self.pid_vals = pid_val_table[setpoints == max(setpoints)].to_dict(orient='list')
        elif setpoint <= min(setpoints):
            self.pid_vals = pid_val_table[setpoints == min(setpoints)].to_dict(orient='list')
        elif self.interpolate_auto:
            next_lo = max(setpoints[setpoints <= setpoint])
            next_hi = min(setpoints[setpoints >= setpoint])
            lo_vals = pid_val_table[setpoints == next_lo].to_dict(orient='list')
            hi_vals = pid_val_table[setpoints == next_hi].to_dict(orient='list')
            self.pid_vals = {}
            for key, lo_val in lo_vals.items():
                self.pid_vals[key] = [lo_val[0] + (hi_vals[key][0] - lo_val[0]) * (setpoint - next_lo)/(next_hi - next_lo)]
        else:
            next_lo = max(setpoints[setpoints <= setpoint])
            self.pid_vals = pid_val_table[setpoints == next_lo].to_dict(orient='list')
        if old_vals != self.pid_vals:
            for key in self.pid_vals:
                if key in ['setpoint', 'stability-time', 'stability-delta'] or (key == 'bias' and self.pid_bias is None):
                    continue
                att = getattr(self, f'pid_{key}')
                att.put(self.pid_vals[key][0])
        self.stability_time = self.pid_vals['stability-time'][0]
        self.stability_delta = self.pid_vals['stability-delta'][0]
        self.setpoint = setpoint

    def wait_for_connection(self, all_signals=False, timeout=2.0):
        if timeout is None:
            timeout = self.connection_timeout
        sig = EpicsSignal(f'{self.prefix}pid_controller')
        sig.wait_for_connection(timeout=timeout)
    # def read(self):
    #     pass
    #
    # def get(self):
    #     val = self.pid_cval.get()
    #     return self.read_conv_func(val)
    #
    #
    # def put(self, value, **kwargs):
    #     self.update_PID_vals(value)
    #     value = self.set_conv_func(value)
    #     self.pid_val.put(value, **kwargs)
    #     st = Status(self, timeout=5, settle_time=0)
    #     st.set_finished()
    #     return st

if __name__ == '__main__':
    pid = PID_Controller('Hall:', name='pid',
                         pid_val_table=r"C:\Users\od93yces\FAIRmat\CAMELS\devices\devices_drivers\PID_controller\test_pid_values.txt",
                         auto_pid=True, interpolate_auto=True,
                         set_conv_func=ptX_inv, read_conv_func='ptX')
    pid.wait_for_connection()
    pid.put(60)
    print(pid.pid_vals)