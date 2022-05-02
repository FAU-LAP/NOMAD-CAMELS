from ophyd import Signal

from epics import caput, caget


class EpicsFieldSignal(Signal):
    def __init__(self,  read_pv_name, name, value=0., timestamp=None, parent=None, labels=None, kind='hinted', tolerance=None, rtolerance=None, metadata=None, cl=None, attr_name='', conversion_function=None, set_conversion_function=None):
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent, labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance, metadata=metadata, cl=cl, attr_name=attr_name)
        self.read_pv_name = read_pv_name
        if conversion_function is None:
            conversion_function = lambda x: x
        self.conversion_function = conversion_function
        if set_conversion_function is None:
            set_conversion_function = lambda x: x
        self.set_conversion_function = set_conversion_function

    def get(self):
        if self.read_pv_name is not None:
            print(self.read_pv_name)
            self._readback = self.conversion_function(caget(self.read_pv_name))
        return super().get()

    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        val = self.set_conversion_function(value)
        if self.read_pv_name is not None:
            caput(self.read_pv_name, val, wait=True)
        super().put(val, timestamp=timestamp, force=force, metadata=metadata, **kwargs)

class EpicsFieldSignalRO(EpicsFieldSignal):
    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        raise Exception('EpicsFieldSignalRO does not support putting a value!')