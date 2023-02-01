import pyvisa
rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('GPIB12::12::INSTR')
print(inst.query("U0X"))