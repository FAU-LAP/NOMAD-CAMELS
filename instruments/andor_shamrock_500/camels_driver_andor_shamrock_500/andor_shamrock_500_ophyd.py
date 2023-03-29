from ophyd import Component as Cpt
import numpy as np
import re
from pyAndorSpectrograph import ATSpectrograph

from CAMELS.bluesky_handling.custom_function_signal import Custom_Function_Signal
from CAMELS.main_classes.device_class import Device, Device_Config
from camels_support_visa_signal import VISA_Signal_Read, VISA_Signal_Write, VISA_Device


# TODO
#  This should not be a VISA Device -> write new device class for instruments using dlls
class Andor_Shamrock_500(VISA_Device):
    """
    Driver for the Andor Shamrock 500 spectrometer (not the camera!).
    The camera is implemented separately.
    """
    setGrating = Cpt(VISA_Signal_Read, name='setGrating', )
    # Configuration settings
    serial_number = Cpt(Custom_Function_Signal, name='serial_number', kind='config', )

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent, **kwargs)

        # self.setGrating.put_function = lambda: self.read_camera_function()
        # self.serial_number.put_function = lambda x: self.set_temperature_function(x)






if __name__ == '__main__':
    testk = Andor_Shamrock_500(name='testk')
