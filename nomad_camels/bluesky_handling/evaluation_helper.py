from bluesky.callbacks.core import CallbackBase
import numpy as np
import ast
import time
import scipy.constants as const

# Record the start time of the script
starttime = time.time()

# Create a base namespace with common modules and constants
base_namespace = {
    "numpy": np,
    "np": np,
    "time": 0,
    "const": const
}
# Add all numpy functions to the base namespace
base_namespace.update({name: getattr(np, name) for name in np.__all__})
# Add the start time and elapsed time to the base namespace
base_namespace.update({"StartTime": starttime, "ElapsedTime": time.time() - starttime})

class Evaluator(CallbackBase):
    """
    This class can be used to evaluate strings with names known in bluesky at
    any point, as well inside the run itself. It provides methods to evaluate
    strings and update the namespace dynamically.
    """

    def __init__(self, *args, namespace=None, **kwargs):
        """
        Initializes the Evaluator with an optional additional namespace.

        Parameters
        ----------
        namespace : dict, optional
            The namespace of the run that is added to the default base_namespace.
        """
        super().__init__(*args, **kwargs)
        self.add_namespace = {}  # Additional namespace to be merged with the base namespace
        if namespace is not None:
            self.add_namespace = namespace
        self.namespace = dict(base_namespace)  # Initialize the namespace with the base namespace
        self.update_namespace()  # Update the namespace with the additional namespace
        self.last_update = 0  # Last update time of the namespace
        self.raised_exceptions = []  # List to store raised exceptions

    def eval_string(self, eval_str: str) -> str:
        """
        Evaluates the given string through the provided namespace to another string.
        The string is split at quotation marks and the parts of the string are tried
        to be evaluated. If that is not possible, they are just added back to the string as is.
        Checks if the namespace is up to date before evaluating.

        Parameters
        ----------
        eval_str : str
            The string to be evaluated.

        Returns
        -------
        str
            The evaluated string.

        Raises
        ------
        ValueError
            If there is a bigger problem during evaluation.
        """
        self.update_namespace()  # Ensure the namespace is up to date
        try:
            return_str = ""
            # Split the string at quotation marks and evaluate each part
            for part in eval_str.split('"' if '"' in eval_str else "'"):
                try:
                    return_str += str(eval(part, self.namespace))
                except:
                    return_str += part
            return return_str
        except Exception as err:
            raise ValueError(f"Could not evaluate {eval_str!r}") from err

    def eval(self, eval_str: str, do_not_reraise=False):
        """
        Evaluates the string within the given namespace.
        Checks if the namespace is up to date before evaluating.

        Parameters
        ----------
        eval_str : str
            The string to be evaluated.
        do_not_reraise : bool, optional
            If True, exceptions are not re-raised, and NaN is returned instead.

        Returns
        -------
        Value
            The evaluated value.
        """
        self.update_namespace()  # Ensure the namespace is up to date
        if do_not_reraise:
            return get_eval(eval_str, self.namespace, self)
        return get_eval(eval_str, self.namespace)

    def start(self, doc):
        """
        Overwrites the `start` method to add the variable 'StartTime' to the namespace.
        See bluesky's documentation for more information.

        Parameters
        ----------
        doc : dict
            The start document provided by bluesky.
        """
        self.namespace["StartTime"] = doc["time"]  # Add the start time to the namespace
        super().start(doc)  # Call the superclass method

    def event(self, doc):
        """
        Overwrites the `event` method to add the variable 'time' to the namespace and
        update the `last_update` attribute for checking before evaluation.
        See bluesky's documentation for more information.

        Parameters
        ----------
        doc : dict
            The event document provided by bluesky.
        """
        self.namespace["time"] = doc["time"]  # Add the event time to the namespace
        self.namespace.update(doc["data"])  # Update the namespace with event data
        self.last_update = doc["time"]  # Update the last update time

    def update_namespace(self):
        """
        Updates the namespace with the `add_namespace` dictionary. Since this is
        exactly the given namespace from __init__, it can be easily updated from
        outside the class. Also, the variable 'ElapsedTime' is added to the namespace.

        This method ensures that the namespace is always up-to-date with the latest
        additions and changes.
        """
        self.namespace.update(self.add_namespace) # Update the namespace with the additional namespace
        self.namespace["ElapsedTime"] = (
            self.namespace["time"] - self.namespace["StartTime"]
        ) # Calculate and add the elapsed time to the namespace

    def is_to_date(self, t: float) -> bool:
        """
        Compares whether the given `t` is the same as the Evaluator's last_update.

        Parameters
        ----------
        t : float
            The time to compare with the last update time.

        Returns
        -------
        bool
            True if the given time is the same as the last update time, False otherwise.
        """
        return self.last_update == t

def get_eval(eval_str: str, namespace: dict, evaluator: 'Evaluator' = None):
    """
    Evaluates the given string within the given namespace. Most functionality is
    taken from bluesky.utils.call_or_eval_one.

    Parameters
    ----------
    eval_str : str
        The string to be evaluated.
    namespace : dict
        The namespace in which to evaluate the string.
    evaluator : Evaluator, optional
        The Evaluator instance to use for tracking raised exceptions.

    Returns
    -------
    Value
        The evaluated value.

    Raises
    ------
    ValueError
        If the string cannot be found in the namespace or evaluated as a Python expression.
    """
    # If it is a key in our namespace, look it up.
    if not isinstance(eval_str, str):
        return eval_str
    eval_str = eval_str.strip()
    try:
        # This handles field or stream names that are not valid
        # Python identifiers (e.g. ones with spaces in them).
        return namespace[eval_str]
    except KeyError:
        pass
    # Check whether it is valid Python syntax.
    try:
        ast.parse(eval_str)
    except SyntaxError as err:
        error_text = f"Could not find {eval_str!r} in namespace or evaluate it."
        if evaluator and error_text in evaluator.raised_exceptions:
            return np.nan
        if evaluator is not None:
            evaluator.raised_exceptions.append(error_text)
        raise ValueError(
            f"Could not find {eval_str!r} in namespace or parse it as a Python expression."
        ) from err
    # Try to evaluate it as a Python expression in the namespace.
    try:
        return eval(eval_str, namespace)
    except Exception as err:
        error_text = f"Could not find {eval_str!r} in namespace or evaluate it."
        if evaluator is not None:
            if evaluator and error_text in evaluator.raised_exceptions:
                return np.nan
            evaluator.raised_exceptions.append(error_text)
        raise ValueError(error_text) from err
