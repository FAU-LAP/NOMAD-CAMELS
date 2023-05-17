from bluesky.callbacks.core import CallbackBase
import numpy as np
import ast


_base_namespace = {"numpy": np, "np": np, 'time': 0}
_base_namespace.update({name: getattr(np, name) for name in np.__all__})


class Evaluator(CallbackBase):
    """ """
    def __init__(self, *args, namespace=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_namespace = {}
        if namespace is not None:
            self.add_namespace = namespace
        self.namespace = _base_namespace
        self.namespace.update(self.add_namespace)
        self.last_update = 0

    def eval_string(self, eval_str:str):
        """

        Parameters
        ----------
        eval_str:str :
            

        Returns
        -------

        """
        self.namespace.update(self.add_namespace)
        try:
            reter = ''
            for part in eval_str.split('"' if '"' in eval_str else "'"):
                try:
                    reter += str(eval(part, self.namespace))
                except:
                    reter += part
            return reter
        except Exception as err:
            raise ValueError(f"Could not evaluate {eval_str!r}") from err

    def eval(self, eval_str:str):
        """

        Parameters
        ----------
        eval_str:str :
            

        Returns
        -------

        """
        self.namespace.update(self.add_namespace)
        # If it is a key in our namespace, look it up.
        try:
            # This handles field or stream names that are not valid
            # Python identifiers (e.g. ones with spaces in them).
            return self.namespace[eval_str]
        except KeyError:
            pass
        # Check whether it is valid Python syntax.
        try:
            ast.parse(eval_str)
        except SyntaxError as err:
            raise ValueError(f"Could not find {eval_str!r} in namespace or parse it as a Python expression.") from err
        # Try to evaluate it as a Python expression in the namespace.
        try:
            return eval(eval_str, self.namespace)
        except Exception as err:
            raise ValueError(f"Could not find {eval_str!r} in namespace or evaluate it.") from err

    def event(self, doc):
        """

        Parameters
        ----------
        doc :
            

        Returns
        -------

        """
        self.namespace['time'] = doc['time']
        self.namespace.update(doc['data'])
        self.namespace.update(self.add_namespace)
        self.last_update = doc['time']

    def is_to_date(self, t):
        """

        Parameters
        ----------
        t :
            

        Returns
        -------

        """
        return self.last_update == t