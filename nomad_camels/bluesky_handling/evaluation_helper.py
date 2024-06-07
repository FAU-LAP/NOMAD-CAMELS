from bluesky.callbacks.core import CallbackBase
import numpy as np
import ast
import time
import scipy.constants as const

starttime = time.time()

base_namespace = {"numpy": np, "np": np, "time": 0, "const": const}
base_namespace.update({name: getattr(np, name) for name in np.__all__})
base_namespace.update({"StartTime": starttime, "ElapsedTime": time.time() - starttime})


class Evaluator(CallbackBase):
    """
    This class can be used to evaluate strings with names known in bluesky at
    any point, as well inside the run itself.
    """

    def __init__(self, *args, namespace=None, **kwargs):
        """
        Parameters
        ----------
        namespace : dict
            The namespace of the run that is added to the default base_namespace
        """
        super().__init__(*args, **kwargs)
        self.add_namespace = {}
        if namespace is not None:
            self.add_namespace = namespace
        self.namespace = dict(base_namespace)
        self.update_namespace()
        self.last_update = 0

    def eval_string(self, eval_str: str):
        """
        Evaluates the given string through the provided namespace to another
        string. The string is split at quotation marks and the parts of the
        string are tried to be evaluated. If that is not possible, they are just
        added back to the string as is.
        Checks if the namespace is up to date before evaluating.

        Parameters
        ----------
        eval_str : str
            The string to be evaluated.


        Returns
        -------
        return_str
            The evaluated string.

        Raises
        ------
        ValueError
            If there is a bigger problem.

        """
        self.update_namespace()
        try:
            return_str = ""
            for part in eval_str.split('"' if '"' in eval_str else "'"):
                try:
                    return_str += str(eval(part, self.namespace))
                except:
                    return_str += part
            return return_str
        except Exception as err:
            raise ValueError(f"Could not evaluate {eval_str!r}") from err

    def eval(self, eval_str: str):
        """
        Evaluates the string within the given namespace.
        Checks if the namespace is up to date before evaluating.

        Parameters
        ----------
        eval_str : str
            The string to be evaluated.


        Returns
        -------
        Value
            The evaluated value.

        """
        self.update_namespace()
        return get_eval(eval_str, self.namespace)

    def start(self, doc):
        """
        Overwrites the `start` method to add the variable 'StartTime' to the
        namespace.
        See bluesky's documentation for more information.
        """
        self.namespace["StartTime"] = doc["time"]
        super().start(doc)

    def event(self, doc):
        """
        Overwrites the `event` method to add the variable 'time' to the
        namespace and update the `last_update` attribute for checking before
        evaluation.
        See bluesky's documentation for more information.
        """
        self.namespace["time"] = doc["time"]
        self.namespace.update(doc["data"])
        # self.update_namespace()
        self.last_update = doc["time"]

    def update_namespace(self):
        """
        Updates the namespace with the `add_namespace` dictionary. Since this is
        exactly the given namespace from __init__, it can be easily updated from
        outside the class.
        Also the variable 'ElapsedTime' is added to the namespace.
        """
        self.namespace.update(self.add_namespace)
        self.namespace["ElapsedTime"] = time.time() - self.namespace["StartTime"]

    def is_to_date(self, t):
        """
        Compares whether the given `t` is the same as the Evaluator's
        last_update.
        """
        return self.last_update == t


def get_eval(eval_str, namespace):
    """This evaluates the given string within the given namespace.
    Most functionality is taken from bluesky.utils.call_or_eval_one."""
    # If it is a key in our namespace, look it up.
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
        raise ValueError(
            f"Could not find {eval_str!r} in namespace or parse it as a Python expression."
        ) from err
    # Try to evaluate it as a Python expression in the namespace.
    try:
        return eval(eval_str, namespace)
    except Exception as err:
        raise ValueError(
            f"Could not find {eval_str!r} in namespace or evaluate it."
        ) from err
