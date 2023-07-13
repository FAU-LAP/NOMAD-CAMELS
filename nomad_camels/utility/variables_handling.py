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

evaluation_functions_names

operator_names
"""

from ast import literal_eval, parse
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QColor, QAction

import numpy as np
from nomad_camels.bluesky_handling import evaluation_helper
from nomad_camels.ui_widgets.warn_popup import WarnPopup


preset = ''
device_driver_path = ''
meas_files_path = ''
CAMELS_path = ''

preferences = {}

protocols = {}
protocol_variables = {}
channels = {}
loop_step_variables = {}
devices = {}
current_protocol = None
dark_mode = False

copied_step = None

read_channel_sets = []
read_channel_names = []

evaluation_functions_names = {
    'randint()': 'randint(x) - random integer below x',
    'rand()': 'rand() - random float between 0 and 1',
    'round()': 'round(x) - round number to nearest integer',
    'exp()': 'exp(x) - exponential function of x',
    'sqrt()': 'sqrt(x) - square root of x',
    'log()': 'ln(x) - natural logarithm of x',
    'sin()': 'sin(x) - sine of x',
    'cos()': 'cos(x) - cosine of x',
    'tan()': 'tan(x) - tangent of x',
    'sinh()': 'sinh(x) - hyperbolic sine of x',
    'cosh()': 'cosh(x) - hyperbolic cosine of x',
    'tanh()': 'tanh(x) - hyperbolic tangent of x',
    'arctan()': 'arctan(x) - arcus tangent of x',
    'arcsin()': 'arcsin(x) - arcus sine of x',
    'arccos()': 'arccos(x) - arcus cosine of x',
    'arcsinh()': 'arcsinh(x) - area hyperbolic sine of x',
    'arccosh()': 'arccosh(x) - area hyperbolic cosine of x',
    'arctanh()': 'arctanh(x) - area hyperbolic tangent of x',
    'sinc()': 'sinc(x) - sinc function of x'
}

operator_names = {
    '+': 'add',
    '-': 'subtract',
    '/': 'devide',
    '*': 'multiply',
    '**': 'to the power of',
    '%': 'modulus',
    '==': 'equals',
    '<': 'less than',
    '>': 'greater than',
    '<=': 'less or equal',
    '>=': 'greater or equal',
    'and': 'logical AND',
    'or': 'logical OR',
    'not': 'logical negation'
}


def get_output_channels():
    """ """
    outputs = []
    for channel in channels:
        if channels[channel].output:
            outputs.append(channel)
    return outputs

def get_color(color='', string=False):
    """Returns the respective QColor or rgb-code(if `string`) for
    `color`, taking dark-mode into account.

    Parameters
    ----------
    color :
         (Default value = '')
    string :
         (Default value = False)

    Returns
    -------

    """
    if color == 'red' or color == 'r':
        rgb = (255, 180, 180)
        if dark_mode:
            rgb = (75, 0, 0)
    elif color == 'strong_red':
        rgb = (230, 0, 0)
    elif color == 'green' or color == 'g':
        rgb = (180, 255, 180)
        if dark_mode:
            rgb = (0, 75, 0)
    elif color == 'dark_green':
        rgb = (32, 175, 32)
    elif color == 'grey' or color == 'gray':
        rgb = (169, 169, 169)
    elif color == 'blue' or color == 'b':
        rgb = (180, 180, 255)
        if dark_mode:
            rgb = (0, 0, 75)
    elif color == 'black':
        rgb = (0, 0, 0)
        if dark_mode:
            rgb = (255, 255, 255)
    elif color == 'orange':
        rgb = (255, 170, 25)
    else:
        rgb = (255, 255, 255)
        if dark_mode:
            rgb = (0, 0, 0)
    if string:
        return str(rgb)
    return QColor(*rgb)

def get_menus(connect_function, pretext='Insert'):
    """Providing QMenus with the `connect_function` for each action,
    containing all the variables, channels, functions and operators.

    Parameters
    ----------
    connect_function :
        
    pretext :
         (Default value = 'Insert')

    Returns
    -------

    """
    variable_menu = QMenu(f'{pretext} Variable')
    channel_menu = QMenu(f'{pretext} Channel-Value')
    function_menu = QMenu(f'{pretext} Function')
    operator_menu = QMenu(f'{pretext} Operator')
    channel_actions = []
    operator_actions = []
    actions = []
    function_actions = []
    add_actions_from_dict(channels, channel_actions, connect_function)
    add_actions_from_dict(protocol_variables, actions, connect_function)
    add_actions_from_dict(loop_step_variables, actions, connect_function)
    add_actions_from_dict({'StartTime': 1, 'ElapsedTime': 1}, actions,
                          connect_function)
    add_actions_from_dict(operator_names, operator_actions, connect_function)
    add_actions_from_dict(evaluation_functions_names, function_actions,
                          connect_function)
    channel_menu.addActions(channel_actions)
    variable_menu.addActions(actions)
    operator_menu.addActions(operator_actions)
    function_menu.addActions(function_actions)
    if pretext == 'Insert':
        menus = [channel_menu, variable_menu, function_menu]
        actions = [channel_actions, actions, function_actions]
    else:
        menus = [channel_menu, variable_menu, operator_menu, function_menu]
        actions = [channel_actions, actions, operator_actions, function_actions]
    return menus, actions

def add_actions_from_dict(dictionary, actions, connect_function, add_string=''):
    """

    Parameters
    ----------
    dictionary :
        
    actions :
        
    connect_function :
        
    add_string :
         (Default value = '')

    Returns
    -------

    """
    for var in sorted(dictionary, key=lambda x: x.lower()):
        if isinstance(dictionary[var], dict):
            add_actions_from_dict(dictionary[var], actions, connect_function,
                                  f'{var}:')
        else:
            addvar = f'{add_string}{var}'
            action = QAction(addvar)
            action.triggered.connect(lambda state=None, x=addvar: connect_function(x))
            actions.append(action)

def check_eval(s):
    """Checks, whether the string `s` can be evaluated.

    Parameters
    ----------
    s :
        

    Returns
    -------

    """
    try:
        namespace = dict(evaluation_helper.base_namespace)
        namespace.update(protocol_variables)
        namespace.update(loop_step_variables)
        for channel in channels:
            namespace.update({channel: 1})
        # utils.call_or_eval_one(s, namespace)
        evaluation_helper.get_eval(s, namespace)
        return True
    except Exception:
        return False

def get_eval(s):
    """

    Parameters
    ----------
    s :
        

    Returns
    -------

    """
    try:
        namespace = dict(evaluation_helper.base_namespace)
        namespace.update(protocol_variables)
        namespace.update(loop_step_variables)
        for channel in channels:
            namespace.update({channel: 1})
        return evaluation_helper.get_eval(s, namespace)
    except:
        return np.nan


def get_data(s):
    """Returns the evaluated data of s.

    Parameters
    ----------
    s :
        

    Returns
    -------

    """
    if not s:
        return ''
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
    s :
        

    Returns
    -------

    """
    if not isinstance(s, str):
        return str(type(s))
    if not s:
        return ''
    try:
        lit = literal_eval(s)
    except ValueError:
        return 'String'
    except SyntaxError:
        return 'String'
    return str(type(lit))

def get_write_from_data_type(s):
    """

    Parameters
    ----------
    s :
        

    Returns
    -------

    """
    t = check_data_type(s)
    if t == 'String':
        return f'"{s}"'
    return s


def check_variable_name(name, raise_not_warn=False, parent=None):
    try:
        built_check = name in vars(__builtins__)
    except:
        built_check = name in __builtins__
    if built_check:
        text = f'The name "{name}" is a python builtin function! Please use another name.'
        if raise_not_warn:
            raise Exception(text)
        WarnPopup(parent, text, 'Invalid Name')
        return False
    try:
        parse(f'{name} = None')
    except (ValueError, SyntaxError, TypeError):
        text = f'The name "{name}" is not a valid name! Remove e.g. spaces or special characters.'
        if raise_not_warn:
            raise Exception(text)
        WarnPopup(parent, text, 'Invalid Name')
        return False
    return True


