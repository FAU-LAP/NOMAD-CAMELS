fit_variable_changer = {'+': 'plus',
                        '-': 'minus',
                        '=': 'equals',
                        '==': 'equals',
                        '/': 'devide',
                        '*': 'times',
                        '**': 'power',
                        '<': 'less',
                        '>': 'greater',
                        '(': 'bracketL',
                        ')': 'bracketR',
                        '.': 'dot',
                        ',': 'comma',
                        ' ': '_'}

def replace_name(var_name):
    for key in fit_variable_changer:
        var_name = var_name.replace(key, fit_variable_changer[key])
    return var_name
