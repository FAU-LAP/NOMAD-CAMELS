from ophyd import Device
from ophyd import Component as Cpt

from bluesky_handling.visa_signal import VISA_Signal_Read, VISA_Signal_Write


class Keysight_B2912(Device):
    mesV1 = Cpt(VISA_Signal_Read, 'mesV1', query_text='MEAS:VOLT? (@1)')
    mesI1 = Cpt(VISA_Signal_Read, 'mesI1', query_text='MEAS:CURR? (@1)')
    mesV2 = Cpt(VISA_Signal_Read, 'mesV2', query_text='MEAS:VOLT? (@2)')
    mesI2 = Cpt(VISA_Signal_Read, 'mesI2', query_text='MEAS:CURR? (@2)')
    setV1 = Cpt(VISA_Signal_Write, 'setV1', additional_put_text='SOUR1:VOLT ')
    setI1 = Cpt(VISA_Signal_Write, 'setI1', additional_put_text='SOUR1:CURR ')
    setV2 = Cpt(VISA_Signal_Write, 'setV2', additional_put_text='SOUR2:VOLT ')
    setI2 = Cpt(VISA_Signal_Write, 'setI2', additional_put_text='SOUR2:CURR ')
    idn = Cpt(VISA_Signal_Read, 'idn', query_text='*IDN?', kind='config')
