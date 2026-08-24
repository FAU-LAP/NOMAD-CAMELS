"""Holds the semantic annotations of the protocol that is currently running,
keyed by the data stream they belong to.

The annotation of a channel is defined per read step, so the same channel may
mean two different things in two read steps of one protocol. A signal object
however exists once per channel, which is why the annotation must not be
attached to it. It is attached to the descriptor of a stream instead, and the
stream is what this module keys on.

The name of a stream is only known at runtime, since it depends on the
``stream_name`` a protocol is called with, and a sub-protocol is built once but
may be called from several places with a different one. The generated protocol
therefore registers its annotations here right before reading, and
`run_engine_overwrite.SemanticRunBundler` looks them up while composing the
descriptor.

The registry is deliberately global to the process: the protocol module and
every sub-protocol module import this same module, and the RunEngine reading
from it runs in the same process.
"""

import logging

_stream_annotations = {}
_checked_support = False
_experiment_description = ""


def _warn_if_unsupported():
    """Warns once per run if the installed bluesky is too old to annotate
    descriptors, so that the annotation does not go missing silently."""
    global _checked_support
    if _checked_support:
        return
    _checked_support = True
    from bluesky.bundlers import RunBundler

    if not hasattr(RunBundler, "_prepare_stream"):
        logging.warning(
            "The installed version of bluesky cannot annotate data streams "
            "(this needs bluesky >= 1.11.0). The semantic mapping is still "
            "written to the metadata of the file, but the individual datasets "
            "will not carry their IRI."
        )


def register(stream_name, annotations):
    """Records the annotations of the channels read into `stream_name`.

    Parameters
    ----------
    stream_name : str
        The resolved name of the stream, i.e. the name as it is passed to
        `bluesky.plan_stubs.create`.
    annotations : dict, None
        {data_key: {"label": str, "iri": str}}. Falsy values are ignored, so
        that an unannotated read does not have to check before calling.
    """
    if not annotations:
        return
    _warn_if_unsupported()
    _stream_annotations.setdefault(stream_name, {}).update(annotations)


def get(stream_name):
    """Returns the annotations registered for `stream_name`, or None."""
    return _stream_annotations.get(stream_name, None)


def set_experiment_description(description):
    """Records the protocol's selected experiment-class description for the
    run currently being built, so it can be stamped onto every read channel's
    dataset. Called once, right after `open_run`."""
    global _experiment_description
    _experiment_description = str(description) if description else ""


def get_experiment_description():
    """Returns the experiment-class description registered for the run
    currently being built, or "" if none was set."""
    return _experiment_description


def reset():
    """Forgets all registered annotations. Called when a run starts, so that a
    protocol cannot see the annotations of the one before it."""
    global _checked_support, _experiment_description
    _stream_annotations.clear()
    _checked_support = False
    _experiment_description = ""
