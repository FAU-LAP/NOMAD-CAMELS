"""This module provides the functionalities needed for CAMELS to produce a
running python script for its protocols.

The overview of the protocol-file looks like this:\n
- import sys
- add path_to_camels, path_to_camels/nomad_camels, path to instruments to path
- `standard_string`
- `variable_string`
- `device_import_string`
- plot-string
- outer protocol string (things like plots from single steps)
- plan-string (including the inner plan, w/o start/stop and the outer)
- add-main-string (protocol or step specific things that should be done in the main function)
- `standard_run_string`
- further metadata (user / sample, file)
- `standard_start_string`
- set up databroker and progress bar
- `devices_string`
- `standard_start_string2`
- `standard_save_string`
- `final_string`
- `standard_start_string3`

giving shortly:\n
- imports/variables...
- def protocol_plan_inner
- def protocol_plan
- def create_plots
- def steps_add_main (plots of steps, etc.)
- def uid_collector
- def run_protocol_main
- def main
- if __name__ == "__main__"

With the call chain as follows:\n
- if --> main
- main --> create_plots, steps_add_main, run_protocol_main
- run_protocol_main --> uid_collector, protocol_plan
- protocol_plan --> protocol_plan_inner
"""

import os.path
import copy

import pathlib

from nomad_camels.utility import variables_handling, load_save_functions

from nomad_camels.bluesky_handling.builder_helper_functions import plot_creator
from nomad_camels.utility import device_handling


# The default string in the beginning of the protocol including imports etc.
standard_string = "import numpy as np\n"
standard_string += "import importlib\n"
standard_string += "import bluesky\n"
standard_string += "import ophyd\n"
standard_string += "from bluesky import RunEngine\n"
standard_string += "from bluesky.callbacks.best_effort import BestEffortCallback\n"
standard_string += "import bluesky.plan_stubs as bps\n"
standard_string += "import databroker\n"
standard_string += "from PySide6.QtWidgets import QApplication, QMessageBox\n"
standard_string += "from PySide6.QtCore import QCoreApplication, QThread\n"
standard_string += "import datetime\n"
standard_string += (
    "from nomad_camels.main_classes import plot_widget, list_plot, plot_2D\n"
)
standard_string += "from nomad_camels.utility.databroker_export import broker_to_hdf5, broker_to_dict, broker_to_NX\n"
standard_string += "from nomad_camels.utility import theme_changing\n"
standard_string += (
    "from nomad_camels.bluesky_handling.evaluation_helper import Evaluator\n"
)
standard_string += (
    "from nomad_camels.bluesky_handling import helper_functions, variable_reading\n"
)
standard_string += "darkmode = False\n"
standard_string += 'theme = "default"\n'
standard_string += 'protocol_step_information = {"protocol_step_counter": 0, "total_protocol_steps": 0, "protocol_stepper_signal": None}\n'


# this string is used for collection of uids to later access the data
standard_run_string = "uids = []\n"
standard_run_string += "def uid_collector(name, doc):\n"
standard_run_string += '\tuids.append(doc["uid"])\n\n\n'
standard_run_string += 'def run_protocol_main(RE, dark=False, used_theme="default", catalog=None, devices=None, md=None):\n'
standard_run_string += "\tdevs = devices or {}\n"
standard_run_string += "\tmd = md or {}\n"
standard_run_string += "\tglobal darkmode, theme, protocol_step_information\n"
standard_run_string += "\tdarkmode, theme = dark, used_theme\n"

# this is the string with the main function of the protocol, starting everything
# and also the if branch, whether it is the main script to execute everything
# without importing
standard_start_string = "\n\n\ndef main():\n"
standard_start_string += "\tRE = RunEngine()\n"
standard_start_string += "\tbec = BestEffortCallback()\n"
standard_start_string += "\tRE.subscribe(bec)\n"
standard_start_string2 = "\t\tplot_etc = create_plots(RE)\n"
standard_start_string2 += "\t\tadditional_step_data = steps_add_main(RE, devs)\n"
standard_start_string2 += (
    "\t\trun_protocol_main(RE=RE, catalog=catalog, devices=devs, md=md)\n"
)
standard_start_string3 = '\n\n\nif __name__ == "__main__":\n'
standard_start_string3 += "\tmain()\n"
# standard_start_string3 += '\tapp = QCoreApplication.instance()\n'
standard_start_string3 += '\tprint("protocol finished!")\n'
standard_start_string3 += "\tif app is not None:\n"
standard_start_string3 += "\t\tsys.exit(app.exec())\n"
# standard_start_string += '\treturn plot_dat, additional_step_data\n'

standard_nexus_dict = {
    "/ENTRY[entry]/operator/address": "metadata_start/user/Address (affiliation)",
    "/ENTRY[entry]/operator/affiliation": "metadata_start/user/Affiliation",
    "/ENTRY[entry]/operator/email": "metadata_start/user/E-Mail",
    "/ENTRY[entry]/operator/name": "metadata_start/user/Name",
    "/ENTRY[entry]/operator/orcid": "metadata_start/user/ORCID",
    "/ENTRY[entry]/operator/telephone_number": "metadata_start/user/Phone",
    "/ENTRY[entry]/start_time": "metadata_start/time",
    "/ENTRY[entry]/SAMPLE[sample]/data_identifier": "metadata_start/sample/Identifier",
    "/ENTRY[entry]/SAMPLE[sample]/sample_name": "metadata_start/sample/Name",
    "/ENTRY[entry]/SAMPLE[sample]/sample_history": "metadata_start/sample/Preparation-Info",
    "/ENTRY[entry]/PROCESS[process]/program": "metadata_start/program",
    "/ENTRY[entry]/PROCESS[process]/version": "metadata_start/version",
    "/ENTRY[entry]/SAMPLE[sample]/measured_data": "data",
}


def build_protocol(
    protocol,
    file_path,
    save_path="test.nxs",
    catalog="CAMELS_CATALOG",
    userdata=None,
    sampledata=None,
):
    """Creating the runable python file from a given `protocol`.

    Parameters
    ----------
    protocol : main_classes.protocol_class.Measurement_Protocol
        The protocol that provides the information for the python file.
    file_path : str, path
        The path, where the file should be saved.
    save_path : str, path
         (Default value = 'test.nxs')
         The path, where the data should be saved to.
    catalog : str
         (Default value = 'CAMELS_CATALOG')
         The name of the databroker catalog that should be used.
    userdata : dict, None
         (Default value = None)
         Metadata that describes the user.
    sampledata : dict, None
         (Default value = None)
         Metadata that describes the sample.
    """
    # first the path is prepared
    if not protocol.loop_steps:
        raise Exception(
            f'The protocol "{protocol.name}" is empty.\nYou cannot run or build an empty protocol.'
        )
    if not isinstance(save_path, pathlib.Path):
        save_path = pathlib.Path(save_path)
    if isinstance(save_path, pathlib.WindowsPath):
        save_path = save_path.as_posix()

    # clearing leftovers from former builds
    variables_handling.read_channel_names.clear()
    variables_handling.read_channel_sets.clear()

    # beginning of larger strings
    device_import_string = "\n"
    devices_string = ""
    read_device_drivers_string = ""
    variable_string = "\nnamespace = {}\n"
    variable_string += "all_fits = {}\n"
    variable_string += "plots = []\n"
    variable_string += "boxes = {}\n"
    variable_string += "app = None\n"
    variable_string += f'save_path = "{save_path}"\n'
    variable_string += f'session_name = "{protocol.session_name}"\n'
    variable_string += f"export_to_csv = {protocol.export_csv}\n"
    variable_string += f"export_to_json={protocol.export_json}\n"
    if "new_file_each_run" in variables_handling.preferences:
        variable_string += (
            f'new_file_each_run={variables_handling.preferences["new_file_each_run"]}\n'
        )
    else:
        variable_string += f"new_file_each_run=False\n"
    additional_string_devices = ""
    final_string = "\t\tfor name, device in devs.items():\n"
    final_string += '\t\t\tif hasattr(device, "finalize_steps") and callable(device.finalize_steps):\n'
    final_string += "\t\t\t\tdevice.finalize_steps()\n"

    # now all the variables of the protocol are added to the namespace
    # this includes also the variables of steps such as a foor-loop
    for var, val in protocol.variables.items():
        if variables_handling.check_data_type(val) == "String":
            val = f'"{val}"'
        if "(" in var or ")" in var:
            continue
        variable_string += f"{var} = {val}\n"
        variable_string += f'namespace["{var}"] = {var}\n'
    for var, val in protocol.loop_step_variables.items():
        if variables_handling.check_data_type(val) == "String":
            val = f'"{val}"'
        if "(" in var or ")" in var:
            continue
        variable_string += f"{var} = {val}\n"
        variable_string += f'namespace["{var}"] = {var}\n'
    variable_string += f'\n{protocol.name}_variable_signal = variable_reading.Variable_Signal(name="{protocol.name}_variable_signal", variables_dict=namespace)\n'
    # this handles all the used devices
    for dev in protocol.get_used_devices():
        device = variables_handling.devices[dev]
        classname = device.ophyd_class_name
        if protocol.skip_config:
            config = {}
        else:
            config = copy.deepcopy(device.get_config())
        settings = copy.deepcopy(device.get_settings())
        additional_info = copy.deepcopy(device.get_additional_info())
        # information on the connection is reshaped to be useful
        if "connection" in settings:
            conn = settings.pop("connection")
            if "type" in conn:
                conn.pop("type")
            settings.update(conn)
        if "idn" in settings:
            settings.pop("idn")

        # the non_string settings are strings in the dictionary, but are a known
        # variable or instance, so they are added without quotation marks
        extra_settings = {}
        non_strings = []
        for key in settings:
            if key.startswith("!non_string!_"):
                extra_settings[key.replace("!non_string!_", "")] = settings[key]
                non_strings.append(key)
        for s in non_strings:
            settings.pop(s)

        # same applies to non_string configs
        extra_config = {}
        non_strings = []
        for key in config:
            if key.startswith("!non_string!_"):
                extra_config[key.replace("!non_string!_", "")] = config[key]
                non_strings.append(key)
        for s in non_strings:
            config.pop(s)

        # Information about the device is written into the protocol as well
        additional_info["device_class_name"] = classname
        if "description" in additional_info:
            desc = additional_info["description"].replace("\n", "\n\t\t")
            devices_string += f'\t\t"""{dev} ({classname}):\n\t\t{desc}"""\n'
        devices_string += f"\t\tsettings = {settings}\n"
        devices_string += f"\t\tadditional_info = {additional_info}\n"
        devices_string += f'\t\t{dev} = {classname}("{dev}:", name="{dev}", '
        for key, value in extra_settings.items():
            devices_string += f"{key}={value}, "
        devices_string += "**settings)\n"

        # the devices are being connected, then their config is called and
        # written to the metadata
        devices_string += f'\t\tprint("connecting {dev}")\n'
        devices_string += f"\t\t{dev}.wait_for_connection()\n"
        devices_string += f"\t\tconfig = {config}\n"
        for k, v in extra_config.items():
            devices_string += f'\t\tconfig["{k}"] = {v}\n'
        devices_string += f"\t\tconfigs = {dev}.configure(config)[1]\n"
        devices_string += f'\t\tdevice_config["{dev}"] = {{}}\n'
        devices_string += f'\t\tdevice_config["{dev}"].update(helper_functions.simplify_configs_dict(configs))\n'
        devices_string += f'\t\tdevice_config["{dev}"].update(settings)\n'
        devices_string += f'\t\tdevice_config["{dev}"].update(additional_info)\n'
        devices_string += f'\t\tdevs.update({{"{dev}": {dev}}})\n'
        if device.name in device_handling.local_packages:
            device_import_string += f'sys.path.append(r"{device_handling.local_package_paths[device.name]}")\n'
        device_import_string += f"from nomad_camels_driver_{device.name}.{device.name}_ophyd import {classname}\n"
        additional_string_devices += device.get_additional_string()
        # For each device execute the get_opyd_and_py_file_contents from the helper_functions
        # This adds the .pya and .py files to the metadata dictionary md
        read_device_drivers_string += f"\tmd = helper_functions.get_opyd_and_py_file_contents({classname}, md, '{dev}')\n"






    # finishing up the device initialization
    devices_string += '\t\tprint("devices connected")\n'
    devices_string += f'\t\tmd = {{"devices": device_config, "description": "{repr(protocol.description)}"}}\n'

    # if using special nexus-format, some restructuring of metadata is done
    if protocol.use_nexus:
        md_dict = {}
        for i, name in enumerate(protocol.metadata["Name"]):
            md_dict[name] = protocol.metadata["Value"][i]
        devices_string += f"\t\tmd.update({md_dict})\n"

    # the plots are created
    plot_string, plotting = plot_creator(protocol.plots, multi_stream=True)

    # everything is put together for the complete protocol-string
    protocol_string = "import sys\n"
    protocol_string += (
        f'sys.path.append(r"{os.path.dirname(variables_handling.CAMELS_path)}")\n'
    )
    protocol_string += f'sys.path.append(r"{os.path.dirname(variables_handling.CAMELS_path)}/nomad_camels")\n'
    protocol_string += (
        f'sys.path.append(r"{variables_handling.device_driver_path}")\n\n'
    )
    protocol_string += standard_string
    protocol_string += f"{variable_string}\n\n"
    protocol_string += device_import_string
    protocol_string += protocol.get_outer_string()
    protocol_string += protocol.get_plan_string()
    protocol_string += plot_string
    protocol_string += protocol.get_add_main_string()
    protocol_string += standard_run_string

    # setting up the progress bar
    protocol_string += f'\tprotocol_step_information["total_protocol_steps"] = {protocol.get_total_steps()}\n'
    protocol_string += additional_string_devices

    # add user / sample to metadata
    sampledata = sampledata or {"name": "default_sample"}
    userdata = userdata or {"name": "default_user"}
    protocol_string += user_sample_string(userdata, sampledata)
    protocol_string += f'\tmd["protocol_overview"] = "{protocol.get_short_string().encode("unicode_escape").decode()}"\n'

    # reading the file itself and adding it to the metadata
    protocol_string += '\twith open(__file__, "r", encoding="utf-8") as f:\n'
    protocol_string += '\t\tmd["python_script"] = f.read()\n'
    protocol_string += read_device_drivers_string
    protocol_string += '\tmd["variables"] = namespace\n'

    # adding uid to RunEngine, calling the plan
    protocol_string += '\tRE.subscribe(uid_collector, "start")\n'
    protocol_string += f"\tRE({protocol.name}_plan(devs, md=md, runEngine=RE))\n"

    # wait for RunEngine to finish, then save the data
    standard_save_string = "\tfinally:\n"
    standard_save_string += '\t\twhile RE.state not in ["idle", "panicked"]:\n'
    standard_save_string += "\t\t\timport time\n"
    standard_save_string += "\t\t\ttime.sleep(0.5)\n"
    standard_save_string += "\t\tif uids:\n"
    standard_save_string += "\t\t\truns = catalog[tuple(uids)]\n"
    if protocol.use_nexus:
        nexus_dict = protocol.get_nexus_paths()
        nexus_dict.update(standard_nexus_dict)
        standard_save_string += "\t\t\tdata = broker_to_dict(runs)\n"
        standard_save_string += f"\t\t\tnexus_mapper = {nexus_dict}\n\n"
        # TODO finish this
    else:
        standard_save_string += (
            "\t\t\tbroker_to_NX(runs, save_path, plots,"
            "session_name=session_name,"
            "export_to_csv=export_to_csv,"
            "export_to_json=export_to_json,"
            "new_file_each_run=new_file_each_run)\n\n"
        )

    protocol_string += standard_start_string

    # checking for databroker catalog, using temp if not available
    protocol_string += "\ttry:\n"
    protocol_string += f'\t\tcatalog = databroker.catalog["{catalog}"]\n'
    protocol_string += "\texcept KeyError:\n"
    protocol_string += "\t\timport warnings\n"
    protocol_string += '\t\twarnings.warn("Could not find databroker catalog, using temporary catalog. If data is not transferred, it might get lost.")\n'
    protocol_string += "\t\tcatalog = databroker.temp().v2\n"
    protocol_string += "\tRE.subscribe(catalog.v1.insert)\n\n"

    # progress bar setup
    protocol_string += "\tfrom nomad_camels.utility import tqdm_progress_bar\n"
    protocol_string += (
        f"\ttqdm_bar = tqdm_progress_bar.ProgressBar({protocol.get_total_steps()})\n\n"
    )
    protocol_string += (
        '\tprotocol_step_information["protocol_stepper_signal"] = tqdm_bar\n'
    )

    # all the devices and the actual run are in a try-block
    protocol_string += "\tdevs = {}\n\tdevice_config = {}\n\ttry:\n"
    protocol_string += devices_string
    protocol_string += standard_start_string2
    # protocol_string += '\tfinally:\n'
    protocol_string += standard_save_string
    protocol_string += final_string
    protocol_string += standard_start_string3

    # the string is written to the file
    if not os.path.isdir(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(protocol_string)

    # the protocol is converted to a dictionary and saved as a json
    protocol_dict = load_save_functions.get_save_str(protocol)
    if not isinstance(file_path, pathlib.Path):
        file_path = pathlib.Path(file_path)
    load_save_functions.save_dictionary(file_path.with_suffix(".cprot"), protocol_dict)


def user_sample_string(userdata, sampledata):
    """Returns the string adding userdata and sampledata to the md.

    Parameters
    ----------
    userdata : dict
        data on the user
    sampledata : dict
        data on the sample
    Returns
    -------
    u_s_string : str
        the string containing the data and adding it to the metadata
    """
    u_s_string = f'\tmd["user"] = {userdata}\n'
    u_s_string += f'\tmd["sample"] = {sampledata}\n'
    return u_s_string
