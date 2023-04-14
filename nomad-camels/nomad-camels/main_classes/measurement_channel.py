from nomad-camels.utility import variables_handling

class Measurement_Channel:
    """Class that represents one single channel. Most important
    attributes are the name, and the device."""
    def __init__(self, name='', output=False, device=None):
        self.name = name
        self.output = output
        self.device = device

    def get_bluesky_name(self):
        return f'{self.device}.{self.name.split(".")[-1]}'

    def get_pv_name(self):
        """Returns the name of the corresponding EPICS PV."""
        name = f'{variables_handling.preset}:{self.device}:{self.name.split(".")[-1]}'
        return name


def from_pv_name(pv_name):
    """Returns the corresponding Channel-name of an EPICS PV."""
    split_name = pv_name.split(':')
    return f'{split_name[1]}_{split_name[2]}'
