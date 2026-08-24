import json
import logging
from itertools import zip_longest

from nomad_camels.utility import variables_handling


def _get(obj, key, default=None):
    """Access dict-like and object-like CAMELS structures uniformly."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _is_set(value):
    return value is not None and value != "" and value != [] and value != {}


def _semantic(label, iri):
    return {
        "label": label,
        "iri": iri,
    }


def _experiment_annotation(protocol):
    label = _get(protocol, "experiment_ontology_class", "")
    iri = _get(protocol, "experiment_ontology_class_iri", "")
    if not _is_set(label) and not _is_set(iri):
        return None
    return {
        "target": {
            "type": "measurement",
        },
        "semantic": _semantic(label, iri),
    }


def _iter_steps(protocol):
    """
    Iterate over top-level and nested loop steps while avoiding duplicates.
    ``loop_steps`` preserves the visible top-level order. ``loop_step_dict`` may
    additionally contain nested child steps. Both sources are combined and
    de-duplicated by object identity.
    """
    seen = set()
    sources = [
        _get(protocol, "loop_steps", []) or [],
        (_get(protocol, "loop_step_dict", {}) or {}).values(),
    ]
    for source in sources:
        for step in source:
            marker = id(step)
            if marker in seen:
                continue
            seen.add(marker)
            yield step


def _read_channel_entries(step):
    """Yields (channel, label, iri) for every annotated channel of a read step."""
    channels = _get(step, "channel_list", []) or []
    labels = _get(step, "channel_semantics", []) or []
    iris = _get(step, "channel_semantic_iris", []) or []
    for channel, label, iri in zip_longest(channels, labels, iris, fillvalue=""):
        if not _is_set(label) and not _is_set(iri):
            continue
        yield channel, label, iri


def _set_channel_entries(step):
    """Yields (channel, label, iri, value) for every annotated channel of a set
    step."""
    channels_values = _get(step, "channels_values", {}) or {}
    channels = channels_values.get("Channels", []) or []
    labels = channels_values.get("Semantics", []) or []
    iris = channels_values.get("SemanticIRIs", []) or []
    values = channels_values.get("Values", []) or []
    for channel, label, iri, value in zip_longest(
        channels, labels, iris, values, fillvalue=""
    ):
        if not _is_set(label) and not _is_set(iri):
            continue
        yield channel, label, iri, value


def _channel_target(channel, role, step):
    """Builds the ``target`` of a channel annotation, including the data key the
    channel will have in the data whenever it can be resolved."""
    target = {
        "type": "channel",
        "name": channel,
        "role": role,
    }
    data_key = variables_handling.channel_to_data_key(channel)
    if data_key is not None:
        target["data_key"] = data_key
    target["step"] = _get(step, "full_name", "")
    return target


def _read_channel_annotations(step):
    return [
        {
            "target": _channel_target(channel, "read", step),
            "semantic": _semantic(label, iri),
        }
        for channel, label, iri in _read_channel_entries(step)
    ]


def _set_channel_annotations(step):
    annotations = []
    for channel, label, iri, value in _set_channel_entries(step):
        annotation = {
            "target": _channel_target(channel, "set", step),
            "semantic": _semantic(label, iri),
        }
        # Keep the CAMELS set expression as contextual target metadata.
        if _is_set(value):
            annotation["target"]["value_expression"] = str(value)
        annotations.append(annotation)
    return annotations


def read_step_annotations(step):
    """
    Returns the annotations of a read step keyed by the data key the channel
    will have in the data, i.e. ``{data_key: {"label": ..., "iri": ...}}``.

    This is the form needed to annotate the data itself, so channels that
    cannot be resolved to a data key are dropped rather than guessed. The
    ``semantic_mapping`` document keeps them, see `_read_channel_annotations`.

    Parameters
    ----------
    step : loop_steps.read_channels.Read_Channels
        The step whose annotations should be returned.
    """
    annotations = {}
    # Which channel provided an entry, only used to report a collision.
    sources = {}
    collisions = set()
    for channel, label, iri in _read_channel_entries(step):
        data_key = variables_handling.channel_to_data_key(channel)
        if data_key is None:
            logging.warning(
                f'Semantic mapping: channel "{channel}" of step '
                f'"{_get(step, "full_name", "")}" is unknown, its annotation is '
                f"not written to the data."
            )
            continue
        if data_key in annotations:
            if annotations[data_key]["iri"] == iri:
                continue
            # Two channels sharing a data key is possible, since ophyd joins
            # device and attribute with an underscore that may also occur
            # inside either name. Annotating one of them would be a guess.
            logging.warning(
                f'Semantic mapping: channels "{sources[data_key]}" and '
                f'"{channel}" both use the data key "{data_key}" but carry '
                f"different IRIs. Neither is written to the data."
            )
            collisions.add(data_key)
            continue
        annotations[data_key] = _semantic(label, iri)
        sources[data_key] = channel
    for data_key in collisions:
        annotations.pop(data_key, None)
    # Sorted, so that the key built from it does not depend on the order in
    # which the channels happen to be listed in the step.
    return {data_key: annotations[data_key] for data_key in sorted(annotations)}


def stream_annotation_key(step):
    """
    Returns the annotations of a read step in a hashable, order independent
    form, used to decide whether two read steps may share a data stream.

    Only the IRI is part of the key. Two labels for one IRI mean the same
    thing and must not split a stream.
    """
    return tuple(
        (data_key, semantic["iri"])
        for data_key, semantic in read_step_annotations(step).items()
    )


def _variable_annotations(protocol):
    labels = _get(protocol, "variable_semantics", {}) or {}
    iris = _get(protocol, "variable_semantic_iris", {}) or {}
    variable_names = set(labels) | set(iris)
    annotations = []
    for name in sorted(variable_names):
        label = labels.get(name, "")
        iri = iris.get(name, "")
        if not _is_set(label) and not _is_set(iri):
            continue
        annotations.append(
            {
                "target": {
                    "type": "variable",
                    "name": name,
                },
                "semantic": _semantic(label, iri),
            }
        )
    return annotations


def build_semantic_mapping(protocol, enabled=True):
    """
    Build the semantic mapping written to HDF5.

    The caller decides whether semantic mapping is enabled. This function only
    serializes labels and IRIs already stored in the CAMELS protocol; it does
    not load or validate an ontology.
    """
    if not enabled:
        return None
    annotations = []
    experiment = _experiment_annotation(protocol)
    if experiment is not None:
        annotations.append(experiment)
    for step in _iter_steps(protocol):
        if not _get(step, "is_active", True):
            continue
        step_type = _get(step, "step_type", "")
        if step_type == "Read Channels":
            annotations.extend(_read_channel_annotations(step))
        elif step_type == "Set Channels":
            annotations.extend(_set_channel_annotations(step))
    annotations.extend(_variable_annotations(protocol))
    return {
        "schema_version": "1.1",
        "source": "manual_protocol_mapping",
        "annotations": annotations,
    }


def semantic_mapping_to_json(protocol, enabled=True):
    mapping = build_semantic_mapping(protocol, enabled=enabled)
    if mapping is None:
        return None
    return json.dumps(mapping, ensure_ascii=False, indent=2)