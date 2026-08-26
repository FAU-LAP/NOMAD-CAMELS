"""Consolidates the semantic mapping written into the HDF5 file.

Every dataset of an annotated channel carries its IRI as an attribute, written
by suitcase from the data keys of the descriptor (see
`run_engine_overwrite.SemanticRunBundler`). This serializer takes over writing
the `semantic_mapping` entry from the base `suitcase-nomad-camels-hdf5`
package - which would otherwise write it from the protocol design alone, at
run start - and instead writes one consolidated version at run stop: the same
protocol-declared annotations, each channel annotation enriched with the real
path of the dataset it resolves to and each variable annotation with every
real path it resolves to (a variable's value can be written into more than
one stream), plus a mixed-meaning `value_log` case that resolving from the
protocol alone could not know about.

It is built from what was actually written rather than only from the
protocol, so the paths and the attributes cannot drift apart. The serializer
is the only component that knows the real paths, which is why this lives
here.

Also resolves the generic "reading" stream name of the protocol's own
top-level, multi_stream plot widget to a concrete "reading_N" stream (see
`descriptor` below), since the base package's plot-to-NXdata linking looks
up `plot.stream_name` by exact match.
"""

import json
import logging

import h5py
from suitcase.nomad_camels_hdf5 import Serializer

SCHEMA_VERSION = "2.2"
IRI_ATTRIBUTE = "semantic_iri"
LABEL_ATTRIBUTE = "semantic_label"


class CAMELSSerializer(Serializer):
    """A `Serializer` that writes one consolidated semantic mapping into
    ``<entry>/measurement_details/semantic_mapping``, instead of the base
    class's design-only version."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # {dataset path: entry of the mapping}
        self._semantic_datasets = {}

    def descriptor(self, doc):
        super().descriptor(doc)
        stream_name = doc["name"].replace("||sub_stream||", "/").replace(
            "||subprotocol_stream||", "/"
        )
        if (
            "reading" not in self._stream_names
            and stream_name.startswith("reading_")
            and "_fits_readying_" not in stream_name
        ):
            # The protocol's own top-level, multi_stream plot widget is
            # tagged with the generic "reading" stream name (see
            # `builder_helper_functions.plot_creator`), never a specific
            # "reading_N" - the base writer's plot-to-NXdata linking only does
            # an exact `_stream_names` lookup, so alias it here to the first
            # of this build's own reading streams, the same one "primary"
            # used to resolve to before CAMELS stopped flattening it.
            self._stream_names["reading"] = self._stream_names[stream_name]

    def _recreate_paths(self, include_channel_links=True):
        # The base implementation walks every `_stream_names` entry and
        # creates a group for whichever isn't already a real HDF5 group name
        # - the "reading" alias from `descriptor` above is deliberately not
        # one, so it has to sit out that walk, or it would get its own bogus
        # empty group. Restored after, since `_make_stop_entry` still needs
        # it (called right after this, once per output file).
        reading_alias = self._stream_names.pop("reading", None)
        try:
            super()._recreate_paths(include_channel_links=include_channel_links)
        finally:
            if reading_alias is not None:
                self._stream_names["reading"] = reading_alias

    def _make_start_entry(self, doc):
        # Written by _write_semantic_mapping at stop instead, once the real
        # paths are known - the base class must not write its own,
        # design-only version. self._start_doc (deep-copied by the caller
        # before this runs) still keeps the original mapping for that.
        doc = dict(doc)
        doc.pop("semantic_mapping", None)
        super()._make_start_entry(doc)

    def _add_data_to_stream_group(
        self, metadata, stream_group, ep_data_array, ep_data_key
    ):
        # Only a dataset that is created here gets its attributes written, so
        # this is also the only moment its path has to be recorded.
        is_new = ep_data_key not in stream_group
        super()._add_data_to_stream_group(
            metadata, stream_group, ep_data_array, ep_data_key
        )
        if not is_new:
            return
        try:
            self._collect_semantic_dataset(metadata, stream_group, ep_data_key)
        except Exception as e:
            logging.warning(f"Could not index the semantics of {ep_data_key}: {e}")

    def _collect_semantic_dataset(self, metadata, stream_group, ep_data_key):
        """Remembers a dataset that was just created with a semantic IRI."""
        iri = (metadata or {}).get(IRI_ATTRIBUTE, "")
        if not iri or ep_data_key not in stream_group:
            return
        dataset = stream_group[ep_data_key]
        self._semantic_datasets[dataset.name] = {
            "path": dataset.name,
            "data_key": ep_data_key,
            "iri": iri,
            "label": metadata.get(LABEL_ATTRIBUTE, ""),
        }

    def _make_stop_entry(self, doc):
        # Has to happen before, the parent closes the file at the end of it.
        try:
            self._write_semantic_mapping()
        except Exception as e:
            logging.warning(f"Could not write the semantic mapping: {e}")
        super()._make_stop_entry(doc)

    def _loaded_mapping(self):
        """Returns the protocol-declared `semantic_mapping` document as a
        dict, parsing it from JSON if it is still a string, or `{}` if the
        run carries none."""
        mapping = (self._start_doc or {}).get("semantic_mapping", None)
        if not mapping:
            return {}
        if isinstance(mapping, str):
            mapping = json.loads(mapping)
        return mapping

    def _mapped_annotations(self):
        """Returns the protocol-declared annotations and their source, one
        flat dict per annotation: each channel annotation enriched with the
        single real dataset path it resolves to, if any, and each variable
        annotation with the sorted list of every real dataset path it
        resolves to, if any - a variable's value can legitimately be written
        into more than one stream, so there is no single canonical path for
        it."""
        mapping = self._loaded_mapping()
        if not mapping:
            return [], "manual_protocol_mapping"
        # The IRI is part of the key so that one data key annotated with two
        # different meanings across steps still resolves unambiguously.
        # Accumulated as a list, appended in the same order as
        # self._semantic_datasets, instead of overwritten: a channel only ever
        # has one real path per (data_key, iri), so the list's last element is
        # the same path an overwrite would have left, but a variable's
        # namespace is one shared, mutable object, so the same (data_key, iri)
        # can legitimately collect one real path per stream that read it.
        paths_by_data_key_iri = {}
        for entry in self._semantic_datasets.values():
            key = (entry["data_key"], entry["iri"])
            paths_by_data_key_iri.setdefault(key, []).append(entry["path"])
        annotations = []
        for annotation in mapping.get("annotations", []) or []:
            target = annotation.get("target", {}) or {}
            semantic = annotation.get("semantic", {}) or {}
            flat = {"type": target.get("type", "")}
            for key in ("name", "step", "data_key"):
                if key in target:
                    flat[key] = target[key]
            flat[LABEL_ATTRIBUTE] = semantic.get("label", "")
            flat[IRI_ATTRIBUTE] = semantic.get("iri", "")
            if target.get("type") in ("channel", "variable"):
                # data_key is only present when it differs from the target's
                # name (e.g. a channel alias); otherwise the name doubles as
                # the key. Variables have no alias concept, so this always
                # falls back to their name.
                data_key = target.get("data_key") or target.get("name", "")
                paths = paths_by_data_key_iri.get(
                    (data_key, flat[IRI_ATTRIBUTE]), []
                )
                if target.get("type") == "variable":
                    if paths:
                        flat["paths"] = sorted(paths)
                elif paths:
                    flat["path"] = paths[-1]
            annotations.append(flat)
        return annotations, mapping.get("source", "manual_protocol_mapping")

    def _variable_semantic_map(self):
        """Returns `{variable_name: {"label": str, "iri": str}}` for every
        protocol-declared variable annotation that carries an IRI - the IRI
        is what identifies a meaning, same rule as for channels (see
        `semantic_mapping.read_step_annotations`)."""
        mapping = self._loaded_mapping()
        result = {}
        for annotation in mapping.get("annotations", []) or []:
            target = annotation.get("target", {}) or {}
            if target.get("type") != "variable":
                continue
            name = target.get("name")
            semantic = annotation.get("semantic", {}) or {}
            iri = semantic.get("iri", "")
            if not name or not iri:
                continue
            result[name] = {"label": semantic.get("label", ""), "iri": iri}
        return result

    def _stamp_variable_semantics(self):
        """Stamps `semantic_iri`/`semantic_label` onto the HDF5 dataset of
        every annotated protocol variable.

        Unlike channels, every variable read into one `Variable_Signal`
        shares one descriptor data key and one metadata dict (see
        `variable_reading.Variable_Signal.describe`), so their per-variable
        HDF5 datasets (one nested group per signal, one dataset per
        variable, created by the base suitcase package) cannot be told apart
        at the descriptor level. This instead finds them by the "variables"
        attribute the base package already stamps onto every one of those
        datasets, and matches them by name against the protocol-declared
        annotations directly - built from what was actually written, same as
        the channel path enrichment above.
        """
        variable_semantics = self._variable_semantic_map()
        if not variable_semantics:
            return

        def visit(_name, obj):
            if not isinstance(obj, h5py.Dataset) or "variables" not in obj.attrs:
                return
            semantic = variable_semantics.get(obj.name.rsplit("/", 1)[-1])
            if semantic is None or IRI_ATTRIBUTE in obj.attrs:
                return
            obj.attrs[IRI_ATTRIBUTE] = semantic["iri"]
            obj.attrs[LABEL_ATTRIBUTE] = semantic["label"]
            self._semantic_datasets[obj.name] = {
                "path": obj.name,
                "data_key": obj.name.rsplit("/", 1)[-1],
                "iri": semantic["iri"],
                "label": semantic["label"],
            }

        self._data_entry.visititems(visit)

    def _write_semantic_mapping(self):
        """Writes the consolidated mapping into the entry currently open.

        `stop` calls `_make_stop_entry` once per file of the run, so this may
        run several times with `self._entry` bound to a different file. The
        content is the same in each of them, so writing the same mapping into
        each is correct, but it must not be written twice into one.
        """
        self._stamp_variable_semantics()
        annotations, source = self._mapped_annotations()
        mixed_value_logs = self._mixed_value_logs()
        if not annotations and not self._semantic_datasets and not mixed_value_logs:
            return
        details = self._entry["measurement_details"]
        if "semantic_mapping" in details:
            return
        mapping = {
            "schema_version": SCHEMA_VERSION,
            "source": source,
            "annotations": annotations,
        }
        if mixed_value_logs:
            mapping["mixed_value_logs"] = mixed_value_logs
        details["semantic_mapping"] = json.dumps(
            mapping, ensure_ascii=False, indent=2
        )
        details["semantic_mapping"].attrs["format"] = "application/json"
        details["semantic_mapping"].attrs["schema_version"] = SCHEMA_VERSION

    def _mixed_value_logs(self):
        """Reports channels whose merged per-channel view mixes meanings.

        A channel deliberately read with two different IRIs in different
        protocol steps ends up in two streams, each correctly annotated. Its
        combined ``value_log`` concatenates both, though, and a single HDF5
        attribute cannot represent two meanings for different parts of one
        dataset - so it carries none. This is not reported as an error, only
        so a reader of ``value_log`` knows it is looking at a mixture rather
        than assuming an unannotated channel.
        """
        iris_per_channel = {}
        for entry in self._semantic_datasets.values():
            iris_per_channel.setdefault(entry["data_key"], set()).add(entry["iri"])
        mixed = []
        for data_key, iris in sorted(iris_per_channel.items()):
            if len(iris) < 2:
                continue
            path = self._channel_paths.get(data_key, "")
            entry = {
                "data_key": data_key,
                "semantic_iris": sorted(iris),
            }
            if path:
                entry["instrument_path"] = f"/{self._entry_name}/{path}/value_log"
            mixed.append(entry)
        return mixed
