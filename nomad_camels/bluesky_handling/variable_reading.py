from ophyd import SignalRO
import numpy as np

class Variable_Signal(SignalRO):
    def __init__(self,  name, value=None, timestamp=None, parent=None,
                 labels=None, kind='normal', tolerance=None, rtolerance=None,
                 metadata=None, cl=None, attr_name='', variables_dict=None):
        super().__init__(name=name, value=value, timestamp=timestamp, parent=parent,
                         labels=labels, kind=kind, tolerance=tolerance, rtolerance=rtolerance,
                         metadata=metadata, cl=cl, attr_name=attr_name)
        self.variables_dict = variables_dict or {}

    def describe(self):
        info = super().describe()
        info[self.name]['source'] = 'local_NOMAD_CAMELS_variables'
        info[self.name]['variables'] = list(sorted(self.variables_dict.keys()))
        return info

    def get(self):
        data = []
        for key in sorted(self.variables_dict.keys()):
            data.append(self.variables_dict[key])
        self._readback = data
        return super().get()
