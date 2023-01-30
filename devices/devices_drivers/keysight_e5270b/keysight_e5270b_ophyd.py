from ophyd import EpicsSignal, EpicsSignalRO, Device
from ophyd import Component as Cpt
from bluesky_handling.visa_signal import VISA_Signal_Read, VISA_Signal_Write, VISA_Device
from bluesky_handling import TriggerEpicsSignalRO
from bluesky_handling.custom_function_signal import (Custom_Function_Signal,
                                                     Custom_Function_SignalRO)
import time as ttime


class Keysight_E5270B(VISA_Device):
    speedADCPLC = Cpt(Custom_Function_Signal, name='speedADCPLC', kind='config')
    speedADCmode = Cpt(Custom_Function_Signal, name='speedADCmode', kind='config')
    resADCPLC = Cpt(Custom_Function_Signal, name='resADCPLC', kind='config')
    resADCmode = Cpt(Custom_Function_Signal, name='resADCmode', kind='config')
    idn = Cpt(VISA_Signal_Read, name='idn', kind='config', 
              read_function= lambda:'*IDN?')
    err = Cpt(Custom_Function_Signal, name='err',)
    # --------------------Channel 1----------------------------------------
    setV1 = Cpt(VISA_Signal_Write, name='setV1', metadata={'units': 'V'})
    setI1 = Cpt(VISA_Signal_Write, name='setI1', metadata={'units': 'A'})
    mesI1 = Cpt(VISA_Signal_Read, name='mesI1', metadata={'units': 'A'})
    mesV1 = Cpt(VISA_Signal_Read, name='mesV1', metadata={'units': 'V'})
    enable1 = Cpt(VISA_Signal_Write, name='enable1',)
    # Config settings of the device
    measMode1 = Cpt(VISA_Signal_Write, name='measMode1', kind='config',)
    # used in setting current DI and setting voltage DV, only a variable
    currComp1 = Cpt(Custom_Function_Signal, name='currComp1', kind='config',)
    voltComp1 = Cpt(Custom_Function_Signal, name='voltComp1', kind='config')
    # voltage range used when setting DV
    VoutRange1 = Cpt(Custom_Function_Signal, name='VoutRange1', kind='config')
    # current range used when setting DI
    IoutRange1 = Cpt(Custom_Function_Signal, name='IoutRange1', kind='config')
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange1 = Cpt(VISA_Signal_Write, name='VmeasRange1', kind='config')
    # current range used when simply using (MM, CMM and XE)
    ImeasRange1 = Cpt(VISA_Signal_Write, name='ImeasRange1', kind='config')
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC1 = Cpt(VISA_Signal_Write, name='setADC1', kind='config',)
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter1 = Cpt(VISA_Signal_Write, name='outputFilter1', kind='config', )
    # --------------------Channel 2----------------------------------------
    setV2 = Cpt(VISA_Signal_Write, name='setV2', metadata={'units': 'V'})
    setI2 = Cpt(VISA_Signal_Write, name='setI2', metadata={'units': 'A'})
    mesI2 = Cpt(VISA_Signal_Read, name='mesI2', metadata={'units': 'A'})
    mesV2 = Cpt(VISA_Signal_Read, name='mesV2', metadata={'units': 'V'})
    enable2 = Cpt(VISA_Signal_Write, name='enable2', )
    # Config settings of the device
    measMode2 = Cpt(VISA_Signal_Write, name='measMode2', kind='config', )
    # used in setting current DI and setting voltage DV, only a variable
    currComp2 = Cpt(Custom_Function_Signal, name='currComp2', kind='config', )
    voltComp2 = Cpt(Custom_Function_Signal, name='voltComp2', kind='config')
    # voltage range used when setting DV
    VoutRange2 = Cpt(Custom_Function_Signal, name='VoutRange2', kind='config')
    # current range used when setting DI
    IoutRange2 = Cpt(Custom_Function_Signal, name='IoutRange2', kind='config')
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange2 = Cpt(VISA_Signal_Write, name='VmeasRange2', kind='config')
    # current range used when simply using (MM, CMM and XE)
    ImeasRange2 = Cpt(VISA_Signal_Write, name='ImeasRange2', kind='config')
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC2 = Cpt(VISA_Signal_Write, name='setADC2', kind='config', )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter2 = Cpt(VISA_Signal_Write, name='outputFilter2', kind='config', )
    # --------------------Channel 3----------------------------------------
    setV3 = Cpt(VISA_Signal_Write, name='setV3', metadata={'units': 'V'})
    setI3 = Cpt(VISA_Signal_Write, name='setI3', metadata={'units': 'A'})
    mesI3 = Cpt(VISA_Signal_Read, name='mesI3', metadata={'units': 'A'})
    mesV3 = Cpt(VISA_Signal_Read, name='mesV3', metadata={'units': 'V'})
    enable3 = Cpt(VISA_Signal_Write, name='enable3', )
    # Config settings of the device
    measMode3 = Cpt(VISA_Signal_Write, name='measMode3', kind='config', )
    # used in setting current DI and setting voltage DV, only a variable
    currComp3 = Cpt(Custom_Function_Signal, name='currComp3', kind='config', )
    voltComp3 = Cpt(Custom_Function_Signal, name='voltComp3', kind='config')
    # voltage range used when setting DV
    VoutRange3 = Cpt(Custom_Function_Signal, name='VoutRange3', kind='config')
    # current range used when setting DI
    IoutRange3 = Cpt(Custom_Function_Signal, name='IoutRange3', kind='config')
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange3 = Cpt(VISA_Signal_Write, name='VmeasRange3', kind='config')
    # current range used when simply using (MM, CMM and XE)
    ImeasRange3 = Cpt(VISA_Signal_Write, name='ImeasRange3', kind='config')
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC3 = Cpt(VISA_Signal_Write, name='setADC3', kind='config', )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter3 = Cpt(VISA_Signal_Write, name='outputFilter3', kind='config', )
    # --------------------Channel 4----------------------------------------
    setV4 = Cpt(VISA_Signal_Write, name='setV4', metadata={'units': 'V'})
    setI4 = Cpt(VISA_Signal_Write, name='setI4', metadata={'units': 'A'})
    mesI4 = Cpt(VISA_Signal_Read, name='mesI4', metadata={'units': 'A'})
    mesV4 = Cpt(VISA_Signal_Read, name='mesV4', metadata={'units': 'V'})
    enable4 = Cpt(VISA_Signal_Write, name='enable4', )
    # Config settings of the device
    measMode4 = Cpt(VISA_Signal_Write, name='measMode4', kind='config', )
    # used in setting current DI and setting voltage DV, only a variable
    currComp4 = Cpt(Custom_Function_Signal, name='currComp4', kind='config', )
    voltComp4 = Cpt(Custom_Function_Signal, name='voltComp4', kind='config')
    # voltage range used when setting DV
    VoutRange4 = Cpt(Custom_Function_Signal, name='VoutRange4', kind='config')
    # current range used when setting DI
    IoutRange4 = Cpt(Custom_Function_Signal, name='IoutRange4', kind='config')
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange4 = Cpt(VISA_Signal_Write, name='VmeasRange4', kind='config')
    # current range used when simply using (MM, CMM and XE)
    ImeasRange4 = Cpt(VISA_Signal_Write, name='ImeasRange4', kind='config')
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC4 = Cpt(VISA_Signal_Write, name='setADC4', kind='config', )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter4 = Cpt(VISA_Signal_Write, name='outputFilter4', kind='config', )
    # --------------------Channel 5----------------------------------------
    setV5 = Cpt(VISA_Signal_Write, name='setV5', metadata={'units': 'V'})
    setI5 = Cpt(VISA_Signal_Write, name='setI5', metadata={'units': 'A'})
    mesI5 = Cpt(VISA_Signal_Read, name='mesI5', metadata={'units': 'A'})
    mesV5 = Cpt(VISA_Signal_Read, name='mesV5', metadata={'units': 'V'})
    enable5 = Cpt(VISA_Signal_Write, name='enable5', )
    # Config settings of the device
    measMode5 = Cpt(VISA_Signal_Write, name='measMode5', kind='config', )
    # used in setting current DI and setting voltage DV, only a variable
    currComp5 = Cpt(Custom_Function_Signal, name='currComp5', kind='config', )
    voltComp5 = Cpt(Custom_Function_Signal, name='voltComp5', kind='config')
    # voltage range used when setting DV
    VoutRange5 = Cpt(Custom_Function_Signal, name='VoutRange5', kind='config')
    # current range used when setting DI
    IoutRange5 = Cpt(Custom_Function_Signal, name='IoutRange5', kind='config')
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange5 = Cpt(VISA_Signal_Write, name='VmeasRange5', kind='config')
    # current range used when simply using (MM, CMM and XE)
    ImeasRange5 = Cpt(VISA_Signal_Write, name='ImeasRange5', kind='config')
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC5 = Cpt(VISA_Signal_Write, name='setADC5', kind='config', )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter5 = Cpt(VISA_Signal_Write, name='outputFilter5', kind='config', )
    # --------------------Channel 6----------------------------------------
    setV6 = Cpt(VISA_Signal_Write, name='setV6', metadata={'units': 'V'})
    setI6 = Cpt(VISA_Signal_Write, name='setI6', metadata={'units': 'A'})
    mesI6 = Cpt(VISA_Signal_Read, name='mesI6', metadata={'units': 'A'})
    mesV6 = Cpt(VISA_Signal_Read, name='mesV6', metadata={'units': 'V'})
    enable6 = Cpt(VISA_Signal_Write, name='enable6', )
    # Config settings of the device
    measMode6 = Cpt(VISA_Signal_Write, name='measMode6', kind='config', )
    # used in setting current DI and setting voltage DV, only a variable
    currComp6 = Cpt(Custom_Function_Signal, name='currComp6', kind='config', )
    voltComp6 = Cpt(Custom_Function_Signal, name='voltComp6', kind='config')
    # voltage range used when setting DV
    VoutRange6 = Cpt(Custom_Function_Signal, name='VoutRange6', kind='config')
    # current range used when setting DI
    IoutRange6 = Cpt(Custom_Function_Signal, name='IoutRange6', kind='config')
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange6 = Cpt(VISA_Signal_Write, name='VmeasRange6', kind='config')
    # current range used when simply using (MM, CMM and XE)
    ImeasRange6 = Cpt(VISA_Signal_Write, name='ImeasRange6', kind='config')
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC6 = Cpt(VISA_Signal_Write, name='setADC6', kind='config', )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter6 = Cpt(VISA_Signal_Write, name='outputFilter6', kind='config', )
    # --------------------Channel 7----------------------------------------
    setV7 = Cpt(VISA_Signal_Write, name='setV7', metadata={'units': 'V'})
    setI7 = Cpt(VISA_Signal_Write, name='setI7', metadata={'units': 'A'})
    mesI7 = Cpt(VISA_Signal_Read, name='mesI7', metadata={'units': 'A'})
    mesV7 = Cpt(VISA_Signal_Read, name='mesV7', metadata={'units': 'V'})
    enable7 = Cpt(VISA_Signal_Write, name='enable7', )
    # Config settings of the device
    measMode7 = Cpt(VISA_Signal_Write, name='measMode7', kind='config', )
    # used in setting current DI and setting voltage DV, only a variable
    currComp7 = Cpt(Custom_Function_Signal, name='currComp7', kind='config', )
    voltComp7 = Cpt(Custom_Function_Signal, name='voltComp7', kind='config')
    # voltage range used when setting DV
    VoutRange7 = Cpt(Custom_Function_Signal, name='VoutRange7', kind='config')
    # current range used when setting DI
    IoutRange7 = Cpt(Custom_Function_Signal, name='IoutRange7', kind='config')
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange7 = Cpt(VISA_Signal_Write, name='VmeasRange7', kind='config')
    # current range used when simply using (MM, CMM and XE)
    ImeasRange7 = Cpt(VISA_Signal_Write, name='ImeasRange7', kind='config')
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC7 = Cpt(VISA_Signal_Write, name='setADC7', kind='config', )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter7 = Cpt(VISA_Signal_Write, name='outputFilter7', kind='config', )
    # --------------------Channel 8----------------------------------------
    setV8 = Cpt(VISA_Signal_Write, name='setV8', metadata={'units': 'V'})
    setI8 = Cpt(VISA_Signal_Write, name='setI8', metadata={'units': 'A'})
    mesI8 = Cpt(VISA_Signal_Read, name='mesI8', metadata={'units': 'A'})
    mesV8 = Cpt(VISA_Signal_Read, name='mesV8', metadata={'units': 'V'})
    enable8 = Cpt(VISA_Signal_Write, name='enable8', )
    # Config settings of the device
    measMode8 = Cpt(VISA_Signal_Write, name='measMode8', kind='config', )
    # used in setting current DI and setting voltage DV, only a variable
    currComp8 = Cpt(Custom_Function_Signal, name='currComp8', kind='config', )
    voltComp8 = Cpt(Custom_Function_Signal, name='voltComp8', kind='config')
    # voltage range used when setting DV
    VoutRange8 = Cpt(Custom_Function_Signal, name='VoutRange8', kind='config')
    # current range used when setting DI
    IoutRange8 = Cpt(Custom_Function_Signal, name='IoutRange8', kind='config')
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange8 = Cpt(VISA_Signal_Write, name='VmeasRange8', kind='config')
    # current range used when simply using (MM, CMM and XE)
    ImeasRange8 = Cpt(VISA_Signal_Write, name='ImeasRange8', kind='config')
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC8 = Cpt(VISA_Signal_Write, name='setADC8', kind='config', )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter8 = Cpt(VISA_Signal_Write, name='outputFilter8', kind='config', )

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, use_channels=(), **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        self.use_channels = use_channels

        if use_channels:
            comps = list(self.component_names)
            for comp in self.component_names:
                for i in range(1, 9):
                    if i not in self.use_channels and str(i) in comp:
                        comps.remove(comp)
                        break
            self.component_names = tuple(comps)

        # array of current compliances for each of the 8 channels
        # array[i] corresponds to channel number i+1
        self.curr_compliance_array = [0, 0, 0, 0, 0, 0, 0, 0]
        # array of voltage compliances for each of the 8 channels
        # array[i] corresponds to channel number i+1
        self.volt_compliance_array = [0, 0, 0, 0, 0, 0, 0, 0]
        # arrays containing the last values set for MM and CMM for each channel
        self.last_MM_value = [None, None, None, None, None, None, None, None]
        self.last_CMM_value = [None, None, None, None, None, None, None, None]
        # the last channel set in with the MM command is read when executing 'XE'
        self.last_MM_channel = None
        #Mode and NPLC of the High Res AD converters for the entire SMU
        self.resADCmode.put_conv_function = lambda x: self.set_ADC_mode(1, x)
        #Mode and NPLC of the High Speed AD converters for the entire SMU
        self.speedADCmode.put_conv_function = lambda x: self.set_ADC_mode(0, x)
        self.err.put_conv_function = lambda: 'ERR?'
        # --------------------Channel 1----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp1.put_function = lambda x: self.set_voltCompliance(x, 1)
        self.setI1.put_conv_function = lambda x: self.source_current(x, 1, self.IoutRange1, )
        # set array element of curr compliance to the value entered
        self.currComp1.put_function = lambda x: self.set_currCompliance(x, 1, )
        self.setV1.put_conv_function = lambda x: self.source_voltage(x, 1, self.VoutRange1)
        self.enable1.put_conv_function = lambda x: f'CN 1'
        self.setADC1.put_conv_function = lambda x: f'AAD 1,{x}'
        self.outputFilter1.put_conv_function = lambda x: f'FL {x},1'
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV1.read_function = lambda: self.measure_single_voltage(1)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI1.read_function = lambda: self.measure_single_current(1)
        # function called when putting value to measMode1
        self.measMode1.put_conv_function = lambda x: self.set_MM_value(x, 1)
        # function called when putting value to currComp1
        self.ImeasRange1.put_conv_function = lambda x: f'RI 1,{x}'
        # function called when putting value to voltComp1
        self.VmeasRange1.put_conv_function = lambda x: f'RV 1,{x}'
        # --------------------Channel 2----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp2.put_function = lambda x: self.set_voltCompliance(x, 2)
        self.setI2.put_conv_function = lambda x: self.source_current(x, 2, self.IoutRange2, )
        # set array element of curr compliance to the value entered
        self.currComp2.put_function = lambda x: self.set_currCompliance(x, 2, )
        self.setV2.put_conv_function = lambda x: self.source_voltage(x, 2, self.VoutRange2)
        self.enable2.put_conv_function = lambda x: f'CN 2'
        self.setADC2.put_conv_function = lambda x: f'AAD 2,{x}'
        self.outputFilter2.put_conv_function = lambda x: f'FL {x},2'
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV2.read_function = lambda: self.measure_single_voltage(2)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI2.read_function = lambda: self.measure_single_current(2)
        # function called when putting value to measMode2
        self.measMode2.put_conv_function = lambda x: self.set_MM_value(x, 2)
        # function called when putting value to currComp2
        self.ImeasRange2.put_conv_function = lambda x: f'RI 2,{x}'
        # function called when putting value to voltComp2
        self.VmeasRange2.put_conv_function = lambda x: f'RV 2,{x}'
        # --------------------Channel 3----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp3.put_function = lambda x: self.set_voltCompliance(x, 3)
        self.setI3.put_conv_function = lambda x: self.source_current(x, 3, self.IoutRange3, )
        # set array element of curr compliance to the value entered
        self.currComp3.put_function = lambda x: self.set_currCompliance(x, 3, )
        self.setV3.put_conv_function = lambda x: self.source_voltage(x, 3, self.VoutRange3)
        self.enable3.put_conv_function = lambda x: f'CN 3'
        self.setADC3.put_conv_function = lambda x: f'AAD 3,{x}'
        self.outputFilter3.put_conv_function = lambda x: f'FL {x},3'
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV3.read_function = lambda: self.measure_single_voltage(3)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI3.read_function = lambda: self.measure_single_current(3)
        # function called when putting value to measMode3
        self.measMode3.put_conv_function = lambda x: self.set_MM_value(x, 3)
        # function called when putting value to currComp3
        self.ImeasRange3.put_conv_function = lambda x: f'RI 3,{x}'
        # function called when putting value to voltComp3
        self.VmeasRange3.put_conv_function = lambda x: f'RV 3,{x}'
        # --------------------Channel 4----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp4.put_function = lambda x: self.set_voltCompliance(x, 4)
        self.setI4.put_conv_function = lambda x: self.source_current(x, 4, self.IoutRange4, )
        # set array element of curr compliance to the value entered
        self.currComp4.put_function = lambda x: self.set_currCompliance(x, 4, )
        self.setV4.put_conv_function = lambda x: self.source_voltage(x, 4, self.VoutRange4)
        self.enable4.put_conv_function = lambda x: f'CN 4'
        self.setADC4.put_conv_function = lambda x: f'AAD 4,{x}'
        self.outputFilter4.put_conv_function = lambda x: f'FL {x},4'
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV4.read_function = lambda: self.measure_single_voltage(4)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI4.read_function = lambda: self.measure_single_current(4)
        # function called when putting value to measMode4
        self.measMode4.put_conv_function = lambda x: self.set_MM_value(x, 4)
        # function called when putting value to currComp4
        self.ImeasRange4.put_conv_function = lambda x: f'RI 4,{x}'
        # function called when putting value to voltComp4
        self.VmeasRange4.put_conv_function = lambda x: f'RV 4,{x}'
        # --------------------Channel 5----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp5.put_function = lambda x: self.set_voltCompliance(x, 5)
        self.setI5.put_conv_function = lambda x: self.source_current(x, 5, self.IoutRange5, )
        # set array element of curr compliance to the value entered
        self.currComp5.put_function = lambda x: self.set_currCompliance(x, 5, )
        self.setV5.put_conv_function = lambda x: self.source_voltage(x, 5, self.VoutRange5)
        self.enable5.put_conv_function = lambda x: f'CN 5'
        self.setADC5.put_conv_function = lambda x: f'AAD 5,{x}'
        self.outputFilter5.put_conv_function = lambda x: f'FL {x},5'
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV5.read_function = lambda: self.measure_single_voltage(5)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI5.read_function = lambda: self.measure_single_current(5)
        # function called when putting value to measMode5
        self.measMode5.put_conv_function = lambda x: self.set_MM_value(x, 5)
        # function called when putting value to currComp5
        self.ImeasRange5.put_conv_function = lambda x: f'RI 5,{x}'
        # function called when putting value to voltComp5
        self.VmeasRange5.put_conv_function = lambda x: f'RV 5,{x}'
        # --------------------Channel 6----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp6.put_function = lambda x: self.set_voltCompliance(x, 6)
        self.setI6.put_conv_function = lambda x: self.source_current(x, 6, self.IoutRange6, )
        # set array element of curr compliance to the value entered
        self.currComp6.put_function = lambda x: self.set_currCompliance(x, 6, )
        self.setV6.put_conv_function = lambda x: self.source_voltage(x, 6, self.VoutRange6)
        self.enable6.put_conv_function = lambda x: f'CN 6'
        self.setADC6.put_conv_function = lambda x: f'AAD 6,{x}'
        self.outputFilter6.put_conv_function = lambda x: f'FL {x},6'
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV6.read_function = lambda: self.measure_single_voltage(6)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI6.read_function = lambda: self.measure_single_current(6)
        # function called when putting value to measMode6
        self.measMode6.put_conv_function = lambda x: self.set_MM_value(x, 6)
        # function called when putting value to currComp6
        self.ImeasRange6.put_conv_function = lambda x: f'RI 6,{x}'
        # function called when putting value to voltComp6
        self.VmeasRange6.put_conv_function = lambda x: f'RV 6,{x}'
        # --------------------Channel 7----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp7.put_function = lambda x: self.set_voltCompliance(x, 7)
        self.setI7.put_conv_function = lambda x: self.source_current(x, 7, self.IoutRange7, )
        # set array element of curr compliance to the value entered
        self.currComp7.put_function = lambda x: self.set_currCompliance(x, 7, )
        self.setV7.put_conv_function = lambda x: self.source_voltage(x, 7, self.VoutRange7)
        self.enable7.put_conv_function = lambda x: f'CN 7'
        self.setADC7.put_conv_function = lambda x: f'AAD 7,{x}'
        self.outputFilter7.put_conv_function = lambda x: f'FL {x},7'
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV7.read_function = lambda: self.measure_single_voltage(7)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI7.read_function = lambda: self.measure_single_current(7)
        # function called when putting value to measMode7
        self.measMode7.put_conv_function = lambda x: self.set_MM_value(x, 7)
        # function called when putting value to currComp7
        self.ImeasRange7.put_conv_function = lambda x: f'RI 7,{x}'
        # function called when putting value to voltComp7
        self.VmeasRange7.put_conv_function = lambda x: f'RV 7,{x}'
        # --------------------Channel 8----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp8.put_function = lambda x: self.set_voltCompliance(x, 8)
        self.setI8.put_conv_function = lambda x: self.source_current(x, 8, self.IoutRange8, )
        # set array element of curr compliance to the value entered
        self.currComp8.put_function = lambda x: self.set_currCompliance(x, 8, )
        self.setV8.put_conv_function = lambda x: self.source_voltage(x, 8, self.VoutRange8)
        self.enable8.put_conv_function = lambda x: f'CN 8'
        self.setADC8.put_conv_function = lambda x: f'AAD 8,{x}'
        self.outputFilter8.put_conv_function = lambda x: f'FL {x},8'
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV8.read_function = lambda: self.measure_single_voltage(8)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI8.read_function = lambda: self.measure_single_current(8)
        # function called when putting value to measMode8
        self.measMode8.put_conv_function = lambda x: self.set_MM_value(x, 8)
        # function called when putting value to currComp8
        self.ImeasRange8.put_conv_function = lambda x: f'RI 8,{x}'
        # function called when putting value to voltComp8
        self.VmeasRange8.put_conv_function = lambda x: f'RV 8,{x}'


    def enable_used_channels(self):
        for channel in self.use_channels:
            self.visa_instrument.write(f'CN {channel}')
    def wait_for_connection(self, all_signals=False, timeout=2.0):
        self.wait_conn_sub(all_signals, timeout)

    def wait_conn_sub(self, all_signals=False, timeout=2.0):
        """Wait for signals to connect

        Parameters
        ----------
        all_signals : bool, optional
            Wait for all signals to connect (including lazy ones)
        timeout : float or None
            Overall timeout
        """
        signals = []
        for walk in self.walk_signals(include_lazy=all_signals):
            name = walk.item.attr_name
            use = True
            for i in range(1, 9):
                if i not in self.use_channels and str(i) in name:
                    use = False
                    break
            if use:
                signals.append(walk.item)

        pending_funcs = {
            dev: getattr(dev, '_required_for_connection', {})
            for name, dev in self.walk_subdevices(include_lazy=all_signals)
        }
        pending_funcs[self] = self._required_for_connection

        t0 = ttime.time()
        while timeout is None or (ttime.time() - t0) < timeout:
            connected = all(sig.connected for sig in signals)
            if connected and not any(pending_funcs.values()):
                self.visa_instrument.write('FMT 2,0;RED 1')
                self.enable_used_channels()
                return
            ttime.sleep(min((0.05, timeout / 10.0)))

        def get_name(sig):
            sig_name = f'{self.name}.{sig.dotted_name}'
            return (f'{sig_name} ({sig.pvname})' if hasattr(sig, 'pvname')
                    else sig_name)

        reasons = []
        unconnected = ', '.join(get_name(sig)
                                for sig in signals if not sig.connected)
        if unconnected:
            reasons.append(f'Failed to connect to all signals: {unconnected}')
        if any(pending_funcs.values()):
            pending = ', '.join(description.format(device=dev)
                                for dev, funcs in pending_funcs.items()
                                for obj, description in funcs.items())
            reasons.append(f'Pending operations: {pending}')
        raise TimeoutError('; '.join(reasons))




        
        
    def set_ADC_mode(self, type_res_or_speed, mode):
        if mode==2 or mode == 1:
            plc = self.resADCPLC.get()
            return f'AIT {type_res_or_speed},{mode},{plc}'
        if mode==0:
            return f'AIT {type_res_or_speed},{mode}'

    def set_MM_value(self, val, chnum):
        self.last_MM_channel=chnum
        self.last_MM_value[chnum-1] = val
        self.visa_instrument.write(f'MM {val},{chnum}')
        print(f'from set_MM_val: MM {val},{chnum}')
        return f'MM {val},{chnum}'

    def set_CMM_value(self, val, chnum):
        self.last_CMM_value[chnum - 1] = val
        self.visa_instrument.write(f'CMM {chnum},{val}')
        print(f'write string = CMM {chnum},{val}')
        return f'CMM {chnum},{val}'

    def measure_single_voltage(self, chnum):
        print(f'voltage measurement {chnum=}')
        if self.last_MM_channel != chnum:
            self.set_MM_value(1, chnum)
        elif self.last_MM_value[chnum-1] != 1:
            self.set_MM_value(1, chnum)
        if self.last_CMM_value[chnum-1] != 2:
            self.set_CMM_value(2, chnum)
        return 'XE'

    def measure_single_current(self, chnum):
        print(f'current measurement {chnum=}')
        if self.last_MM_channel != chnum:
            self.set_MM_value(1, chnum)
        if self.last_MM_value[chnum-1] != 1:
            self.set_MM_value(1, chnum)
        if self.last_CMM_value[chnum-1] != 1:
            self.set_CMM_value(1, chnum)
        return 'XE'

    def set_currCompliance(self, value, chan,):
        self.curr_compliance_array[chan-1] = value

    def set_voltCompliance(self, value, chan):
        self.volt_compliance_array[chan-1] = value

    def source_current(self, current, chnum, range_signal,):
        irange = range_signal.get()
        Vcomp = self.volt_compliance_array[chnum-1]
        print(f'DI {chnum},{irange},{current},{Vcomp}')
        return f'DI {chnum},{irange},{current},{Vcomp}'

    def source_voltage(self, voltage, chnum, range_signal,):
        vrange = range_signal.get()
        Icomp = self.curr_compliance_array[chnum-1]
        return f'DV {chnum},{vrange},{voltage},{Icomp}'

#### Driver for E5270B using EPICS ####
class Keysight_E5270B_EPICS(Device):
    setV1 = Cpt(EpicsSignal, 'setV1')
    setI1 = Cpt(EpicsSignal, 'setI1')
    mesI1 = Cpt(TriggerEpicsSignalRO, 'mesI1')
    mesV1 = Cpt(TriggerEpicsSignalRO, 'mesV1')
    enable1 = Cpt(EpicsSignal, 'enable1')
    measMode1 = Cpt(EpicsSignal, 'measMode1', kind='config')
    currComp1 = Cpt(EpicsSignal, 'currComp1', kind='config')
    voltComp1 = Cpt(EpicsSignal, 'voltComp1', kind='config')
    VoutRange1 = Cpt(EpicsSignal, 'VoutRange1', kind='config')
    IoutRange1 = Cpt(EpicsSignal, 'IoutRange1', kind='config')
    VmeasRange1 = Cpt(EpicsSignal, 'VmeasRange1', kind='config')
    ImeasRange1 = Cpt(EpicsSignal, 'ImeasRange1', kind='config')
    setADC1 = Cpt(EpicsSignal, 'setADC1', kind='config')
    outputFilter1 = Cpt(EpicsSignal, 'outputFilter1', kind='config')

    setV2 = Cpt(EpicsSignal, 'setV2')
    setI2 = Cpt(EpicsSignal, 'setI2')
    mesI2 = Cpt(TriggerEpicsSignalRO, 'mesI2')
    mesV2 = Cpt(TriggerEpicsSignalRO, 'mesV2')
    enable2 = Cpt(EpicsSignal, 'enable2')
    measMode2 = Cpt(EpicsSignal, 'measMode2', kind='config')
    currComp2 = Cpt(EpicsSignal, 'currComp2', kind='config')
    voltComp2 = Cpt(EpicsSignal, 'voltComp2', kind='config')
    VoutRange2 = Cpt(EpicsSignal, 'VoutRange2', kind='config')
    IoutRange2 = Cpt(EpicsSignal, 'IoutRange2', kind='config')
    VmeasRange2 = Cpt(EpicsSignal, 'VmeasRange2', kind='config')
    ImeasRange2 = Cpt(EpicsSignal, 'ImeasRange2', kind='config')
    setADC2 = Cpt(EpicsSignal, 'setADC2', kind='config')
    outputFilter2 = Cpt(EpicsSignal, 'outputFilter2', kind='config')

    setV3 = Cpt(EpicsSignal, 'setV3')
    setI3 = Cpt(EpicsSignal, 'setI3')
    mesI3 = Cpt(TriggerEpicsSignalRO, 'mesI3')
    mesV3 = Cpt(TriggerEpicsSignalRO, 'mesV3')
    enable3 = Cpt(EpicsSignal, 'enable3')
    measMode3 = Cpt(EpicsSignal, 'measMode3', kind='config')
    currComp3 = Cpt(EpicsSignal, 'currComp3', kind='config')
    voltComp3 = Cpt(EpicsSignal, 'voltComp3', kind='config')
    VoutRange3 = Cpt(EpicsSignal, 'VoutRange3', kind='config')
    IoutRange3 = Cpt(EpicsSignal, 'IoutRange3', kind='config')
    VmeasRange3 = Cpt(EpicsSignal, 'VmeasRange3', kind='config')
    ImeasRange3 = Cpt(EpicsSignal, 'ImeasRange3', kind='config')
    setADC3 = Cpt(EpicsSignal, 'setADC3', kind='config')
    outputFilter3 = Cpt(EpicsSignal, 'outputFilter3', kind='config')

    setV4 = Cpt(EpicsSignal, 'setV4')
    setI4 = Cpt(EpicsSignal, 'setI4')
    mesI4 = Cpt(TriggerEpicsSignalRO, 'mesI4')
    mesV4 = Cpt(TriggerEpicsSignalRO, 'mesV4')
    enable4 = Cpt(EpicsSignal, 'enable4')
    measMode4 = Cpt(EpicsSignal, 'measMode4', kind='config')
    currComp4 = Cpt(EpicsSignal, 'currComp4', kind='config')
    voltComp4 = Cpt(EpicsSignal, 'voltComp4', kind='config')
    VoutRange4 = Cpt(EpicsSignal, 'VoutRange4', kind='config')
    IoutRange4 = Cpt(EpicsSignal, 'IoutRange4', kind='config')
    VmeasRange4 = Cpt(EpicsSignal, 'VmeasRange4', kind='config')
    ImeasRange4 = Cpt(EpicsSignal, 'ImeasRange4', kind='config')
    setADC4 = Cpt(EpicsSignal, 'setADC4', kind='config')
    outputFilter4 = Cpt(EpicsSignal, 'outputFilter4', kind='config')

    setV5 = Cpt(EpicsSignal, 'setV5')
    setI5 = Cpt(EpicsSignal, 'setI5')
    mesI5 = Cpt(TriggerEpicsSignalRO, 'mesI5')
    mesV5 = Cpt(TriggerEpicsSignalRO, 'mesV5')
    enable5 = Cpt(EpicsSignal, 'enable5')
    measMode5 = Cpt(EpicsSignal, 'measMode5', kind='config')
    currComp5 = Cpt(EpicsSignal, 'currComp5', kind='config')
    voltComp5 = Cpt(EpicsSignal, 'voltComp5', kind='config')
    VoutRange5 = Cpt(EpicsSignal, 'VoutRange5', kind='config')
    IoutRange5 = Cpt(EpicsSignal, 'IoutRange5', kind='config')
    VmeasRange5 = Cpt(EpicsSignal, 'VmeasRange5', kind='config')
    ImeasRange5 = Cpt(EpicsSignal, 'ImeasRange5', kind='config')
    setADC5 = Cpt(EpicsSignal, 'setADC5', kind='config')
    outputFilter5 = Cpt(EpicsSignal, 'outputFilter5', kind='config')

    setV6 = Cpt(EpicsSignal, 'setV6')
    setI6 = Cpt(EpicsSignal, 'setI6')
    mesI6 = Cpt(TriggerEpicsSignalRO, 'mesI6')
    mesV6 = Cpt(TriggerEpicsSignalRO, 'mesV6')
    enable6 = Cpt(EpicsSignal, 'enable6')
    measMode6 = Cpt(EpicsSignal, 'measMode6', kind='config')
    currComp6 = Cpt(EpicsSignal, 'currComp6', kind='config')
    voltComp6 = Cpt(EpicsSignal, 'voltComp6', kind='config')
    VoutRange6 = Cpt(EpicsSignal, 'VoutRange6', kind='config')
    IoutRange6 = Cpt(EpicsSignal, 'IoutRange6', kind='config')
    VmeasRange6 = Cpt(EpicsSignal, 'VmeasRange6', kind='config')
    ImeasRange6 = Cpt(EpicsSignal, 'ImeasRange6', kind='config')
    setADC6 = Cpt(EpicsSignal, 'setADC6', kind='config')
    outputFilter6 = Cpt(EpicsSignal, 'outputFilter6', kind='config')

    setV7 = Cpt(EpicsSignal, 'setV7')
    setI7 = Cpt(EpicsSignal, 'setI7')
    mesI7 = Cpt(TriggerEpicsSignalRO, 'mesI7')
    mesV7 = Cpt(TriggerEpicsSignalRO, 'mesV7')
    enable7 = Cpt(EpicsSignal, 'enable7')
    measMode7 = Cpt(EpicsSignal, 'measMode7', kind='config')
    currComp7 = Cpt(EpicsSignal, 'currComp7', kind='config')
    voltComp7 = Cpt(EpicsSignal, 'voltComp7', kind='config')
    VoutRange7 = Cpt(EpicsSignal, 'VoutRange7', kind='config')
    IoutRange7 = Cpt(EpicsSignal, 'IoutRange7', kind='config')
    VmeasRange7 = Cpt(EpicsSignal, 'VmeasRange7', kind='config')
    ImeasRange7 = Cpt(EpicsSignal, 'ImeasRange7', kind='config')
    setADC7 = Cpt(EpicsSignal, 'setADC7', kind='config')
    outputFilter7 = Cpt(EpicsSignal, 'outputFilter7', kind='config')

    setV8 = Cpt(EpicsSignal, 'setV8')
    setI8 = Cpt(EpicsSignal, 'setI8')
    mesI8 = Cpt(TriggerEpicsSignalRO, 'mesI8')
    mesV8 = Cpt(TriggerEpicsSignalRO, 'mesV8')
    enable8 = Cpt(EpicsSignal, 'enable8')
    measMode8 = Cpt(EpicsSignal, 'measMode8', kind='config')
    currComp8 = Cpt(EpicsSignal, 'currComp8', kind='config')
    voltComp8 = Cpt(EpicsSignal, 'voltComp8', kind='config')
    VoutRange8 = Cpt(EpicsSignal, 'VoutRange8', kind='config')
    IoutRange8 = Cpt(EpicsSignal, 'IoutRange8', kind='config')
    VmeasRange8 = Cpt(EpicsSignal, 'VmeasRange8', kind='config')
    ImeasRange8 = Cpt(EpicsSignal, 'ImeasRange8', kind='config')
    setADC8 = Cpt(EpicsSignal, 'setADC8', kind='config')
    outputFilter8 = Cpt(EpicsSignal, 'outputFilter8', kind='config')

    speedADCPLC = Cpt(EpicsSignal, 'speedADCPLC', kind='config')
    speedADCmode = Cpt(EpicsSignal, 'speedADCmode', kind='config')
    resADCPLC = Cpt(EpicsSignal, 'resADCPLC', kind='config')
    resADCmode = Cpt(EpicsSignal, 'resADCmode', kind='config')
    idn = Cpt(EpicsSignalRO, 'idn', kind='config')
    err = Cpt(TriggerEpicsSignalRO, 'err', no_mdel=True)

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, use_channels=(), **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        self.use_channels = use_channels
        if use_channels:
            comps = list(self.component_names)
            for comp in self.component_names:
                for i in range(1, 9):
                    if i not in self.use_channels and str(i) in comp:
                        comps.remove(comp)
                        break
            self.component_names = tuple(comps)

    def wait_for_connection(self, all_signals=False, timeout=2.0):
        self.wait_conn_sub(all_signals, timeout)
        self.measMode1.put(1)
        self.measMode2.put(1)
        self.measMode3.put(1)
        self.measMode4.put(1)
        self.measMode5.put(1)
        self.measMode6.put(1)
        self.measMode7.put(1)
        self.measMode8.put(1)

    def wait_conn_sub(self, all_signals=False, timeout=2.0):
        """Wait for signals to connect

        Parameters
        ----------
        all_signals : bool, optional
            Wait for all signals to connect (including lazy ones)
        timeout : float or None
            Overall timeout
        """
        signals = []
        for walk in self.walk_signals(include_lazy=all_signals):
            name = walk.item.attr_name
            use = True
            for i in range(1, 9):
                if i not in self.use_channels and str(i) in name:
                    use = False
                    break
            if use:
                signals.append(walk.item)

        pending_funcs = {
            dev: getattr(dev, '_required_for_connection', {})
            for name, dev in self.walk_subdevices(include_lazy=all_signals)
        }
        pending_funcs[self] = self._required_for_connection

        t0 = ttime.time()
        while timeout is None or (ttime.time() - t0) < timeout:
            connected = all(sig.connected for sig in signals)
            if connected and not any(pending_funcs.values()):
                return
            ttime.sleep(min((0.05, timeout / 10.0)))

        def get_name(sig):
            sig_name = f'{self.name}.{sig.dotted_name}'
            return (f'{sig_name} ({sig.pvname})' if hasattr(sig, 'pvname')
                    else sig_name)

        reasons = []
        unconnected = ', '.join(get_name(sig)
                                for sig in signals if not sig.connected)
        if unconnected:
            reasons.append(f'Failed to connect to all signals: {unconnected}')
        if any(pending_funcs.values()):
            pending = ', '.join(description.format(device=dev)
                                for dev, funcs in pending_funcs.items()
                                for obj, description in funcs.items())
            reasons.append(f'Pending operations: {pending}')
        raise TimeoutError('; '.join(reasons))


if __name__ == '__main__':
    e5270b = Keysight_E5270B(prefix='Default:', name='e5270b', use_channels=[1,8])
    # comps = e5270b.walk_components()
    # for comp in comps:
    #     print(comp)