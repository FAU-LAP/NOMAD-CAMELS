from Gap_Burner_Arduino.Gap_Burner_Arduino_ophyd import Gap_Burner_Arduino
from main_classes import device_class

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        files = []
        req = []
        super().__init__(name='Gap_Burner_Arduino', virtual=False, tags=['Arduino', 'voltage', 'current', 'burn'], directory='Gap_Burner_Arduino', ophyd_device=Gap_Burner_Arduino, requirements=req, files=files, ophyd_class_name='Gap_Burner_Arduino', **kwargs)
        self.config["ramp_time"] = 400
        self.config["offset"] = 1200
        self.config["min_current"] = 0
        self.config["min_voltage"] = 600
        self.config["dac_ref_zero"] = 0
        self.config["dac_zero"] = 400



class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None):
        super().__init__(parent, 'Gap Burner - Arduino', data, settings_dict,
                         config_dict, ioc_dict, additional_info)
        # self.comboBox_connection_type.addItem('EPICS: USB-serial')
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
