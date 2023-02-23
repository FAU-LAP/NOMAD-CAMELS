import time

from ophyd import Signal, SignalRO, Device
import pyvisa
import re

# number_pattern =

rm = pyvisa.ResourceManager()
open_resources = {}

def list_resources():
    return rm.list_resources()

def close_resources():
    for res in open_resources:
        open_resources[res].close()
    open_resources.clear()

class VISA_Signal_Write(Signal):
    def __init__(self,  name, value=0., timestamp=None, parent=None,
                 labels=None, kind='hinted', tolerance=None, rtolerance=None,
                 metadata=None, cl=None, attr_name='', write_termination='\n',
                 baud_rate=9600, resource_name='', additional_put_text='',
                 put_conv_function=None, put_format_string=''):
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent,
                         labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance,
                         metadata=metadata, cl=cl, attr_name=attr_name)
        self.visa_instrument = None
        self.resource_name = resource_name
        # if resource_name:
        #     if resource_name in open_resources:
        #         self.visa_instrument = open_resources[resource_name]
        #     else:
        #         self.visa_instrument = rm.open_resource(resource_name)
        #         open_resources[resource_name] = self.visa_instrument
        #     self.visa_instrument.write_termination = write_termination
        #     self.visa_instrument.baud_rate = baud_rate
        self.put_conv_function = put_conv_function or None
        self.additional_put_text = additional_put_text
        self.put_format_string = put_format_string

    def change_instrument(self, resource_name):
        if resource_name:
            if resource_name in open_resources:
                self.visa_instrument = open_resources[resource_name]
            else:
                self.visa_instrument = rm.open_resource(resource_name)
                open_resources[resource_name] = self.visa_instrument

    def put(self, value, *, timestamp=None, force=False, metadata=None,
            **kwargs):
        if self.put_conv_function:
            write_text = self.put_conv_function(value)
        elif self.put_format_string:
            write_text = self.put_format_string % value
        else:
            write_text = f'{self.additional_put_text}{value}'
        self.visa_instrument.write(write_text)
        super().put(value, timestamp=timestamp, force=force, metadata=metadata, **kwargs)

    def describe(self):
        info = super().describe()
        info[self.name]['source'] = 'VISA'
        info[self.name].update(self.metadata)
        return info



class VISA_Signal_Read(SignalRO):
    def __init__(self,  name, value=0., timestamp=None, parent=None, labels=None,
                 kind='hinted', tolerance=None, rtolerance=None, metadata=None,
                 cl=None, attr_name='', read_termination='\n', write_termination='\n',
                 baud_rate=9600, resource_name='', query_text='', match_return=False,
                 read_function=None, process_read_function=None):
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent, labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance, metadata=metadata, cl=cl, attr_name=attr_name)
        self.visa_instrument = None
        self.resource_name = resource_name
        self.match_return = match_return
        # if resource_name:
        #     if resource_name in open_resources:
        #         self.visa_instrument = open_resources[resource_name]
        #     else:
        #         self.visa_instrument = rm.open_resource(resource_name)
        #         open_resources[resource_name] = self.visa_instrument
        #     self.visa_instrument.read_termination = read_termination
        #     self.visa_instrument.write_termination = write_termination
        #     self.visa_instrument.baud_rate = baud_rate
        self.read_function = read_function or None
        self.process_read_function = process_read_function or None
        self.query_text = query_text
        self.reading = False

    def get(self):
        while self.visa_instrument.currently_reading:
            time.sleep(0.1)
        self.visa_instrument.currently_reading = True
        if self.read_function:
            val = self.visa_instrument.query(self.read_function())
        else:
            val = self.visa_instrument.query(self.query_text)
        self.visa_instrument.currently_reading = False
        if self.process_read_function:
            val = self.process_read_function(val)
        else:
            try:
                val = float(val)
            except:
                if self.match_return:
                    try:
                        match = re.search(r".*?([-+eE\d.]+).*", val)
                        gr = match.group(1)
                        val = float(gr)
                    except:
                        pass
        self._readback = val
        return super().get()

    def describe(self):
        info = super().describe()
        info[self.name]['source'] = 'VISA'
        info[self.name].update(self.metadata)
        return info



class VISA_Device(Device):
    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 read_termination='\r\n', write_termination='\r\n',
                 baud_rate=9600, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent, **kwargs)
        self.visa_instrument = None
        if resource_name:
            if resource_name in open_resources:
                self.visa_instrument = open_resources[resource_name]
            else:
                self.visa_instrument = rm.open_resource(resource_name)
                open_resources[resource_name] = self.visa_instrument
            self.visa_instrument.write_termination = write_termination
            self.visa_instrument.read_termination = read_termination
            self.visa_instrument.baud_rate = baud_rate
            self.visa_instrument.currently_reading = False

        for comp in self.walk_signals():
            it = comp.item
            it.visa_instrument = self.visa_instrument



if __name__ == '__main__':
    print(list_resources())
    tester = 'USB0::0x0957::0x8E18::MY51140626::INSTR'
    # testsig = VISA_Signal_Write('testsig', write_termination='\r\n', resource_name=tester)
    testsigR = VISA_Signal_Read('testsigR', read_termination='\r\n', write_termination='\r\n', resource_name=tester, query_text='MEAS:VOLT:DC?')
    print(testsigR.get())