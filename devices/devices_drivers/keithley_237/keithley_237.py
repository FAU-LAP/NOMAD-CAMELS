from keithley_237.keithley_237_ophyd import Keithley_237

from main_classes import device_class

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        files = []
        req = []
        super().__init__(name='keithley_237', virtual=False, tags=['DMM', 'voltage', 'current',], directory='keithley_237', ophyd_device=Keithley_237, requirements=req, files=files, ophyd_class_name='Keithley_237', **kwargs)
        self.config['Four_wire'] = "False"
        self.config['Averages'] = "1"
        self.config['Integration_time'] = "4ms"
        self.config['Current_compliance_range'] = "Auto"
        self.config['Current_compliance'] = 1e-6
        self.config['Voltage_compliance_range'] = "Auto"
        self.config['Voltage_compliance'] = 10
        self.config['Bias_delay'] = 0
        self.config['Source_Type'] = "Voltage"
        self.config['Sweep_Type'] = "Q0"
        self.config['Sweep_Start'] = 0
        self.config['Sweep_Stop'] = 0
        self.config['Sweep_Step'] = 0
        self.config['Sweep_Pulses'] = 0
        self.config['Sweep_Points'] = 0
        self.config['Sweep_T_on'] = 0
        self.config['Sweep_T_off'] = 0






class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None):
        comboBoxes = {'Source_Type': ["Voltage", "Current", "Sweep Voltage", "Sweep Current"],
                      'Current_compliance_range': ["Auto", "1nA", "10nA", "100nA", "1uA",
                                             "10uA", "100uA", "1mA", "10mA", "100mA"],
                      'Voltage_compliance_range': ["Auto", "1.1V", "11V", "110V", "1100V"],
                      "Four_wire": ["False", "True"],
                      "Averages": ["1", "2", "4", "8", "16", "32"],
                      'Integration_time': ["20ms", "4ms", "0.4ms"],
                      'Sweep_Type' : ["Q0","Q1","Q2","Q3","Q4","Q5",]
                      }
        super().__init__(parent, 'Keithley 237', data, settings_dict,
                         config_dict, ioc_dict, additional_info, comboBoxes=comboBoxes)
        self.comboBox_connection_type.addItem('Local VISA')
        self.comboBox_connection_type.addItem('EPICS: USB-serial')
        self.load_settings()
