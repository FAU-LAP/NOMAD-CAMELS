from main_classes import device_class
from keysight_b2912.keysight_b2912_config import Ui_Form

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None, additional_info=None):
        super().__init__(parent, 'Keysight B2912', data, settings_dict, additional_info)
        self.comboBox_connection_type.addItem('prologix-GPIB')
        self.load_settings()