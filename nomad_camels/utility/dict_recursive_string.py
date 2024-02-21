def dict_recursive_string(data, indent=0):
    """Recursively adds the given dictionary `data` to a string in the format
    "key: value" where each key-value pair has its own line and nested
    dictionaries are indented. Returns the resulting string."""
    rec_string = ""
    for key, value in data.items():
        if isinstance(value, dict):
            rec_string += f"{' ' * 4 * indent}{key}:"
            rec_string += dict_recursive_string(value, indent + 1)
        else:
            rec_string += f"{' ' * 4 * indent}{key}: {value}\n"
    return rec_string
