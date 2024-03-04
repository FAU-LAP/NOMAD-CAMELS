"""Provides a function to rename typical names for fit-variables to valid
python-names"""

fit_variable_changer = {
    "+": "plus",
    "-": "minus",
    "=": "equals",
    "==": "equals",
    "/": "divide",
    "*": "times",
    "**": "power",
    "<": "less",
    ">": "greater",
    "(": "bracketL",
    ")": "bracketR",
    ".": "dot",
    ",": "comma",
    " ": "_",
}


def replace_name(var_name):
    """
    Replaces mathematical symbols with text so that the variable name becomes a
    valid name.

    Parameters
    ----------
    var_name : str
        The variable that should be renamed.
    """
    for key in fit_variable_changer:
        var_name = var_name.replace(key, fit_variable_changer[key])
    return var_name
