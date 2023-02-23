from ophyd import Component as Cpt
import numpy as np
import re

from bluesky_handling.visa_signal import VISA_Signal_Write, VISA_Signal_Read, VISA_Device
from bluesky_handling.custom_function_signal import Custom_Function_Signal


def get_current_range_value(current_range_string):
    current_ranges = {"Auto": 0,
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


def get_voltage_range_value(voltage_range_string):
    voltage_ranges = {"Auto": 0,
                      "1.1V": 1,
                      "11V": 2,
                      "110V": 3,
                      "1100V": 4, }
    return voltage_ranges[voltage_range_string]


def get_integration_time_value(integration_time):
    if integration_time:
        integration_times = {"0.4ms": 0,
                             "4ms": 1,
                             "20ms": 3,
                             }
        return integration_times[integration_time]

def read_sweep_array(read_string):
    read_data = np.array(read_string.split(','), dtype=float)
    source_data = []
    for x in read_data[::2]:
        try:
            source_data.append(float(x))
        except:
            match_result = re.match(r'^(\+\d\d.\d)(\+.*)$', x)
            source_data.append(float(match_result[2]))
    source_data = np.array(source_data)
    measure_data = [float(x) for x in read_data[1::2]]
    all_data = np.vstack((source_data,measure_data)).transpose()
    return all_data






class Keithley_237(VISA_Device):
    """
    Driver for the Keithley 237:
    The K237 needs to be initialized before measurement! (set initialize loop-step to any value)
    Basic functions:
    F: Set source and function
    P: Select filter
    S: Set integration time
    W: Enable/ disable default delay
    L: Program compliance
    B: Program bias operation
    Q: Create/append sweep list
    A: Modify sweep list
    T: Select trigger configuration
    R: Enable/ disable triggers
    N: Select operate/ standby mode
    Y: Select terminator characters
    K: Select EOI and hold-off on X
    G: Select output data format
    V: 1100V range control
    J: Execute self-tests
    U: Request status
    H: Send IEEE immediate trigger, H0X needed to actually trigger device
    X: Execute DDCs
    """
    read_DC = Cpt(VISA_Signal_Read, name='read_DC', metadata={'units': 'unit of measure', 'test': '123test'})
    set_DC = Cpt(VISA_Signal_Write, name='set_DC', metadata={'units': 'unit of source', 'test': '123test'})
    start_sweep = Cpt(VISA_Signal_Write, name='start_sweep',)
    read_sweep = Cpt(VISA_Signal_Read, name='read_sweep', query_text='X', metadata={'units': 'first colum is unit of source , second column is unit of measure', 'test': '123test'})
    # Settings for Sweeps
    setSweep_Type = Cpt(Custom_Function_Signal, name='setSweep_Type', )
    setSweep_Level = Cpt(Custom_Function_Signal, name='setSweep_Level', )
    setSweep_Start = Cpt(Custom_Function_Signal, name='Sweep_Start', )
    setSweep_Stop = Cpt(Custom_Function_Signal, name='setSweep_Stop', )
    setSweep_Step = Cpt(Custom_Function_Signal, name='setSweep_Step', )
    setSweep_Pulses = Cpt(Custom_Function_Signal, name='setSweep_Pulses', )
    setSweep_Points = Cpt(Custom_Function_Signal, name='setSweep_Points', )
    setSweep_T_on = Cpt(Custom_Function_Signal, name='setSweep_T_on', )
    setSweep_T_off = Cpt(Custom_Function_Signal, name='setSweep_T_off', )
    # Configuration settings
    idn = Cpt(VISA_Signal_Read, name='idn', kind='config', query_text='U0X', match_return=False)
    Source_Type = Cpt(Custom_Function_Signal, name='Source_Type', kind='config')
    Four_wire = Cpt(Custom_Function_Signal, name='Four_wire', kind='config')
    Averages = Cpt(Custom_Function_Signal, name='Averages', kind='config', )
    Bias_delay = Cpt(Custom_Function_Signal, name='Bias_delay', kind='config', )
    Integration_time = Cpt(Custom_Function_Signal, name='Integration_time', kind='config', )
    Current_compliance_range = Cpt(Custom_Function_Signal, name='Current_compliance_range', kind='config', )
    Current_compliance = Cpt(Custom_Function_Signal, name='Current_compliance', kind='config', )
    Voltage_compliance_range = Cpt(Custom_Function_Signal, name='Voltage_compliance_range', kind='config', )
    Voltage_compliance = Cpt(Custom_Function_Signal, name='Voltage_compliance', kind='config', )
    Sweep_Hysteresis = Cpt(Custom_Function_Signal, name='Sweep_Hysteresis', kind='config', )

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 baud_rate=9600, write_termination='\r\n',
                 read_termination='\r\n', **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, baud_rate=baud_rate,
                         write_termination=write_termination,
                         read_termination=read_termination, **kwargs)
        self.source_range_value = None
        self.compliance_value = None
        self.Integration_time_value = None
        self.compliance_range_value = None
        self.Sweep_Hysteresis_value = None
        self.averages_value = None
        # Setting all the variables with the values of the config settings
        self.Averages.put_function = lambda x: self.Averages_put_function(x)
        self.Integration_time.put_function = lambda x: self.Integration_time_put_function(x)
        self.Voltage_compliance.put_function = lambda x: self.Voltage_compliance_put_function(x)
        self.Sweep_Hysteresis.put_function = lambda x: self.Sweep_Hysteresis_put_function(x)
        # set functions of the settable channels
        self.set_DC.put_conv_function = self.set_DC_function
        self.read_DC.read_function = self.read_DC_function
        self.start_sweep.put_conv_function = lambda x: self.start_sweep_function()

    def Voltage_compliance_put_function(self, volt_value):
        value = self.Source_Type.get()
        if value == 'Voltage':
            self.source_range_value = get_voltage_range_value(self.Voltage_compliance_range.get())
            print(f'{self.source_range_value=}')
            self.compliance_range_value = get_current_range_value(self.Current_compliance_range.get())
            self.compliance_value = self.Current_compliance.get()
            self.set_DC.metadata['units'] = 'V'
            self.read_DC.metadata['units'] = 'V'
            self.visa_instrument.write('F0,0X')
            self.visa_instrument.write('G4,2,0X')
            # print(f'{self.Current_compliance.get()=}')
        elif value == 'Current':
            self.source_range_value = get_current_range_value(self.Current_compliance_range.get())
            self.compliance_range_value = get_voltage_range_value(self.Voltage_compliance_range.get())
            self.compliance_value = self.Voltage_compliance.get()
            self.set_DC.metadata['units'] = 'A'
            self.read_DC.metadata['units'] = 'A'
            self.visa_instrument.write('F1,0X')
            self.visa_instrument.write('G4,2,0X')
        # self.visa_instrument.write(f'L{self.compliance_value},{self.compliance_range_value}X')
            # self.visa_instrument.write(f'L{self.compliance_value},{self.compliance_range_value}')
        elif value == "Sweep Voltage":
            self.source_range_value = get_voltage_range_value(self.Voltage_compliance_range.get())
            self.compliance_range_value = get_current_range_value(self.Current_compliance_range.get())
            self.compliance_value = self.Current_compliance.get()
            self.start_sweep.metadata['units'] = 'V'
            self.read_sweep.metadata['units'] = 'V'
            self.visa_instrument.write('F0,1X')
            self.visa_instrument.write('G5,2,2X')
            self.read_sweep.process_read_function = read_sweep_array
            # self.visa_instrument.write(f'L{self.compliance_value},{self.compliance_range_value}')
        elif value == "Sweep Current":
            self.source_range_value = get_current_range_value(self.Current_compliance_range.get())
            self.compliance_range_value = get_voltage_range_value(self.Voltage_compliance_range.get())
            self.compliance_value = self.Voltage_compliance.get()
            self.start_sweep.metadata['units'] = 'A'
            self.read_sweep.metadata['units'] = 'A'
            self.visa_instrument.write('F1,1X')
            self.visa_instrument.write('G5,2,2X')
            self.read_sweep.process_read_function = read_sweep_array
        return

    def Averages_put_function(self, value):
        self.averages_value = int(np.log2(int(value)))

    def Sweep_Hysteresis_put_function(self,value):
        self.Sweep_Hysteresis_value = value
        print(f'{self.Sweep_Hysteresis_value=}')

    def Integration_time_put_function(self,value):
        self.Integration_time_value =get_integration_time_value(value)
        print(f'P{self.averages_value}XS{self.Integration_time_value}X')
        self.visa_instrument.write(f'P{self.averages_value}XS{self.Integration_time_value}X')

    def set_DC_function(self, set_value):
        write_string = ''
        if self.Source_Type.get() == 'Voltage':
            # self.source_range_value = get_voltage_range_value(self.Voltage_compliance_range.get())
            write_string += f'B{set_value},{self.source_range_value},{int(self.Bias_delay.get())}XN1X'
        elif self.Source_Type.get() == 'Current':
            # self.source_range_value = get_current_range_value(self.Current_compliance_range.get())
            write_string += f'B{set_value},{self.source_range_value},{int(self.Bias_delay.get())}XN1X'
        print(write_string)
        print(self.averages_value)
        return write_string

    def read_DC_function(self,):
        self.visa_instrument.write('H0X')
        return ''

    def start_sweep_function(self):
        # Fixed level: points = counts
        if self.setSweep_Type.get() == 0:
            write_string = (f'Q0,{self.setSweep_Level.get()},{self.compliance_range_value},'
                            f'{int(self.Bias_delay.get())},{self.setSweep_Points.get()}X')
            if self.Sweep_Hysteresis_value:
                write_string += (f'Q6,{self.setSweep_Level.get()},{self.compliance_range_value},'
                                 f'{int(self.Bias_delay.get())},{self.setSweep_Points.get()}X')

        # Linear stair
        elif self.setSweep_Type.get() == 1:
            write_string = (f'Q1,{self.setSweep_Start.get()},{self.setSweep_Stop.get()},'
                            f'{self.setSweep_Step.get()},{self.compliance_range_value},{int(self.Bias_delay.get())}X')
            if self.Sweep_Hysteresis_value:
                write_string += (f'Q7,{self.setSweep_Stop.get()},{self.setSweep_Start.get()},'
                                 f'{self.setSweep_Step.get()},{self.compliance_range_value}, {int(self.Bias_delay.get())}X')
        # Logarithmic stair
        elif self.setSweep_Type.get() == 2:
            write_string = (f'Q2,{self.setSweep_Start.get()},{self.setSweep_Stop.get()},'
                            f'{self.setSweep_Points.get()},{self.compliance_range_value}, {int(self.Bias_delay.get())}X')
            if self.Sweep_Hysteresis_value:
                write_string += (f'Q8,{self.setSweep_Stop.get()},{self.setSweep_Start.get()},'
                                 f'{self.setSweep_Points.get()},{self.compliance_range_value}, {int(self.Bias_delay.get())}X')
        # Fixed level pulsed
        elif self.setSweep_Type.get() == 3:
            write_string = (f'Q3,{self.setSweep_Level.get()},{self.compliance_range_value},'
                            f'{self.setSweep_Pulses.get()},{self.setSweep_T_on.get()},{self.setSweep_T_off.get()}X')
            if self.Sweep_Hysteresis_value:
                write_string += (f'Q9,{self.setSweep_Level.get()},{self.compliance_range_value},'
                                 f'{self.setSweep_Pulses.get()},{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X')
        # Linear Stair pulsed
        elif self.setSweep_Type.get() == 4:
            write_string = (f'Q4,{self.setSweep_Start.get()},{self.setSweep_Stop.get()},'
                            f'{self.setSweep_Step.get()},{self.compliance_range_value}, '
                            f',{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X')
            if self.Sweep_Hysteresis_value:
                write_string += (f'Q10,{self.setSweep_Stop.get()},{self.setSweep_Start.get()},'
                                 f'{self.setSweep_Step.get()},{self.compliance_range_value}, '
                                 f',{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X')
        # Logarithmic stair pulsed
        elif self.setSweep_Type.get() == 5:
            write_string = (f'Q5,{self.setSweep_Start.get()},{self.setSweep_Stop.get()},'
                            f'{self.setSweep_Points.get()},{self.compliance_range_value}, '
                            f',{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X')
            if self.Sweep_Hysteresis_value:
                write_string += (f'Q11,{self.setSweep_Stop.get()},{self.setSweep_Start.get()},'
                                 f'{self.setSweep_Points.get()},{self.compliance_range_value}, '
                                 f',{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X')
        write_string += 'N1XH0X'
        print(write_string)
        return write_string



if __name__ == '__main__':
    testk = Keithley_237(name='testk')
