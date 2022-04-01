import numpy as np

from utility import simpleeval

meas_preset = ''
dev_preset = ''
device_driver_path = ''

protocol_variables = {}
channels = {}
loop_step_variables = {}
devices = {}
evaluation_functions = simpleeval.DEFAULT_FUNCTIONS.copy()
evaluation_functions.update({'exp': np.exp,
                             'ln': np.log,
                             'log': lambda x, y: np.log(x) / np.log(y),
                             'sqrt': np.sqrt,
                             'round': round,
                             'sin': np.sin,
                             'cos': np.cos,
                             'sinh': np.sinh,
                             'cosh': np.cosh,
                             'sinc': np.sinc,
                             'tan': np.tan,
                             'arctan': np.arctan,
                             'arcsin': np.arcsin,
                             'arccos': np.arccos,
                             'arcsinh': np.arcsinh,
                             'arccosh': np.arccosh,
                             'arctanh': np.arctanh})

evaluation_functions_names = {
    'randint()': 'randint(x) - random integer below x',
    'rand()': 'rand() - random float between 0 and 1',
    'round()': 'round(x) - round number to nearest integer',
    'exp()': 'exp(x) - exponential function of x',
    'sqrt()': 'sqrt(x) - square root of x',
    'log(,)': 'log(x,y) - logarithm of x with base y',
    'ln()': 'ln(x) - natural logarithm of x',
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
}

def string_eval(s):
    names = {}
    names.update(protocol_variables)
    names.update(loop_step_variables)
    names.update(channels)
    return simpleeval.simple_eval(s, functions=evaluation_functions, names=names)

def check_eval(s):
    try:
        string_eval(s)
        return True
    except:
        return False
