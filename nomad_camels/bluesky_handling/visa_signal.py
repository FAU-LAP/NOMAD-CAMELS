import time

from ophyd import Signal, SignalRO, Device
import pyvisa
import re

rm = pyvisa.ResourceManager()
open_resources = {}

def list_resources():
    """Gives the results of `ResourceManager.list_resources`."""
    return rm.list_resources()

def close_resources():
    """Goes throug all the opened resources and closes them."""
    for res in open_resources:
        open_resources[res].close()
    open_resources.clear()

class VISA_Signal(Signal):
    """ """
    def __init__(self,  name, value=0., timestamp=None, parent=None,
                 labels=None, kind='hinted', tolerance=None, rtolerance=None,
                 metadata=None, cl=None, attr_name='',
                 write=None, parse=None, parse_return_type=None,
                 retry_on_error=0):
        """
        Parameters
        ----------
        write : str or function with str as a return value
            (Default = None)
            Determines what is written to the instrument. As a string it should have '{value}' in it (could include further formatting). The given value will be put into the string there, e.g. if `write='VOLT{value:03d}'`, the value will be given as an integer of three digits with leading zeroes.
            If `write` is a function, it should return a string. Everytime a value is set, the function will be executed and the resulting string will be sent to the instrument.
            If it is None, the value will be simply converted to a string.
        
        parse : str or function
            (Default value = None)
            This gives how the returned string from the instrument is being parsed.
            If str, it should be a regular expression. The first result from the regex will become the new value.
            If function, it will take the returned string and the new value will be the value returned from this function.
            If `parse` is not None, a query to the instrument will be executed, instead of a simple write. If it is used to just clear the buffer, it could be an empty string.
        
        parse_return_type : str, class or None
            (Default = None)
            If `parse` is a string or None, the returned string (either from the instrument or from `parse`) will be converted to the given class.
            Supported strings for class names are: 'str', 'float', 'int', 'bool'.
            If `parse_return_type` and `parse` is not None, the value will become the readback for this Signal. Otherwise the value given with put becomes the readback.

        retry_on_error : int
            (Default = 0)
            The number of times the reading / setting should be tried again if
            there is an error (e.g. a VISA-IO-error).
        """
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent,
                         labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance,
                         metadata=metadata, cl=cl, attr_name=attr_name)
        self.visa_instrument = None
        self.write = write
        self.parse = parse
        self.retry_on_error = retry_on_error
        if parse_return_type == 'str':
            self.parse_return_type = str
        elif parse_return_type == 'float':
            self.parse_return_type = float
        elif parse_return_type == 'int':
            self.parse_return_type = int
        elif parse_return_type == 'bool':
            self.parse_return_type = bool
        else:
            self.parse_return_type = parse_return_type

    def change_instrument(self, resource_name):
        """
        Changes the visa_instrument to the one with the given `resource_name`.

        Parameters
        ----------
        resource_name : str
            Name of the new instrument to be used.
        """
        if resource_name:
            if resource_name in open_resources:
                self.visa_instrument = open_resources[resource_name]
            else:
                self.visa_instrument = rm.open_resource(resource_name)
                open_resources[resource_name] = self.visa_instrument

    def put(self, value, *, timestamp=None, force=False, metadata=None,
            **kwargs):
        """
        Overwrites `ophyd.Signal.put`. The value is converted to a string, using
        `self.write`. If `self.parse` is not None, a query instead of a simple
        write is being performed, in that case, the value given to super().put
        is the returned value from the query.
        """
        if not self.write:
            write_text = str(value)
        elif isinstance(self.write, str):
            write_text = self.write.format(value=value)
        else:
            write_text = self.write(value)
        if self.parse is not None:
            val = retry_query_or_write(write_text, self.visa_instrument,
                                       self.retry_on_error)
            if self.parse:
                try:
                    if isinstance(self.parse, str):
                        val = re.match(self.parse, val).group(1)
                    else:
                        val = self.parse(val)
                except Exception as e:
                    print(e)
            if self.parse_return_type:
                try:
                    value = self.parse_return_type(val)
                except:
                    value = val
        else:
            retry_query_or_write(write_text, self.visa_instrument,
                                 self.retry_on_error, True)
        super().put(value, timestamp=timestamp, force=force, metadata=metadata, **kwargs)

    def describe(self):
        """Adding "VISA" as the source for the description."""
        info = super().describe()
        info[self.name]['source'] = 'VISA'
        # info[self.name].update(self.metadata)
        return info



def retry_query_or_write(write_text, visa_instrument, retries, just_write=False):
    excs = []
    while visa_instrument.currently_reading:
        time.sleep(0.1)
    if not just_write:
        visa_instrument.currently_reading = True
    for i in range(retries + 1):
        try:
            if just_write:
                visa_instrument.write(write_text)
                return
            else:
                val = visa_instrument.query(write_text)
                visa_instrument.currently_reading = False
                return val
        except Exception as e:
            if i == retries:
                print(excs)
                raise Exception(e)
            excs.append(e)


class VISA_Signal_RO(SignalRO):
    """ """
    def __init__(self,  name, value=0., timestamp=None, parent=None, labels=None,
                 kind='hinted', tolerance=None, rtolerance=None, metadata=None,
                 cl=None, attr_name='',
                 query='', parse=None, parse_return_type='float',
                 retry_on_error=0):
        """
        Parameters
        ----------
        query : str or function with str as a return value
            Determines what is written to the instrument. If it is a string, that string will be sent to the instrument. If it is a function, its return value will be sent to the instrument.

        parse : str or function
            (Default value = None)
            This gives how the returned string from the instrument is being parsed.
            If str, it should be a regular expression. The first result from the regex will become the new value.
            If function, it will take the returned string and the new value will be the value returned from this function.
            If `parse` is not None, a query to the instrument will be executed, instead of a simple write. If it is used to just clear the buffer, it could be an empty string.

        parse_return_type : str, class
            (Default = 'float')
            If `parse` is a string or None, the returned string (either from the instrument or from `parse`) will be converted to the given class.
            Supported strings for class names are: 'str', 'float', 'int', 'bool'.

        retry_on_error : int
            (Default = 0)
            The number of times the reading / setting should be tried again if
            there is an error (e.g. a VISA-IO-error).
        """
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent, labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance, metadata=metadata, cl=cl, attr_name=attr_name)
        self.visa_instrument = None
        self.query = query
        self.parse = parse
        self.retry_on_error = retry_on_error
        if parse_return_type == 'str':
            self.parse_return_type = str
        elif parse_return_type == 'float':
            self.parse_return_type = float
        elif parse_return_type == 'int':
            self.parse_return_type = int
        elif parse_return_type == 'bool':
            self.parse_return_type = bool
        else:
            self.parse_return_type = parse_return_type

    def get(self):
        """
        Overwrites `ophyd.SignalRO.get`, performing a query to the instrument.
        The returned string is parsed regarding `self.parse` and converted to
        the datatype specified by `self.parse_return_type`.
        """
        if isinstance(self.query, str):
            query = self.query
        else:
            query = self.query()
        val = retry_query_or_write(query, self.visa_instrument,
                                   self.retry_on_error)
        if self.parse is not None:
            try:
                if isinstance(self.parse, str):
                    val = re.match(self.parse, val).group(1)
                else:
                    val = self.parse(val)
            except Exception as e:
                print(e)
        if self.parse_return_type:
            try:
                val = self.parse_return_type(val)
            except:
                val = val
        self._readback = val
        return super().get()

    def describe(self):
        """Adding "VISA" as the source for the description."""
        info = super().describe()
        info[self.name]['source'] = 'VISA'
        # info[self.name].update(self.metadata)
        return info



class VISA_Device(Device):
    """
    Subclasses ophyd's `Device` class. Automatically opens the specified VISA
    resource.

    Parameters
    ----------
    resource_name : str
        The name of the VISA-resource.
    read_termination : str
        (Default = '\\r\\n')
        The line termination for reading from the instrument.
    write_termination : str
        (Default = '\\r\\n')
        The line termination for writing to the instrument.
    baud_rate : int
        (Default = 9600)
        The communication baud rate.
    retry_on_error : int
        (Default = 0)
        The number of times the reading / setting should be tried again if
        there is an error (e.g. a VISA-IO-error). It is handed to all components
        that do not have a retry_on_error already defined.
    """
    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 read_termination='\r\n', write_termination='\r\n',
                 baud_rate=9600, timeout=2000, retry_on_error=0, **kwargs):
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
            self.visa_instrument.timeout = timeout

        for comp in self.walk_signals():
            it = comp.item
            it.visa_instrument = self.visa_instrument
            if hasattr(it, 'retry_on_error') and not it.retry_on_error:
                it.retry_on_error = retry_on_error

