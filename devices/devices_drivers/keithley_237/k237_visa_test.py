import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('QtAgg')
import numpy as np
import pyvisa
rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('GPIB12::12::INSTR')
inst.timeout = 10000
inst.write('J0X')
inst.write("F0,1X")
inst.write('B0,2,0X')
inst.write('L2E-3,8X')
inst.write('G5,2,1X')
inst.write("Q1,1,10,0.01,2,0X")
inst.write('N1X')
inst.write('P0X')
inst.write('R1X')
inst.write('H0X')
volts = []
curs = []
for i in range(900):
    v,i= inst.read().split(',')
    volts.append(float(v))
    curs.append(float(i))
volts = np.array(volts)
curs = np.array(curs)
plt.plot(np.array(volts),np.array(curs))
plt.show()
inst.write('U1X')

print(inst.read())