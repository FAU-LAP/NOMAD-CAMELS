from ophyd import Component as Cpt
import numpy as np
import re
from pyAndorSDK2 import atmcd, atmcd_codes, atmcd_errors

from bluesky_handling.custom_device import custom_Device  # ?
from bluesky_handling.custom_function_signal import Custom_Function_Signal

sdk = atmcd() # Load the atmcd library
codes =  atmcd_codes


class Andor_Newton(custom_Device):  # ?
    """
    Driver for the Andor Newton CCD camera
    """
    read_camera = Cpt(Custom_Function_Signal, name='read_DC', metadata={'units': 'intensity'})
    # Configuration settings
    serial_number = Cpt(Custom_Function_Signal, name='serial_number', kind='config',)
    set_temperature = Cpt(Custom_Function_Signal, name='set_temperature', kind='config',)
    shutter_mode = Cpt(Custom_Function_Signal, name='shutter_mode', kind='config')
    exposure_time = Cpt(Custom_Function_Signal, name='exposure_time', kind='config')
    readout_mode = Cpt(Custom_Function_Signal, name='readout_mode', kind='config', )
    preamp_gain = Cpt(Custom_Function_Signal, name='preamp_gain', kind='config', )
    horizontal_binning = Cpt(Custom_Function_Signal, name='horizontal_binning', kind='config', )
    hs_speed = Cpt(Custom_Function_Signal, name='hs_speed', kind='config', )
    vs_speed = Cpt(Custom_Function_Signal, name='vs_speed', kind='config', )
    number_of_tracks = Cpt(Custom_Function_Signal, name='number_of_tracks', kind='config', )
    track_height = Cpt(Custom_Function_Signal, name='track_height', kind='config', )
    start_row = Cpt(Custom_Function_Signal, name='start_row', kind='config', )
    end_row = Cpt(Custom_Function_Signal, name='end_row', kind='config', )

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 baud_rate=9600, write_termination='\r\n',
                 read_termination='\r\n', **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, baud_rate=baud_rate,
                         write_termination=write_termination,
                         read_termination=read_termination, **kwargs)
        self.read_camera.put_function = lambda : self.read_camera_function()
        self.serial_number.put_function = lambda x: self.serial_number_function(x)

    def read_camera_function(self,):





if __name__ == '__main__':
    testk = Andor_Newton(name='testk')
