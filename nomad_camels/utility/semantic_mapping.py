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
    semantic = _semantic(label, iri)
    description = _get(protocol, "experiment_ontology_class_description", "")
    if _is_set(description):
        semantic["description"] = description
    return {
        "target": {
            "type": "measurement",
        },
        "semantic": semantic,
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
    """Yields (channel, label, iri, description) for every annotated channel
    of a read step. ``description`` is the selected physical quantity's own
    ontology description (rdfs:comment), captured when it was selected."""
    channels = _get(step, "channel_list", []) or []
    labels = _get(step, "channel_semantics", []) or []
    iris = _get(step, "channel_semantic_iris", []) or []
    descriptions = _get(step, "channel_semantic_descriptions", []) or []
    for channel, label, iri, description in zip_longest(
        channels, labels, iris, descriptions, fillvalue=""
    ):
        if not _is_set(label) and not _is_set(iri):
            continue
        yield channel, label, iri, description


def _channel_target(channel, step):
    """Builds the ``target`` of a channel annotation, including the data key
    the channel will have in the data whenever it can be resolved and differs
    from the channel's name in the protocol (e.g. because of an alias)."""
    target = {
        "type": "channel",
        "name": channel,
    }
    data_key = variables_handling.channel_to_data_key(channel)
    if data_key is not None and data_key != channel:
        target["data_key"] = data_key
    target["step"] = _get(step, "full_name", "")
    return target


def _read_channel_annotations(step):
    annotations = []
    for channel, label, iri, description in _read_channel_entries(step):
        semantic = _semantic(label, iri)
        if _is_set(description):
            # The selected physical quantity's own ontology description,
            # captured at selection time - same rule as a variable's
            # (see `_variable_annotations`).
            semantic["description"] = description
        annotations.append(
            {
                "target": _channel_target(channel, step),
                "semantic": semantic,
            }
        )
    return annotations


def read_step_annotations(step):
    """
    Returns the annotations of a read step keyed by the data key the channel
    will have in the data, i.e.
    ``{data_key: {"label": ..., "iri": ..., "description": ...}}``.

    This is the form needed to annotate the data itself, so channels that
    cannot be resolved to a data key are dropped rather than guessed, and so
    are channels without an IRI, since the IRI is what identifies a meaning.
    The ``semantic_mapping`` document keeps both, see
    `_read_channel_annotations`.

    Parameters
    ----------
    step : loop_steps.read_channels.Read_Channels
        The step whose annotations should be returned.
    """
    annotations = {}
    # Which channel provided an entry, only used to report a collision.
    sources = {}
    collisions = set()
    for channel, label, iri, description in _read_channel_entries(step):
        if not _is_set(iri):
            # A label without an IRI cannot come from the GUI, the table stores
            # an empty label whenever no IRI was selected. Splitting a stream
            # over a label alone would gain nothing.
            continue
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
        if _is_set(description):
            annotations[data_key]["description"] = description
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
    descriptions = _get(protocol, "variable_semantic_descriptions", {}) or {}
    variable_names = set(labels) | set(iris)
    annotations = []
    for name in sorted(variable_names):
        label = labels.get(name, "")
        iri = iris.get(name, "")
        if not _is_set(label) and not _is_set(iri):
            continue
        semantic = _semantic(label, iri)
        description = descriptions.get(name, "")
        if _is_set(description):
            # The selected physical quantity's own ontology description,
            # captured at selection time - same rule as a read channel's
            # (see `_read_channel_entries`).
            semantic["description"] = description
        annotations.append(
            {
                "target": {
                    "type": "variable",
                    "name": name,
                },
                "semantic": semantic,
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
    annotations.extend(_variable_annotations(protocol))
    return {
        "schema_version": "1.0",
        "source": "manual_protocol_mapping",
        "annotations": annotations,
    }


def semantic_mapping_to_json(protocol, enabled=True):
    mapping = build_semantic_mapping(protocol, enabled=enabled)
    if mapping is None:
        return None
    return json.dumps(mapping, ensure_ascii=False, indent=2)