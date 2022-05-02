from agilent_34401.agilent_34401_ophyd import Agilent_34401

from main_classes import device_class

from PyQt5.QtWidgets import QWidget


class subclass(device_class.Device):
    def __init__(self):
        files = ['agilent_34401.db', 'agilent_34401.proto']
        req = ['prologixSup']
        super().__init__(name='agilent_34401', virtual=False, tags=['DMM', 'voltage', 'current'], directory='agilent_34401', ophyd_device=Agilent_34401, requirements=req, files=files, ophyd_class_name='Agilent_34401')

class subclass_config(device_class.Device_Config):
    def __init__(self):