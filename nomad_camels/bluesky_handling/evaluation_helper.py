from bluesky.callbacks.core import CallbackBase
import numpy as np
import ast
import time

starttime = time.time()

base_namespace = {"numpy": np, "np": np, 'time': 0}
base_namespace.update({name: getattr(np, name) for name in np.__all__})
base_namespace.update({'StartTime': starttime,
                       'ElapsedTime': time.time() - starttime})


class Evaluator(CallbackBase):
    """ """
    def __init__(self, *args, namespace=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_namespace = {}
        if namespace is not None:
            self.add_namespace = namespace
        self.namespace = base_namespace
        self.update_namespace()
        self.last_update = 0

    def eval_string(self, eval_str:str):
        """

        Parameters
        ----------
        eval_str:str :
            

        Returns
        -------

        """
        self.update_namespace()
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
        self.update_namespace()
        return get_eval(eval_str, self.namespace)

    def start(self, doc):
        """

        Parameters
        ----------
        doc :


        Returns
        -------

        """
        self.namespace['StartTime'] = doc['time']
        super().start(doc)

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
        # self.update_namespace()
        self.last_update = doc['time']

    def update_namespace(self):
        """ """
        self.namespace.update(self.add_namespace)
        self.namespace['ElapsedTime'] = time.time() - self.namespace['StartTime']

    def is_to_date(self, t):
        """

        Parameters
        ----------
        t :
            

        Returns
        -------

        """
        return self.last_update == t


def get_eval(eval_str, namespace):
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
        raise ValueError(f"Could not find {eval_str!r} in namespace or parse it as a Python expression.") from err
    # Try to evaluate it as a Python expression in the namespace.
    try:
        return eval(eval_str, namespace)
    except Exception as err:
        raise ValueError(f"Could not find {eval_str!r} in namespace or evaluate it.") from err
