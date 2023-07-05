from ophyd import Device, Kind
import bluesky.plan_stubs as bps

def trigger_and_read_devices(devices, name='primary'):
    """A wrapper for the plan stup `trigger_and_read` that implements
    trigger/read for a device with several components by simply splitting
    up the device and using a list of its components.

    Parameters
    ----------
    devices : list[ophyd.Device]
        List of the devices that should be triggered and read
    name : str
        (Default value = 'primary')
        Name of the stream where to save the data
    """
    split_devices = []
    for dev in devices:
        if isinstance(dev, Device):
            dev.read()
            for _, component in dev._get_components_of_kind(Kind.normal):
                split_devices.append(component)
        else:
            split_devices.append(dev)
    return bps.trigger_and_read(split_devices, name)