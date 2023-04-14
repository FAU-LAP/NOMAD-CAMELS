from ophyd import Signal, SignalRO


class Custom_Function_Signal(Signal):
    def __init__(self,  name, value=0., timestamp=None, parent=None, labels=None, kind='hinted', tolerance=None, rtolerance=None, metadata=None, cl=None, attr_name='', put_function=None, read_function=None, trigger_function=None):
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent, labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance, metadata=metadata, cl=cl, attr_name=attr_name)
        self.put_function = put_function
        self.read_function = read_function
        self.trigger_function = trigger_function
        self.add_metadata = metadata or {}

    def put(self, value, *, timestamp=None, force=False, metadata=None,
            **kwargs):
        if self.put_function:
            self.put_function(value)
        super().put(value, timestamp=timestamp, force=force, metadata=metadata, **kwargs)

    def get(self):
        if self.read_function:
            self._readback = self.read_function()
        return super().get()

    def trigger(self):
        if self.trigger_function:
            self.trigger_function()
        return super().trigger()

    def describe(self):
        info = super().describe()
        info[self.name]['source'] = 'Custom Function'
        info[self.name].update(self.add_metadata)
        return info



class Custom_Function_SignalRO(SignalRO):
    def __init__(self,  name, value=0., timestamp=None, parent=None, labels=None, kind='hinted', tolerance=None, rtolerance=None, metadata=None, cl=None, attr_name='', read_function=None, trigger_function=None):
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent, labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance, metadata=metadata, cl=cl, attr_name=attr_name)
        self.read_function = read_function
        self.trigger_function = trigger_function
        self.add_metadata = metadata or {}

    def get(self):
        if self.read_function:
            self._readback = self.read_function()
        return super().get()

    def trigger(self):
        if self.trigger_function:
            self.trigger_function()
        return super().trigger()

    def describe(self):
        info = super().describe()
        info[self.name]['source'] = 'Custom Function'
        info[self.name].update(self.add_metadata)
        return info
