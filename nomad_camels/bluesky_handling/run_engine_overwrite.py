from bluesky import run_engine, RunEngine
from bluesky.bundlers import RunBundler
import logging

from nomad_camels.bluesky_handling import semantic_runtime


def get_nan_value(value):
    """
    Returns a NaN value of the same type as the input value.
    For example:
    If the input value is a numpy array, it returns an array of NaNs with the same shape.
    If the input value is a list, it returns a list of NaNs with the same length.
    If the input value is a dictionary, it returns an empty dictionary.
    """
    import numpy as np

    if isinstance(value, np.ndarray):
        return np.full(value.shape, np.nan)
    if isinstance(value, (int, float, np.number)):
        return np.nan
    if isinstance(value, str):
        return ""
    if isinstance(value, list):
        return [np.nan] * len(value)
    if isinstance(value, dict):
        return {}
    if isinstance(value, tuple):
        return tuple([np.nan] * len(value))
    if isinstance(value, set):
        return set()
    if isinstance(value, bool):
        return False
    if isinstance(value, complex):
        return np.nan
    return None


class SemanticRunBundler(RunBundler):
    """A `RunBundler` that writes the semantic annotation of a stream into the
    data keys of that stream's descriptor.

    suitcase writes every entry of a data key as an attribute of the dataset it
    belongs to, so this is what carries an IRI from the protocol all the way to
    the data. Doing it here rather than on the signal is what allows one channel
    to mean different things in different read steps: a signal exists once per
    channel, a descriptor exists once per stream.
    """

    def __init__(self, *args, **kwargs):
        # One bundler is created per run, so this is where a protocol stops
        # seeing the annotations of the protocol before it.
        semantic_runtime.reset()
        super().__init__(*args, **kwargs)

    async def _prepare_stream(self, desc_key, objs_dks):
        try:
            objs_dks = self._add_semantics(desc_key, objs_dks)
        except Exception as e:
            # An annotation is never worth losing a measurement over.
            logging.warning(f"Could not add semantic annotation to a descriptor: {e}")
        return await super()._prepare_stream(desc_key, objs_dks)

    @staticmethod
    def _add_semantics(desc_key, objs_dks):
        """Returns `objs_dks` with the annotations of the stream `desc_key`
        added, or unchanged if there are none."""
        annotations = semantic_runtime.get(desc_key)
        if not annotations:
            return objs_dks
        # The data keys of an object are its cached `describe()` output, shared
        # by every stream reading it. Copy before writing, or the annotation of
        # one stream would show up in all the others.
        copied = {
            obj: {
                key: dict(data_key) if key in annotations else data_key
                for key, data_key in data_keys.items()
            }
            for obj, data_keys in objs_dks.items()
        }
        for data_keys in copied.values():
            for key, data_key in data_keys.items():
                if key not in annotations:
                    continue
                # Only non-empty strings, h5py cannot store None as an attribute.
                if annotations[key].get("iri"):
                    data_key["semantic_iri"] = str(annotations[key]["iri"])
                if annotations[key].get("label"):
                    data_key["semantic_label"] = str(annotations[key]["label"])
        return copied


class RunEngineOverwrite(RunEngine):
    """
    A class that overwrites the `RunEngine` class from bluesky to add a custom read method.
    This class is used to handle the reading of objects in a more robust way, especially when dealing with exceptions. It allows to keep running the run engine even if an object raises an exception during the read process.
    It further uses a bundler that annotates descriptors semantically.
    """

    async def _read(self, msg):
        obj = run_engine.check_supports(msg.obj, run_engine.Readable)
        # actually _read_ the object
        run_engine.warn_if_msg_args_or_kwargs(msg, obj.read, msg.args, msg.kwargs)
        # the try except block is added
        if hasattr(obj, "__read_w_except__") and obj.__read_w_except__:
            try:
                ret = await run_engine.maybe_await(obj.read(*msg.args, **msg.kwargs))
            except Exception as e:
                logging.warning(f"Error reading object: {obj}, Exception: {e}")
                print("Error reading object: ", obj)
                print("Exception: ", e)
                import time

                ret = {
                    obj.name: {
                        "value": get_nan_value(obj.value),
                        "timestamp": time.time(),
                    }
                }
        else:
            ret = await run_engine.maybe_await(obj.read(*msg.args, **msg.kwargs))

        if ret is None:
            raise RuntimeError(
                f"The read of {obj.name} returned None. "
                "This is a bug in your object implementation, "
                "`read` must return a dictionary."
            )
        run_key = msg.run
        try:
            current_run = self._run_bundlers[run_key]
        except KeyError:
            ...
        else:
            await current_run.read(msg, ret)

        return ret


# `RunEngine` instantiates its bundler via `type(self).RunBundler(...)`, so
# overwriting the class attribute is enough. Guarded, since `_prepare_stream` is
# not part of the public bluesky API; without it, data is written as before,
# only without the semantic annotation.
if hasattr(RunBundler, "_prepare_stream"):
    RunEngineOverwrite.RunBundler = SemanticRunBundler
