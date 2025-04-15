"""This module helps to synchronize information between different modules. To
this aim, it holds several variables that may be read from different places.
Furthermore, some functions to work with those variables are provided.

Attributes
----------
    preset : str
        The name of the currently used preset of CAMELS.
    device_driver_path : str, path
        The path, where to find local drivers.
    meas_files_path : str, path
        The path, where to write the measurement files, i.e. data.
    CAMELS_path : str, path
        The path to the current installation of CAMELS.
    preferences : dict
        The currently used preferences.
    protocols : dict{"<protocol_name>": protocol}
        The available protocols.
    protocol_variables : dict{"<name>": <value>}
        The variables provided by the currently viewed protocol.
    channels : dict{"<name>": channel}
        All available channels provided by the configured instruments.
    loop_step_variables : dict{"<name>": <value>}
        The variables provided by the steps of the currently viewed protocol.
    devices : dict
        All configured instruments/devices.
    current_protocol = Measurement_Protocol
        The protocol, that is currently being used.
    dark_mode : bool
        Whether dark-mode is currently active.
    copied_step : Loop_Step
        The last step, that was copied.
    read_channel_sets : list[set]
        Sets of the different channel-compositions for read-channels. Used to distinguish different reads with different channels for bluesky
    read_channel_names : list[str]
        Names of the different read-channel steps in use. Used to distinguish the different reads.
    evaluation_functions_names : dict
        Used to provide the right-click menu to use mathematical functions.
    operator_names : dict
        Used to provide the right-click menu to use mathematical operators.
"""

from ast import literal_eval, parse
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QColor, QAction

import numpy as np
from nomad_camels.bluesky_handling import evaluation_helper
from nomad_camels.ui_widgets.warn_popup import WarnPopup


preset = ""
device_driver_path = ""
meas_files_path = ""
CAMELS_path = ""

preferences = {}

protocols = {}
protocol_variables = {}
channels = {}
config_channels = {}
loop_step_variables = {}
devices = {}
watchdogs = {}
current_protocol = None
dark_mode = False

copied_step = None

channel_aliases = {"channel": [], "Alias": []}
instrument_aliases = {"Instrument": [], "Alias": []}

read_channel_sets = []
read_channel_names = []

evaluation_functions_names = {
    "randint()": "randint(x) - random integer below x",
    "rand()": "rand() - random float between 0 and 1",
    "round()": "round(x) - round number to nearest integer",
    "exp()": "exp(x) - exponential function of x",
    "sqrt()": "sqrt(x) - square root of x",
    "log()": "ln(x) - natural logarithm of x",
    "sin()": "sin(x) - sine of x",
    "cos()": "cos(x) - cosine of x",
    "tan()": "tan(x) - tangent of x",
    "sinh()": "sinh(x) - hyperbolic sine of x",
    "cosh()": "cosh(x) - hyperbolic cosine of x",
    "tanh()": "tanh(x) - hyperbolic tangent of x",
    "arctan()": "arctan(x) - arcus tangent of x",
    "arcsin()": "arcsin(x) - arcus sine of x",
    "arccos()": "arccos(x) - arcus cosine of x",
    "arcsinh()": "arcsinh(x) - area hyperbolic sine of x",
    "arccosh()": "arccosh(x) - area hyperbolic cosine of x",
    "arctanh()": "arctanh(x) - area hyperbolic tangent of x",
    "sinc()": "sinc(x) - sinc function of x",
}

operator_names = {
    "+": "add",
    "-": "subtract",
    "/": "divide",
    "*": "multiply",
    "**": "to the power of",
    "%": "modulus",
    "==": "equals",
    "<": "less than",
    ">": "greater than",
    "<=": "less or equal",
    ">=": "greater or equal",
    "and": "logical AND",
    "or": "logical OR",
    "not": "logical negation",
}


def get_user_default_command(ext):
    try:
        import winreg

        # Read the ProgId from the per-user association:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            rf"Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\{ext}\UserChoice",
        )
        progid, _ = winreg.QueryValueEx(key, "ProgId")
        winreg.CloseKey(key)
    except Exception:
        progid = None

    if progid:
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CLASSES_ROOT, progid + r"\shell\open\command"
            )
            command, _ = winreg.QueryValueEx(key, None)
            winreg.CloseKey(key)
            return command.lower()
        except Exception:
            return ""
    return ""


def open_link(link):
    """
    Open a link or file path using the default program.

    On Windows:
      If a .py file’s default association appears to run it (its command contains "python"),
      the function instead opens it in an editor (or reveals it in Explorer).

    On macOS:
      If the default application’s bundle identifier for the file contains "python",
      reveal the file in Finder; otherwise open with the default association.

    On Linux:
      If the file is a .py file and its default association (queried via MIME)
      contains "python", open its containing folder; otherwise, open normally.

    Parameters
    ----------
    link : str
        The file path to open.
    """
    import os
    import platform
    import subprocess

    try:
        ext = os.path.splitext(link)[-1].lower()
    except Exception:
        ext = ""
    system = platform.system()
    if system == "Windows":
        if ext == ".py":
            # Try to get the user default command for .py from the UserChoice registry key.
            command = get_user_default_command(".py")
            if not command or "python" in command:
                # Default would execute the file.
                subprocess.Popen(["explorer", "/select,", os.path.abspath(link)])
            else:
                os.startfile(link)
        else:
            os.startfile(link)
    elif system == "Darwin":
        if ext == ".py":
            try:
                # Use AppleScript to get the default app's bundle identifier for the file.
                applescript = 'tell application "Finder" to get bundle identifier of (get default application for file (POSIX file "{}") as alias)'.format(
                    link
                )
                default_app = subprocess.check_output(
                    ["osascript", "-e", applescript], universal_newlines=True
                ).strip()
            except Exception:
                default_app = ""
            if not default_app or "python" in default_app.lower():
                # Reveal the file in Finder if the default app is Python-related
                subprocess.call(["open", "-R", link])
            else:
                subprocess.call(["open", link])
        else:
            subprocess.call(["open", link])
    else:
        # Linux
        if ext == ".py":
            try:
                mime_type = "text/x-python"
                desktop = subprocess.check_output(
                    ["xdg-mime", "query", "default", mime_type], universal_newlines=True
                ).strip()
            except Exception:
                desktop = ""
            if "python" in desktop.lower():
                folder = os.path.dirname(os.path.abspath(link))
                subprocess.call(["xdg-open", folder])
            else:
                subprocess.call(["xdg-open", link])
        else:
            subprocess.call(["xdg-open", link])
            
def get_channels(use_aliases=True):
    """Returns the channels"""
    if use_aliases:
        channels_dict = {}
        for channel in channels:
            if channel in channel_aliases["channel"]:
                i = channel_aliases["channel"].index(channel)
                channels_dict.update({channel_aliases["Alias"][i]: channels[channel]})
            elif (instr := channels[channel].device) in instrument_aliases[
                "Instrument"
            ]:
                i = instrument_aliases["Instrument"].index(instr)
                alias = instrument_aliases["Alias"][i]
                channel_name = channels[channel].name.split(".")[-1]
                channels_dict.update({f"{alias}_{channel_name}": channels[channel]})
            else:
                channels_dict.update({channel: channels[channel]})
        return channels_dict
    return channels


def get_non_channel_functions():
    functions = []
    for device in devices.values():
        functions += device.get_non_channel_functions()
    return functions


def get_output_channels(use_aliases=True):
    """Goes through all channels and returns a list of the names of those, that
    are outputs."""
    outputs = []
    chans = get_channels(use_aliases)
    for channel in chans:
        if chans[channel].output:
            outputs.append(channel)
    return outputs


def get_color(color="", string=False):
    """Returns the respective QColor or rgb-code(if `string`) for
    `color`, taking dark-mode into account.

    Parameters
    ----------
    color : str
        (Default value = '')
        The name of the color asked for. Possible values are "red" / "r",
        "strong_red", "green" / "g", "dark_green", "grey" / "gray", "blue" / "b"
        "black" (white if `dark_mode`), "orange". Otherwise white (or black, if
        `dark_mode`) is returned.
    string : bool
        (Default value = False)
        If True, only the string of the rgb will be returned, not the QColor.
    """
    if color == "red" or color == "r":
        rgb = (255, 180, 180)
        if dark_mode:
            rgb = (75, 0, 0)
    elif color == "strong_red":
        rgb = (230, 0, 0)
    elif color == "green" or color == "g":
        rgb = (180, 255, 180)
        if dark_mode:
            rgb = (0, 75, 0)
    elif color == "dark_green":
        rgb = (32, 175, 32)
    elif color == "grey" or color == "gray":
        rgb = (169, 169, 169)
    elif color == "blue" or color == "b":
        rgb = (180, 180, 255)
        if dark_mode:
            rgb = (0, 0, 75)
    elif color == "black":
        rgb = (0, 0, 0)
        if dark_mode:
            rgb = (255, 255, 255)
    elif color == "orange":
        rgb = (255, 170, 25)
    else:
        rgb = (255, 255, 255)
        if dark_mode:
            rgb = (0, 0, 0)
    if string:
        return str(rgb)
    return QColor(*rgb)


def get_menus(connect_function, pretext="Insert", use_aliases=True):
    """Providing QMenus with the `connect_function` for each action,
    containing all the variables, channels, functions and operators.

    Parameters
    ----------
    connect_function : callable
        The function that should be executed when the action is clicked. It gets
        the variable's name as a value.
    pretext : str
        (Default value = 'Insert')
        This string will be written in front of the menus.

    Returns
    -------
    menus : list[QMenu]
        the created menus
    actions : list[list[QAction]]
        lists of the individual actions in the menus
    """
    variable_menu = QMenu(f"{pretext} Variable")
    channel_menu = QMenu(f"{pretext} Channel-Value")
    function_menu = QMenu(f"{pretext} Function")
    operator_menu = QMenu(f"{pretext} Operator")
    channel_actions = []
    operator_actions = []
    actions = []
    function_actions = []
    add_actions_from_dict(get_channels(use_aliases), channel_actions, connect_function)
    add_actions_from_dict(protocol_variables, actions, connect_function)
    add_actions_from_dict(loop_step_variables, actions, connect_function)
    add_actions_from_dict({"StartTime": 1, "ElapsedTime": 1}, actions, connect_function)
    add_actions_from_dict(operator_names, operator_actions, connect_function)
    add_actions_from_dict(
        evaluation_functions_names, function_actions, connect_function
    )
    channel_menu.addActions(channel_actions)
    variable_menu.addActions(actions)
    operator_menu.addActions(operator_actions)
    function_menu.addActions(function_actions)
    if pretext == "Insert":
        menus = [channel_menu, variable_menu, function_menu]
        actions = [channel_actions, actions, function_actions]
    else:
        menus = [channel_menu, variable_menu, operator_menu, function_menu]
        actions = [channel_actions, actions, operator_actions, function_actions]
    return menus, actions


def add_actions_from_dict(dictionary, actions, connect_function, add_string=""):
    """
    The values of `dictionary` are handed to the `connect_function` when
    clicking on the respective action named with the keys of the dictionary. The
    created actions are added to `actions`.

    Parameters
    ----------
    dictionary : dict
        the keys become the names of the actions, the values are handed to the
        `connect_function`
    actions : list
        the created actions will be added to this list
    connect_function : callable
        this function is called, when one of the actions is clicked
    add_string : str
        (Default value = '')
        added in front of the values of the dictionary for the connect_function
    """
    for var in sorted(dictionary, key=lambda x: x.lower()):
        if isinstance(dictionary[var], dict):
            add_actions_from_dict(dictionary[var], actions, connect_function, f"{var}:")
        else:
            addvar = f"{add_string}{var}"
            action = QAction(addvar)
            action.triggered.connect(lambda state=None, x=addvar: connect_function(x))
            actions.append(action)


def check_eval(s, use_aliases=True):
    """Checks, whether the string `s` can be evaluated. Returns True if it is
    possible, otherwise False.

    Parameters
    ----------
    s : str
        the string that should be checked
    """
    try:
        namespace = dict(evaluation_helper.base_namespace)
        namespace.update(protocol_variables)
        namespace.update(loop_step_variables)
        for channel in get_channels(use_aliases):
            namespace.update({channel: 1})
        # utils.call_or_eval_one(s, namespace)
        evaluation_helper.get_eval(s, namespace)
        return True
    except Exception:
        return False


def get_eval(s, use_aliases=True):
    """
    Evaluates the string `s` with the namespace of `protocol_variables` and
    `loop_step_variables` in addition to `evaluation_helper.base_namespace`.
    Returns the evaluated value.

    Parameters
    ----------
    s : str
        the string that should be evaluated
    """
    try:
        namespace = dict(evaluation_helper.base_namespace)
        namespace.update(protocol_variables)
        namespace.update(loop_step_variables)
        for channel in get_channels(use_aliases):
            namespace.update({channel: 1})
        return evaluation_helper.get_eval(s, namespace)
    except:
        return np.nan


def get_data(s):
    """Used instead of `get_eval` when there is no specific namespace. It simply
    uses `ast.literal_eval` and if it does not work, the string `s` is returned.

    Parameters
    ----------
    s : str
        the string to be evaluated
    """
    if not s:
        return ""
    try:
        lit = literal_eval(s)
    except ValueError:
        return s
    except SyntaxError:
        return s
    return lit


def check_data_type(s):
    """Returns the datatype of the string-evaluation of s.

    Parameters
    ----------
    s : str
        the string that should be checked
    """
    if not isinstance(s, str):
        return str(type(s))
    if not s:
        return ""
    try:
        lit = literal_eval(s)
    except ValueError:
        return "String"
    except SyntaxError:
        return "String"
    return str(type(lit))


def get_write_from_data_type(s):
    """Used for writing longer strings. Since the strings should stay strings in
    the written files, if the evaluated datatype of `s` is str, quotation marks
    will be added around the value, otherwise nothing is done."""
    t = check_data_type(s)
    if t == "String":
        return f'"{s}"'
    return s


def check_variable_name(name, raise_not_warn=False, parent=None):
    """Checks whether `name` is a valid name for a variable. It checks, whether
    the name mirrors a builtin function or keyword. If not, it is tried with ast
    to parse the statement `<name> = None`, i.e. whether it works as a variable
    name. If anything fails, either an exception is raised (if `raise_not_warn`)
    or a `WarnPopup` is called.

    Parameters
    ----------
    name : str
        the name that should be checked
    raise_not_warn : bool
        (Default value = False)
        if True, an exception is raised if a check fails, otherwise a WarnPopup
    parent : QWidget
        (Default value = None)
        the parent widget for a possibly called WarnPopup
    """
    try:
        built_check = name in vars(__builtins__)
    except:
        built_check = name in __builtins__
    if built_check:
        text = (
            f'The name "{name}" is a python builtin function! Please use another name.'
        )
        if raise_not_warn:
            raise Exception(text)
        WarnPopup(parent, text, "Invalid Name")
        return False
    try:
        parse(f"{name} = None")
    except (ValueError, SyntaxError, TypeError) as e:
        text = f'The name "{name}" is not a valid name! Remove e.g. spaces or special characters.'
        if raise_not_warn:
            raise Exception(text) from e
        WarnPopup(parent, text, "Invalid Name")
        return False
    return True
