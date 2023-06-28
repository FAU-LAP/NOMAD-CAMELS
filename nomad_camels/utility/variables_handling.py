from ast import literal_eval, parse
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QColor, QAction

import numpy as np
# from nomad_camels.utility import simpleeval
from nomad_camels.bluesky_handling import evaluation_helper
from nomad_camels.ui_widgets.warn_popup import WarnPopup

# from bluesky_widgets.models import utils

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


def get_output_channels():
    """ """
    outputs = []
    for channel in channels:
        if channels[channel].output:
            outputs.append(channel)
    return outputs

# evaluation_functions = simpleeval.DEFAULT_FUNCTIONS.copy()
# evaluation_functions.update({'exp': np.exp,
#                              'log': np.log,
#                              'sqrt': np.sqrt,
#                              'round': round,
#                              'sin': np.sin,
#                              'cos': np.cos,
#                              'sinh': np.sinh,
#                              'cosh': np.cosh,
#                              'sinc': np.sinc,
#                              'tan': np.tan,
#                              'arctan': np.arctan,
#                              'arcsin': np.arcsin,
#                              'arccos': np.arccos,
#                              'arcsinh': np.arcsinh,
#                              'arccosh': np.arccosh,
#                              'arctanh': np.arctanh})


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
    # for channel in sorted(channels, key=lambda x: x.lower()):
    #     action = QAction(channel)
    #     action.triggered.connect(lambda state=None, x=channel: connect_function(x))
    #     channel_actions.append(action)
    add_actions_from_dict(protocol_variables, actions, connect_function)
    # for variable in sorted(protocol_variables, key=lambda x: x.lower()):
    #     action = QAction(variable)
    #     action.triggered.connect(lambda state=None, x=variable: connect_function(x))
    #     actions.append(action)
    add_actions_from_dict(loop_step_variables, actions, connect_function)
    add_actions_from_dict({'StartTime': 1, 'ElapsedTime': 1}, actions,
                          connect_function)
    # for variable in sorted(loop_step_variables, key=lambda x: x.lower()):
    #     action = QAction(variable)
    #     action.triggered.connect(lambda state=None, x=variable: connect_function(x))
    #     actions.append(action)
    add_actions_from_dict(operator_names, operator_actions, connect_function)
    # for op in operator_names:
    #     action = QAction(f'{op}\t{operator_names[op]}')
    #     action.triggered.connect(lambda state=None, x=op: connect_function(x))
    #     operator_actions.append(action)
    add_actions_from_dict(evaluation_functions_names, function_actions,
                          connect_function)
    # for foo in sorted(evaluation_functions_names, key=lambda x: x.lower()):
    #     action = QAction(evaluation_functions_names[foo])
    #     action.triggered.connect(lambda state=None, x=foo: connect_function(x))
    #     function_actions.append(action)
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


