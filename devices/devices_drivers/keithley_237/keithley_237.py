from keithley_237.keithley_237_ophyd import Keithley_237

from main_classes import device_class

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        files = []
        req = []
        super().__init__(name='keithley_237', virtual=False, tags=['DMM', 'voltage', 'current', 'resistance'], directory='keithley_237', ophyd_device=Keithley_237, requirements=req, files=files, ophyd_class_name='Keithley_237', **kwargs)
        self.config['NPLC'] = 1
        self.config['optionen'] = "2"
        self.config['andere'] = "1 nA"



class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None):
        comboBoxes = {"optionen": ["1", "2", "3"],
                      "andere": ["1 nA", "1 mA"]}
        super().__init__(parent, 'Keithley 237', data, settings_dict,
                         config_dict, ioc_dict, additional_info, comboBoxes=comboBoxes)
        self.comboBox_connection_type.addItem('EPICS: USB-serial')
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
