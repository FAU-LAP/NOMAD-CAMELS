from nomad_camels.frontpanels import instrument_installer
from nomad_camels.utility import variables_handling


def ensure_demo_in_devices():
    """Ensure that only the demo_instrument is loaded in the devices dictionary."""
    instr, packs = instrument_installer.getInstalledDevices(True, True)
    if "demo_instrument" not in instr:
        instrument_installer.install_instrument("demo_instrument")
        instr, packs = instrument_installer.getInstalledDevices(True, True)
        assert "demo_instrument" in instr

    # Clear all devices and keep only demo_instrument
    if "demo_instrument" in variables_handling.devices:
        demo_inst = variables_handling.devices["demo_instrument"]
        variables_handling.devices.clear()
        variables_handling.devices["demo_instrument"] = demo_inst
    else:
        variables_handling.devices.clear()
        inst = packs["demo_instrument"].subclass()
        variables_handling.devices["demo_instrument"] = inst

    assert "demo_instrument" in variables_handling.devices
    assert (
        len(variables_handling.devices) == 1
    ), "Only demo_instrument should be present"

    # Clear and repopulate channels
    variables_handling.channels.clear()
    for dev in variables_handling.devices.values():
        variables_handling.channels.update(dev.get_channels())
