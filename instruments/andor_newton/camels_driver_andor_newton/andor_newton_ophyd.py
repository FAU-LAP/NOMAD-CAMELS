from ophyd import Component as Cpt
import numpy as np
import re
import time
from pyAndorSDK2 import atmcd, atmcd_codes, atmcd_errors

from CAMELS.bluesky_handling.custom_function_signal import Custom_Function_Signal
from CAMELS.main_classes.device_class import Device, Device_Config
from camels_support_visa_signal import VISA_Signal_Read, VISA_Signal_Write, VISA_Device

sdk = atmcd() # Load the atmcd library
codes = atmcd_codes
imageSize = 1024 # number of pixels in x direction


class Andor_Newton(VISA_Device):
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
                 configuration_attrs=None, parent=None, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        self.read_camera.put_function = lambda : self.read_camera_function()
        self.set_temperature.put_function = lambda x: self.set_temperature_function(x)

    def set_temperature_function(self,):
        ret = sdk.SetTemperature(-60)
        print("Function SetTemperature returned {} target temperature -60".format(ret))
        ret = sdk.CoolerON()
        print("Function CoolerON returned {}".format(ret))
        while ret != atmcd_errors.Error_Codes.DRV_TEMP_STABILIZED:
            time.sleep(5)
            (ret, temperature) = sdk.GetTemperature()
            print("Function GetTemperature returned {} current temperature = {} ".format(
                ret, temperature), end='\r')
        print("")
        print("Temperature stabilized")


    def read_camera_function(self,):
        ret = sdk.StartAcquisition()
        print("Function StartAcquisition returned {}".format(ret))

        ret = sdk.WaitForAcquisition()
        print("Function WaitForAcquisition returned {}".format(ret))

        (ret, arr, validfirst, validlast) = sdk.GetImages16(1, 1, imageSize)
        print("Function GetImages16 returned {} first pixel = {} size = {}".format(
            ret, arr[0], imageSize))
        return arr








if __name__ == '__main__':
    testk = Andor_Newton(name='testk')
