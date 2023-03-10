from CAMELS.utility import variables_handling

manual_controls = {}

def get_instrument_controls():
    controls = {}
    for name, instr in sorted(variables_handling.devices.items(),
                              key=lambda x: x[0].lower()):
        adds = instr.get_controls()
        controls.update(adds)
    return controls

def get_control_by_type_name(name):
    if name in manual_controls:
        return manual_controls[name]
    instr_controls = get_instrument_controls()
    if name in instr_controls:
        return instr_controls[name]
    raise Exception(f'Manual Control of type {name} is not defined!')
