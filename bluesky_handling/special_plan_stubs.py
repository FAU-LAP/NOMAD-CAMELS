from ophyd import Device, Kind
import bluesky.plan_stubs as bps

def trigger_and_read_devices(devices, name='primary'):
    split_devices = []
    for dev in devices:
        if isinstance(dev, Device):
            dev.read()
            for _, component in dev._get_components_of_kind(Kind.normal):
                split_devices.append(component)
        else:
            split_devices.append(dev)
    return bps.trigger_and_read(split_devices, name)