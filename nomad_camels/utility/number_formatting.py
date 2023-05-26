import numpy as np

preferences = {}

def format_number(value):
    """Format a number-string the way it is specified in the preferences.

    Parameters
    ----------
    value :
        

    Returns
    -------

    """
    if isinstance(value, int):
        return str(value)
    if 'number_format' not in preferences or 'n_decimals' not in preferences:
        return str(f'{value:.2f}')
    if preferences['number_format'] == 'plain':
        return f'{value:.{preferences["n_decimals"]}f}'
    elif preferences['number_format'] == 'scientific':
        return f'{value:.{preferences["n_decimals"]}e}'
    else:
        if (np.abs(value) >= 10**preferences['mixed_from'] or np.abs(value) < 10**(-preferences['mixed_from'] + 1)) and value != 0:
            return f'{value:.{preferences["n_decimals"]}e}'
        return f'{value:.{preferences["n_decimals"]}f}'
