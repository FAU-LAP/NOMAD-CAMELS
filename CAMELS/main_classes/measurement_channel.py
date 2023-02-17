import numpy as np
from utility import variables_handling

class Measurement_Channel:
    """Class that represents one single channel. Most important
    attributes are the name, and the device."""
    def __init__(self, name='', unit='', output=False, min_val=-np.inf,
                 max_val=np.inf, last_val=0, device=None, inputType=None):
        self.name = name
        self.unit = unit
        self.output = output
        self.min_val = min_val
        self.max_val = max_val
        self.last_val = last_val
        self.device = device
        self.inputType = inputType

    def get_bounded_val(self, val):  # not used
        if val > self.max_val:
            return self.max_val
        elif val < self.min_val:
            return self.min_val
        return val

    def get_bluesky_name(self):
        return f'{self.device}.{self.name.split(".")[-1]}'

    def get_pv_name(self):
        """Returns the name of the corresponding EPICS PV."""
        name = f'{variables_handling.preset}:{self.device}:{self.name.split(".")[-1]}'
        return name

    def formatInput(self, value):  # not used
        if self.inputType == 'int':
            return int(value)
        return value


def from_pv_name(pv_name):
    """Returns the corresponding Channel-name of an EPICS PV."""
    split_name = pv_name.split(':')
    return f'{split_name[1]}_{split_name[2]}'
