from ophyd import SignalRO
import numpy as np
from collections import namedtuple


class Variable_Signal(SignalRO):
    def __init__(
        self,
        name,
        value=None,
        timestamp=None,
        parent=None,
        labels=None,
        kind="normal",
        tolerance=None,
        rtolerance=None,
        metadata=None,
        cl=None,
        attr_name="",
        variables_dict=None,
    ):
        super().__init__(
            name=name,
            value=value,
            timestamp=timestamp,
            parent=parent,
            labels=labels,
            kind=kind,
            tolerance=tolerance,
            rtolerance=rtolerance,
            metadata=metadata,
            cl=cl,
            attr_name=attr_name,
        )
        self.variables_dict = variables_dict or {}
        self.vars = list(sorted(self.variables_dict.keys()))

    def describe(self):
        info = super().describe()
        info[self.name]["source"] = "local_NOMAD_CAMELS_variables"
        # self.vars = list(sorted(self.variables_dict.keys()))
        info[self.name]["variables"] = self.vars
        return info

    def get(self):
        # data = []
        # for key in sorted(self.variables_dict.keys()):
        #     if key not in self.vars:
        #         continue
        #     data.append(self.variables_dict[key])
        # self._readback = np.asarray(data)
        data = {}
        for key in sorted(self.variables_dict.keys()):
            if key not in self.vars:
                continue
            data[key] = self.variables_dict[key]
        dev_tuple = namedtuple(self.name, data.keys())
        self._readback = dev_tuple(**data)
        return super().get()
