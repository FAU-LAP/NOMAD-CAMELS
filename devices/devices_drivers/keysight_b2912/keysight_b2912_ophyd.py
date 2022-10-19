from ophyd import Device
from ophyd import Component as Cpt

from bluesky_handling.visa_signal import VISA_Signal_Read, VISA_Signal_Write, rm, open_resources


def source_func(inp, chan, volt_source):
    if inp == 'Voltage':
        v = 'VOLT'
        volt_source[chan-1] = True
    else:
        v = 'CURR'
        volt_source[chan-1] = False
    return f':SOUR{chan}:{v}'

def source_range_func(inp, chan, volt_source):
    v = 'VOLT' if volt_source[chan-1] else 'CURR'
    return f':SOUR{chan}:{v}:{inp[:-2]}'

def source_auto_func(inp, chan, volt_source):
    v = 'VOLT' if volt_source[chan-1] else 'CURR'
    m = 'ON' if inp else 'OFF'
    return f':SOUR{chan}:{v}:AUTO {m}'

def range_lower_lim_func(inp, chan, volt_source):
    v = 'VOLT' if volt_source[chan-1] else 'CURR'
    return f':SOUR{chan}:{v}:AUTO:LLIM {inp[:-2]}'

def output_protection_func(inp, chan):
    v = 'ON' if inp else 'OFF'
    return f':OUTP{chan}:PROT {v}'

def range_func(inp, chan, typ):
    return f'SENS{chan}:{typ}:RANG {inp}'

def low_terminal_func(inp, chan):
    v = 'GRO' if inp == 'Ground' else 'FLO'
    return f':OUTP{chan}:LOW {v};'

def four_wire_meas_func(inp, chan):
    v = 'ON' if inp else 'OFF'
    return f':SENS{chan}:REM {v}'

def auto_range_func(inp, chan, typ):
    v = 'ON' if inp else 'OFF'
    return f':SENS{chan}:{typ}:RANG:AUTO {v}'

def auto_range_lower_lim_func(inp, chan, typ):
    return f':SENS{chan}:{typ}:RANG:AUTO:LLIM {inp[:-2]}'

def auto_range_upper_lim_func(inp, chan, typ):
    return f':SENS{chan}:{typ}:RANG:AUTO:ULIM {inp[:-2]}'

def res_comp_func(inp, chan):
    v = 'ON' if inp else 'OFF'
    return f':SENS{chan}:RES:OCOM {v}'

def auto_range_mode_func(inp, chan, typ):
    if inp == 'Normal':
        v = 'NORM'
    elif inp == 'Resolution':
        v = 'RES'
    else:
        v = 'SPE'
    return f':SENS{chan}:{typ}:RANG:AUTO:MODE {v}'

def NPLC_func(inp, chan):
    return f':SENS{chan}:VOLT:NPLC {inp}; :SENS{chan}:CURR:NPLC {inp}; :SENS{chan}:RES:NPLC {inp};'

def enable_func(inp, chan):
    v = 'ON' if inp else 'OFF'
    return f':OUTP{chan} {v}'




class Keysight_B2912(Device):
    mesV1 = Cpt(VISA_Signal_Read, name='mesV1', query_text='MEAS:VOLT? (@1)')
    mesI1 = Cpt(VISA_Signal_Read, name='mesI1', query_text='MEAS:CURR? (@1)')
    mesV2 = Cpt(VISA_Signal_Read, name='mesV2', query_text='MEAS:VOLT? (@2)')
    mesI2 = Cpt(VISA_Signal_Read, name='mesI2', query_text='MEAS:CURR? (@2)')
    setV1 = Cpt(VISA_Signal_Write, name='setV1', additional_put_text='SOUR1:VOLT ')
    setI1 = Cpt(VISA_Signal_Write, name='setI1', additional_put_text='SOUR1:CURR ')
    setV2 = Cpt(VISA_Signal_Write, name='setV2', additional_put_text='SOUR2:VOLT ')
    setI2 = Cpt(VISA_Signal_Write, name='setI2', additional_put_text='SOUR2:CURR ')

    enable1 = Cpt(VISA_Signal_Write, name='enable1', put_conv_function=lambda x: enable_func(x, 1))
    enable2 = Cpt(VISA_Signal_Write, name='enable2', put_conv_function=lambda x: enable_func(x, 2))

    idn = Cpt(VISA_Signal_Read, name='idn', query_text='*IDN?', kind='config')

    source1 = Cpt(VISA_Signal_Write, name="source1", kind='config')
    source_range1 = Cpt(VISA_Signal_Write, name="source_range1", kind='config')
    range_lower_lim1 = Cpt(VISA_Signal_Write, name="range_lower_lim1", kind='config')
    source_auto1 = Cpt(VISA_Signal_Write, name="source_auto1", kind='config')
    low_terminal1 = Cpt(VISA_Signal_Write, name="low_terminal1", kind='config', put_conv_function=lambda x: low_terminal_func(x, 1))
    current_auto_mode1 = Cpt(VISA_Signal_Write, name="current_auto_mode1", kind='config', put_conv_function=lambda x: auto_range_mode_func(x, 1, 'CURR'))
    current_lower_lim1 = Cpt(VISA_Signal_Write, name="current_lower_lim1", kind='config', put_conv_function=lambda x: auto_range_lower_lim_func(x, 1, 'CURR'))
    current_range1 = Cpt(VISA_Signal_Write, name="current_range1", kind='config', put_conv_function=lambda x: range_func(x, 1, 'CURR'))
    voltage_range1 = Cpt(VISA_Signal_Write, name="voltage_range1", kind='config', put_conv_function=lambda x: range_func(x, 1, 'VOLT'))
    voltage_auto_mode1 = Cpt(VISA_Signal_Write, name="voltage_auto_mode1", kind='config', put_conv_function=lambda x: auto_range_mode_func(x, 1, 'VOLT'))
    voltage_lower_lim1 = Cpt(VISA_Signal_Write, name="voltage_lower_lim1", kind='config', put_conv_function=lambda x: auto_range_lower_lim_func(x, 1, 'VOLT'))
    resistance_range1 = Cpt(VISA_Signal_Write, name="resistance_range1", kind='config', put_conv_function=lambda x: range_func(x, 1, 'RES'))
    resistance_upper_lim1 = Cpt(VISA_Signal_Write, name="resistance_upper_lim1", kind='config', put_conv_function=lambda x: auto_range_upper_lim_func(x, 1, 'RES'))
    output_protection1 = Cpt(VISA_Signal_Write, name="output_protection1", kind='config', put_conv_function=lambda x: output_protection_func(x, 1))
    four_wire_meas1 = Cpt(VISA_Signal_Write, name="four_wire_meas1", kind='config', put_conv_function=lambda x: four_wire_meas_func(x, 1))
    current_auto_range1 = Cpt(VISA_Signal_Write, name="current_auto_range1", kind='config', put_conv_function=lambda x: auto_range_func(x, 1, 'CURR'))
    voltage_auto_range1 = Cpt(VISA_Signal_Write, name="voltage_auto_range1", kind='config', put_conv_function=lambda x: auto_range_func(x, 1, 'VOLT'))
    resistance_auto_range1 = Cpt(VISA_Signal_Write, name="resistance_auto_range1", kind='config', put_conv_function=lambda x: auto_range_func(x, 1, 'RES'))
    resistance_compensation1 = Cpt(VISA_Signal_Write, name="resistance_compensation1", kind='config', put_conv_function=lambda x: res_comp_func(x, 1))
    voltage_compliance1 = Cpt(VISA_Signal_Write, name="voltage_compliance1", kind='config', additional_put_text=':SENS1:CURR:PROT ')
    current_compliance1 = Cpt(VISA_Signal_Write, name="current_compliance1", kind='config', additional_put_text=':SENS1:VOLT:PROT ')
    NPLC1 = Cpt(VISA_Signal_Write, name="NPLC1", kind='config', put_conv_function=lambda x: NPLC_func(x, 1))

    source2 = Cpt(VISA_Signal_Write, name="source2", kind='config')
    source_range2 = Cpt(VISA_Signal_Write, name="source_range2", kind='config')
    range_lower_lim2 = Cpt(VISA_Signal_Write, name="range_lower_lim2", kind='config')
    source_auto2 = Cpt(VISA_Signal_Write, name="source_auto2", kind='config')
    low_terminal2 = Cpt(VISA_Signal_Write, name="low_terminal2", kind='config', put_conv_function=lambda x: low_terminal_func(x, 2))
    current_auto_mode2 = Cpt(VISA_Signal_Write, name="current_auto_mode2", kind='config', put_conv_function=lambda x: auto_range_mode_func(x, 2, 'CURR'))
    current_lower_lim2 = Cpt(VISA_Signal_Write, name="current_lower_lim2", kind='config', put_conv_function=lambda x: auto_range_lower_lim_func(x, 2, 'CURR'))
    current_range2 = Cpt(VISA_Signal_Write, name="current_range2", kind='config', put_conv_function=lambda x: range_func(x, 2, 'CURR'))
    voltage_range2 = Cpt(VISA_Signal_Write, name="voltage_range2", kind='config', put_conv_function=lambda x: range_func(x, 2, 'VOLT'))
    voltage_auto_mode2 = Cpt(VISA_Signal_Write, name="voltage_auto_mode2", kind='config', put_conv_function=lambda x: auto_range_mode_func(x, 2, 'VOLT'))
    voltage_lower_lim2 = Cpt(VISA_Signal_Write, name="voltage_lower_lim2", kind='config', put_conv_function=lambda x: auto_range_lower_lim_func(x, 2, 'VOLT'))
    resistance_range2 = Cpt(VISA_Signal_Write, name="resistance_range2", kind='config', put_conv_function=lambda x: range_func(x, 2, 'RES'))
    resistance_upper_lim2 = Cpt(VISA_Signal_Write, name="resistance_upper_lim2", kind='config', put_conv_function=lambda x: auto_range_upper_lim_func(x, 2, 'RES'))
    output_protection2 = Cpt(VISA_Signal_Write, name="output_protection2", kind='config', put_conv_function=lambda x: output_protection_func(x, 2))
    four_wire_meas2 = Cpt(VISA_Signal_Write, name="four_wire_meas2", kind='config', put_conv_function=lambda x: four_wire_meas_func(x, 2))
    current_auto_range2 = Cpt(VISA_Signal_Write, name="current_auto_range2", kind='config', put_conv_function=lambda x: auto_range_func(x, 2, 'CURR'))
    voltage_auto_range2 = Cpt(VISA_Signal_Write, name="voltage_auto_range2", kind='config', put_conv_function=lambda x: auto_range_func(x, 2, 'VOLT'))
    resistance_auto_range2 = Cpt(VISA_Signal_Write, name="resistance_auto_range2", kind='config', put_conv_function=lambda x: auto_range_func(x, 2, 'RES'))
    resistance_compensation2 = Cpt(VISA_Signal_Write, name="resistance_compensation2", kind='config', put_conv_function=lambda x: res_comp_func(x, 2))
    voltage_compliance2 = Cpt(VISA_Signal_Write, name="voltage_compliance2", kind='config', additional_put_text=':SENS2:CURR:PROT ')
    current_compliance2 = Cpt(VISA_Signal_Write, name="current_compliance2", kind='config', additional_put_text=':SENS2:VOLT:PROT ')
    NPLC2 = Cpt(VISA_Signal_Write, name="NPLC2", kind='config', put_conv_function=lambda x: NPLC_func(x, 2))


    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='', **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        self.visa_instrument = None
        if resource_name:
            if resource_name in open_resources:
                self.visa_instrument = open_resources[resource_name]
            else:
                self.visa_instrument = rm.open_resource(resource_name)
                open_resources[resource_name] = self.visa_instrument
            # self.visa_instrument.write_termination = '\r\n'
            self.visa_instrument.read_termination = '\n'
            # self.visa_instrument.baud_rate = 9600


        self.v_source = [True, True]

        self.source1.put_conv_function = lambda x: source_func(x, 1, self.v_source)
        self.source_range1.put_conv_function = lambda x: source_range_func(x, 1, self.v_source)
        self.range_lower_lim1.put_conv_function = lambda x: range_lower_lim_func(x, 1, self.v_source)
        self.source_auto1.put_conv_function = lambda x: source_auto_func(x, 1, self.v_source)

        self.source2.put_conv_function = lambda x: source_func(x, 2, self.v_source)
        self.source_range2.put_conv_function = lambda x: source_range_func(x, 2, self.v_source)
        self.range_lower_lim2.put_conv_function = lambda x: range_lower_lim_func(x, 2, self.v_source)
        self.source_auto2.put_conv_function = lambda x: source_auto_func(x, 2, self.v_source)

        # self.idn.visa_instrument = self.visa_instrument

        for comp in self.walk_signals():
            it = comp.item
            it.visa_instrument = self.visa_instrument

if __name__ == '__main__':
    b29 = Keysight_B2912('test', name='b29', resource_name='USB0::0x0957::0x8E18::MY51140626::INSTR')
    print(b29.idn.get())
