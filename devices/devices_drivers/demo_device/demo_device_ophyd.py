import numpy as np

from ophyd import Device
from ophyd import Component as Cpt
from bluesky_handling.custom_function_signal import Custom_Function_Signal, Custom_Function_SignalRO

def gauss(x, sig, a, mu):
    return a / sig / np.sqrt(2 * np.pi) * np.exp(-(x - mu)**2 / 2 / sig**2)


class Demo_Device(Device):
    motorX = Cpt(Custom_Function_Signal, name='motorX', metadata={'units': 'm'})
    motorY = Cpt(Custom_Function_Signal, name='motorY', metadata={'units': 'm'})
    motorZ = Cpt(Custom_Function_Signal, name='motorZ', metadata={'units': 'm'})
    detectorX = Cpt(Custom_Function_SignalRO, name='detectorX', metadata={'units': 'counts/s'})
    detectorY = Cpt(Custom_Function_SignalRO, name='detectorY', metadata={'units': 'kg'})
    detectorZ = Cpt(Custom_Function_SignalRO, name='detectorZ', metadata={'units': 'eV'})
    detectorComm = Cpt(Custom_Function_SignalRO, name='detectorComm', metadata={'units': '$'})

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, motor_noises=None,
                 detector_noises=None, sigmas=None, mus=None, amps=None,
                 **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        self.motor_vals = [0, 0, 0]
        self.motor_noises = motor_noises or [0, 0, 0]
        self.detector_noises = detector_noises or [0, 0, 0]
        self.sigmas = sigmas or [5, 7, 0.1]
        self.mus = mus or [0, 3, -4]
        self.amps = amps or [1, 2, 27]
        self.motorX.put_function = lambda x: self.motor_func(x, 0)
        self.motorY.put_function = lambda x: self.motor_func(x, 1)
        self.motorZ.put_function = lambda x: self.motor_func(x, 2)
        self.motorX.read_function = lambda: self.motor_read_func(0)
        self.motorY.read_function = lambda: self.motor_read_func(1)
        self.motorZ.read_function = lambda: self.motor_read_func(2)
        self.detectorX.read_function = lambda: self.det_func(0)
        self.detectorY.read_function = lambda: self.det_func(1)
        self.detectorZ.read_function = lambda: self.det_func(2)
        self.detectorComm.read_function = lambda: self.det_func(3)
        self.motorX._tolerance = self.motor_noises[0]
        self.motorY._tolerance = self.motor_noises[1]
        self.motorZ._tolerance = self.motor_noises[2]

    def motor_func(self, val, motor):
        self.motor_vals[motor] = val

    def motor_read_func(self, n):
        return self.motor_vals[n] + self.motor_noises[n] * (np.random.rand() - 0.5)

    def det_func(self, n):
        if n == 3:
            return self.det_func(0) + self.det_func(1) + self.det_func(2)
        mot_val = self.motor_read_func(n)
        g = gauss(mot_val, self.sigmas[n], self.amps[n], self.mus[n])
        return g + self.detector_noises[n] * (1 - np.random.rand())


if __name__ == '__main__':
    dem = Demo_Device(name='dem')
    print(dem.motorX.get())
