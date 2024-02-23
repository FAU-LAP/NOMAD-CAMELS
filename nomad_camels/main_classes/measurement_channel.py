from nomad_camels.utility import variables_handling


class Measurement_Channel:
    """Class that represents one single channel. Most important
    attributes are the name, and the device.

    Parameters
    ----------

    Returns
    -------

    """

    def __init__(self, name="", output=False, device=None, metadata=None):
        self.name = name
        self.output = output
        self.device = device
        self.metadata = metadata or {}

    def get_bluesky_name(self):
        """ """
        return f'{self.device}.{self.name.split(".")[-1]}'

    def get_pv_name(self):
        """Returns the name of the corresponding EPICS PV."""
        name = f'{variables_handling.preset}:{self.device}:{self.name.split(".")[-1]}'
        return name

    def get_meta_str(self):
        meta_str = ""
        for i, (k, v) in enumerate(self.metadata.items()):
            if i > 0:
                meta_str += "\n"
            meta_str += f"{k}: {v}"
        return meta_str


def from_pv_name(pv_name):
    """Returns the corresponding Channel-name of an EPICS PV.

    Parameters
    ----------
    pv_name :


    Returns
    -------

    """
    split_name = pv_name.split(":")
    return f"{split_name[1]}_{split_name[2]}"
