from CAMELS.utility import variables_handling

manual_controls = {}

def get_instrument_controls():
    controls = {}
    for name, instr in sorted(variables_handling.devices.items(),
                              key=lambda x: x[0].lower()):
        adds = instr.get_controls()
        controls.update(adds)
    return controls
