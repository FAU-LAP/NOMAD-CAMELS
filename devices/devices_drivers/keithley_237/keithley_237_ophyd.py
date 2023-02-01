from ophyd import Component as Cpt

from bluesky_handling.visa_signal import VISA_Signal_Write, VISA_Signal_Read, VISA_Device



class Keithley_237(VISA_Device):
    mesV = Cpt(VISA_Signal_Read, name='mesV', metadata={'units': 'V'})
    mesI = Cpt(VISA_Signal_Read, name='mesI', metadata={'units': 'A'})
    setV = Cpt(VISA_Signal_Write, name='setV', metadata={'units': 'V'})
    setI = Cpt(VISA_Signal_Write, name='setI', metadata={'units': 'A'})
    enable = Cpt(VISA_Signal_Write, name='enable',)

    idn = Cpt(VISA_Signal_Read, name='idn', kind='config', query_text='U0X')
    Source_Type = Cpt(VISA_Signal_Write, name='Source_Type', kind='config')
    Four_wire = Cpt(VISA_Signal_Write, name='Four_wire', kind='config')
    Averages = Cpt(VISA_Signal_Write, name='Averages', kind='config',)
    Bias_delay = Cpt(VISA_Signal_Write, name='Bias_delay', kind='config',)
    Integration_time = Cpt(VISA_Signal_Write, name='Integration_time', kind='config',)
    Current_compliance_range = Cpt(VISA_Signal_Write, name='Current_compliance_range', kind='config',)
    Current_compliance = Cpt(VISA_Signal_Write, name='Current_compliance', kind='config',)
    Voltage_compliance_range = Cpt(VISA_Signal_Write, name='Voltage_compliance_range', kind='config',)
    Voltage_compliance = Cpt(VISA_Signal_Write, name='Voltage_compliance', kind='config',)


    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 baud_rate=9600, write_termination='\r\n',
                 read_termination='\r\n', **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, baud_rate=baud_rate,
                         write_termination=write_termination,
                         read_termination=read_termination, **kwargs)


        self.setV.put_conv_function = lambda x: self.setV_function(x)

        if self.Source_Type == 'Voltage':
            self.visa_instrument.write('F0,0X')
        elif self.Source_Type == 'Current':
            self.visa_instrument.write('F1,0X')
        elif self.Source_Type == "Sweep Voltage":
            self.visa_instrument.write('F0,1X')
        elif self.Source_Type == "Sweep Current":
            self.visa_instrument.write('F1,1X')


        for comp in self.walk_signals():
            it = comp.item
            it.match_return = True

    def set_function(self, voltage_value):
        write_string = ''
        self.Voltage_compliance_value = self.get_voltage_range_value(self.Voltage_compliance_range.get())
        write_string += f'B{voltage_value},{self.Voltage_compliance_value},{self.Bias_delay}X'
        print(write_string)
        return write_string

    def get_voltage_range_value(self,voltage_range_string):
        voltage_ranges = {"Auto": 0,
                          "1.1V": 1,
                          "11V": 2,
                          "110V": 3,
                          "1100V": 4,}
        return voltage_ranges[voltage_range_string]

    def get_current_range_value(self,current_range_string):
        current_ranges = {"Auto":0,
                          "1nA": 1,
                          "10nA": 2,
                          "100nA": 3,
                          "1uA": 4,
                          "10uA": 5,
                          "100uA": 6,
                          "1mA": 7,
                          "10mA": 8,
                          "100mA": 9,
                          }
        return current_ranges[current_range_string]



    def query_function(self, meas):
        if meas != self.last_meas:
            self.visa_instrument.write(f'CONF:{meas}')
            self.visa_instrument.write(f':{meas}:NPLC ')
            self.last_meas = meas
        else:
            self.visa_instrument.write('INIT')
        return 'DATA?'
if __name__ == '__main__':
    testk = Keithley_237(name='testk')