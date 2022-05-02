import numpy as np
from utility import variables_handling

class Measurement_Channel:
    def __init__(self, name='', unit='', output=False, min_val=-np.inf, max_val=np.inf, last_val=0, device=None):
        self.name = name
        self.unit = unit
        self.output = output
        self.min_val = min_val
        self.max_val = max_val
        self.last_val = last_val
        self.device = device

    def get_bounded_val(self, val):
        if val > self.max_val:
            return self.max_val
        elif val < self.min_val:
            return self.min_val
        return val

    def get_pv_name(self):
        name = f'{variables_handling.dev_preset}:{self.device}:{self.name.split(".")[-1]}'
        return name


def from_pv_name(pv_name):
    pass
