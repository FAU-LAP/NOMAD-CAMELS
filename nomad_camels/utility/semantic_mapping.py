import json
from itertools import zip_longest


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


def _read_channel_annotations(step):
    channels = _get(step, "channel_list", []) or []
    labels = _get(step, "channel_semantics", []) or []
    iris = _get(step, "channel_semantic_iris", []) or []
    annotations = []
    for channel, label, iri in zip_longest(channels, labels, iris, fillvalue=""):
        if not _is_set(label) and not _is_set(iri):
            continue
        annotations.append(
            {
                "target": {
                    "type": "channel",
                    "name": channel,
                    "role": "read",
                },
                "semantic": _semantic(label, iri),
            }
        )
    return annotations


def _set_channel_annotations(step):
    channels_values = _get(step, "channels_values", {}) or {}
    channels = channels_values.get("Channels", []) or []
    labels = channels_values.get("Semantics", []) or []
    iris = channels_values.get("SemanticIRIs", []) or []
    values = channels_values.get("Values", []) or []
    annotations = []
    for channel, label, iri, value in zip_longest(
        channels, labels, iris, values, fillvalue=""
    ):
        if not _is_set(label) and not _is_set(iri):
            continue
        annotation = {
            "target": {
                "type": "channel",
                "name": channel,
                "role": "set",
            },
            "semantic": _semantic(label, iri),
        }
        # Keep the CAMELS set expression as contextual target metadata.
        if _is_set(value):
            annotation["target"]["value_expression"] = str(value)
        annotations.append(annotation)
    return annotations


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
        "schema_version": "1.0",
        "source": "manual_protocol_mapping",
        "annotations": annotations,
    }


def semantic_mapping_to_json(protocol, enabled=True):
    mapping = build_semantic_mapping(protocol, enabled=enabled)
    if mapping is None:
        return None
    return json.dumps(mapping, ensure_ascii=False, indent=2)