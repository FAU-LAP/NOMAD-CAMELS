import time

import numpy as np
from scipy.optimize import root
import pandas as pd
import copy

import simple_pid

from ophyd import Device
from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal, Custom_Function_SignalRO
from nomad_camels.utility import device_handling

from PySide6.QtCore import QThread, Signal


def helper_ptX(x, r, a, b, c):
    return 1 - r + a*x + b*x**2 + c*(x - 100) * x**3

def ptX(rMeas, rX=1000):
    r = rMeas/rX
    a = 3.9083E-3
    b = -5.775E-7
    c = -4.183E-12
    t = 273.15 + (-a + np.sqrt(a**2-4*(1-r)*b))/2/b
    if t < 273.15:
        zero = root(lambda x: helper_ptX(x, r, a, b, c), -150).x
        return zero[0] + 273.15
    return t

def ptX_inv(T, rX=1000):
    return root(lambda r: ptX(r, rX) - T, 300).x[0]

def pt1000(rMeas):
    return ptX(rMeas)

def pt1000_inv(T):
    return ptX_inv(T)


class PID_Controller(Device):
    output_value = Cpt(Custom_Function_SignalRO, name='output_value')
    current_value = Cpt(Custom_Function_SignalRO, name='current_value')
    setpoint = Cpt(Custom_Function_Signal, name='setpoint')
    pid_stable = Cpt(Custom_Function_SignalRO, name='pid_stable')
    pid_on = Cpt(Custom_Function_Signal, name='pid_on')
    p_value = Cpt(Custom_Function_SignalRO, name='p_value')
    i_value = Cpt(Custom_Function_SignalRO, name='i_value')
    d_value = Cpt(Custom_Function_SignalRO, name='d_value')

    kp = Cpt(Custom_Function_Signal, name='kp', kind='config')
    ki = Cpt(Custom_Function_Signal, name='ki', kind='config')
    kd = Cpt(Custom_Function_Signal, name='kd', kind='config')
    dt = Cpt(Custom_Function_Signal, name='dt', kind='config')
    min_value = Cpt(Custom_Function_Signal, name='min_value', kind='config')
    max_value = Cpt(Custom_Function_Signal, name='max_value', kind='config')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, pid_val_table=None,
                 read_conv_func=None, auto_pid=True, interpolate_auto=True,
                 set_conv_func=None, bias_signal=None, set_signal=None, read_signal=None, show_plot=False, **kwargs):
        pops = ['val_choice', 'val_file', 'read_signal_name', 'set_signal_name',
                'bias_signal_name']
        for p in pops:
            if p in kwargs:
                kwargs.pop(p)
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        if isinstance(read_signal, str):
            read_signal = device_handling.get_channel_from_string(read_signal)
        if isinstance(set_signal, str):
            set_signal = device_handling.get_channel_from_string(set_signal)
        if isinstance(bias_signal, str):
            bias_signal = device_handling.get_channel_from_string(bias_signal)

        if not read_conv_func:
            read_conv_func = lambda x: x
        elif isinstance(read_conv_func, str):
            read_conv_func = globals()[read_conv_func]
        if not set_conv_func:
            set_conv_func = lambda x: x
        elif isinstance(set_conv_func, str):
            set_conv_func = globals()[set_conv_func]

        def read_function():
            x = read_signal.get()
            return read_conv_func(x)
        self.read_function = read_function

        def set_function(x):
            x = set_conv_func(x)
            set_signal.put(x)
            self.current_output = x
        self.set_function = set_function
        self.current_output = 0

        if bias_signal:
            self.bias_func = bias_signal.put
        else:
            self.bias_func = None

        self.current_value.read_function = self.current_value_read
        self.output_value.read_function = self.get_output
        self.pid_stable.read_function = self.stable_check
        self.kp.put_function = self.set_Kp
        self.ki.put_function = self.set_Ki
        self.kd.put_function = self.set_Kd
        self.dt.put_function = self.set_dt
        self.min_value.put_function = self.set_minval
        self.max_value.put_function = self.set_maxval
        self.pid_on.put_function = self.set_pid_on
        self.setpoint.put_function = self.update_PID_vals

        if pid_val_table is None:
            pid_val_table = pd.DataFrame({'setpoint': [0], 'kp': [0], 'ki': [0], 'kd': [0], 'max_value': [np.inf], 'min_value': [-np.inf], 'bias': [0], 'stability-delta': [0], 'stability-time': [0]})
        elif type(pid_val_table) is str:
            pid_val_table = pd.read_csv(pid_val_table, delimiter='\t')
        self.pid_val_table = pid_val_table
        self.auto_pid = auto_pid
        self.interpolate_auto = interpolate_auto
        self.pid_vals = None
        self.stability_time = np.inf
        self.stability_delta = 0
        if name != 'test':
            self.pid_thread = PID_Thread(self)
            # if show_plot:
            from nomad_camels.main_classes.plot_widget import PlotWidget_NoBluesky
            y_axes = {'output': 2,
                      'k': 2,
                      'i': 2,
                      'd': 2}
            self.plot = PlotWidget_NoBluesky('time', title='PID plot',
                                             ylabel='value', ylabel2='PID-values',
                                             y_axes=y_axes,
                                             first_hidden=list(y_axes.keys()),
                                             show_plot=show_plot)
            # for y in y_axes:
            #     self.plot.plot.current_lines[y].setLinestyle('None')
            self.pid_thread.new_data.connect(self.data_update)
            self.pid_thread.start()
            self.update_PID_vals(self.pid_thread.pid.setpoint)

    def change_show_plot(self, show):
        self.plot.plot.show_plot = show
        self.plot.setHidden(not show)

    def current_value_read(self):
        return self.pid_thread.current_value

    def data_update(self, timestamp, setpoint, current, output, kid):
        ys = {'current value': current,
              'setpoint': setpoint,
              'output': output,
              'k': kid[0],
              'i': kid[1],
              'd': kid[2]}
        self.plot.plot.add_data(timestamp, ys)

    def stable_check(self):
        return self.pid_thread.stable_time >= self.stability_time


    def get_output(self):
        return self.current_output

    def set_Kp(self, value):
        self.pid_thread.pid.Kp = value

    def set_Ki(self, value):
        self.pid_thread.pid.Ki = value

    def set_Kd(self, value):
        self.pid_thread.pid.Kd = value

    def set_dt(self, value):
        self.pid_thread.pid.sample_time = value
        self.pid_thread.sample_time = value

    def set_minval(self, value):
        maxval = self.max_value.get()
        self.pid_thread.pid.output_limits = (value, maxval)

    def set_maxval(self, value):
        minval = self.min_value.get()
        self.pid_thread.pid.output_limits = (minval, value)

    def read_p(self):
        return self.pid_thread.pid.components[0]

    def read_i(self):
        return self.pid_thread.pid.components[1]

    def read_d(self):
        return self.pid_thread.pid.components[2]

    def set_pid_on(self, value):
        self.pid_thread.pid.set_auto_mode(value)
        self.auto_pid = value
        self.update_PID_vals(self.pid_thread.pid.setpoint, force=True)

    def finalize_steps(self):
        self.pid_thread.still_running = False
        self.plot.close()


    def update_PID_vals(self, setpoint, force=False):
        if not self.auto_pid:
            if self.bias_func is not None:
                self.bias_func(0)
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
        if old_vals != self.pid_vals or force:
            for key in self.pid_vals:
                if key in ['setpoint', 'stability-time', 'stability-delta'] or (key == 'bias' and self.bias_func is None):
                    continue
                elif key == 'bias':
                    self.bias_func(self.pid_vals[key][0])
                else:
                    att = getattr(self, key)
                    att.put(self.pid_vals[key][0])
        self.stability_time = self.pid_vals['stability-time'][0]
        self.stability_delta = self.pid_vals['stability-delta'][0]
        self.pid_thread.stability_delta = self.pid_vals['stability-delta'][0]
        # self.setpoint = setpoint
        self.pid_thread.pid.setpoint = setpoint
        self.pid_thread.stable_time = 0

    def update_pid_settings(self, settings):
        self.pid_val_table = settings['pid_val_table']
        self.interpolate_auto = settings['interpolate_auto']
        self.update_PID_vals(self.pid_thread.pid.setpoint)



class PID_Thread(QThread):
    new_data = Signal(float, float, float, float, tuple)

    def __init__(self, pid_device, Kp=1.0, Ki=1.0, Kd=1.0, setpoint=0,
                 sample_time=1, output_limits=(None, None), auto_mode=False,
                 proportional_on_measurement=False, error_map=None, **kwargs):
        super().__init__()
        self.pid = simple_pid.PID(Kp=Kp, Ki=Ki, Kd=Kd, setpoint=setpoint,
                                  sample_time=sample_time,
                                  output_limits=output_limits,
                                  auto_mode=auto_mode,
                                  proportional_on_measurement=proportional_on_measurement,
                                  error_map=error_map)
        self.device = pid_device
        self.sample_time = sample_time
        self.stable_time = 0
        self.stability_delta = 0
        self.last = None
        self.starttime = 0
        self.current_value = 0
        self.still_running = True

    def update_pid(self, Kp=None, Ki=None, Kd=None, setpoint=None,
                   sample_time=None, output_limits=None, auto_mode=True,
                   proportional_on_measurement=False, error_map=None,):
        pass

    def run(self):
        self.starttime = time.monotonic()
        self.last = time.monotonic()
        while self.still_running:
            self.pid_step()

    def pid_step(self):
        now = time.monotonic()
        dis = now - self.last
        if dis < self.sample_time:
            time.sleep(self.sample_time - dis)
            dis = time.monotonic() - self.last
        self.current_value = self.device.read_function()
        if self.pid.auto_mode:
            new_output = self.pid(self.current_value)
        else:
            new_output = 0
        self.last = time.monotonic()
        if new_output is not None:
            self.device.set_function(new_output)
        if np.abs(self.pid.setpoint - self.current_value) <= self.stability_delta:
            self.stable_time += dis
        else:
            self.stable_time = 0
        self.new_data.emit(self.last - self.starttime, self.pid.setpoint, self.current_value,
                           new_output or 0, self.pid.components)

