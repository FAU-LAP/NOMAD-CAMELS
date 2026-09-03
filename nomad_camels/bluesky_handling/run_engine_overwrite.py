from bluesky import run_engine, RunEngine
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


def _semantic_document_callback(name, doc):
    """A `RunEngine` document callback that writes the semantic annotation of a
    stream into the data keys of that stream's descriptor.

    suitcase writes every entry of a data key as an attribute of the dataset it
    belongs to, so this is what carries an IRI from the protocol all the way to
    the data. Doing it here rather than on the signal is what allows one channel
    to mean different things in different read steps: a signal exists once per
    channel, a descriptor exists once per stream.

    Registered as the very first subscriber on `RunEngineOverwrite` (see
    `RunEngineOverwrite.__init__`), so it runs before every other subscriber
    (the databroker catalog insert, any ZMQ publisher, `CAMELSSerializer`) and
    mutates the descriptor document they all receive by reference - unlike a
    private `RunBundler` hook (only available from bluesky 1.11.0), this only
    relies on the public, version-stable `RunEngine.subscribe` API.
    """
    if name == "start":
        # One run's worth of annotations must not leak into the next.
        semantic_runtime.reset()
        return
    if name != "descriptor":
        return
    try:
        _add_semantics(doc)
    except Exception as e:
        # An annotation is never worth losing a measurement over.
        logging.warning(f"Could not add semantic annotation to a descriptor: {e}")


def _add_semantics(doc):
    """Adds the semantic annotation of `doc`'s stream to its data keys, if
    there is one - in place, so that every subscriber of this descriptor
    (already registered or not) sees the same, annotated document.

    The experiment-class description is not part of this: it is written once,
    as an attribute of the run's top-level "data" group, by
    `CAMELSSerializer._write_experiment_description` instead of being
    repeated onto every data key here."""
    annotations = semantic_runtime.get(doc["name"]) or {}
    if not annotations:
        return
    # The data keys of an object are its cached `describe()` output, shared
    # by every stream reading it. Copy before writing, or the annotation of
    # one stream would show up in all the others.
    data_keys = doc["data_keys"]
    for key, data_key in list(data_keys.items()):
        own = annotations.get(key)
        if not own:
            continue
        data_key = dict(data_key)
        # Only non-empty strings, h5py cannot store None as an attribute.
        if own.get("iri"):
            data_key["semantic_iri"] = str(own["iri"])
        if own.get("label"):
            data_key["semantic_label"] = str(own["label"])
        if own.get("description"):
            data_key["semantic_description"] = str(own["description"])
        data_keys[key] = data_key


class RunEngineOverwrite(RunEngine):
    """
    A class that overwrites the `RunEngine` class from bluesky to add a custom read method.
    This class is used to handle the reading of objects in a more robust way, especially when dealing with exceptions. It allows to keep running the run engine even if an object raises an exception during the read process.
    It further subscribes a callback that annotates descriptors semantically.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Registered here, before the app adds any of its own subscribers
        # (databroker catalog insert, ZMQ publisher, CAMELSSerializer, ...),
        # so this always runs first and every other subscriber sees the
        # annotated descriptor.
        self.subscribe(_semantic_document_callback, name="all")

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
