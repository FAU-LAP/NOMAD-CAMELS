"""Consolidates the semantic mapping written into the HDF5 file.

Every dataset of an annotated channel carries its IRI as an attribute, written
by suitcase from the data keys of the descriptor (see
`run_engine_overwrite.SemanticRunBundler`). This serializer takes over writing
the `semantic_mapping` entry from the base `suitcase-nomad-camels-hdf5`
package - which would otherwise write it from the protocol design alone, at
run start - and instead writes one consolidated version at run stop: the same
protocol-declared annotations, enriched with the real path of the dataset
each channel annotation resolves to, plus a mixed-meaning `value_log` case
that resolving from the protocol alone could not know about.

It is built from what was actually written rather than only from the
protocol, so the paths and the attributes cannot drift apart. The serializer
is the only component that knows the real paths, which is why this lives
here.
"""

import json
import logging

from suitcase.nomad_camels_hdf5 import Serializer

SCHEMA_VERSION = "2.0"
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

    def _mapped_annotations(self):
        """Returns the protocol-declared annotations and their source, one
        flat dict per annotation, each channel annotation enriched with the
        real dataset path it resolves to, if any."""
        mapping = (self._start_doc or {}).get("semantic_mapping", None)
        if not mapping:
            return [], "manual_protocol_mapping"
        if isinstance(mapping, str):
            mapping = json.loads(mapping)
        # The IRI is part of the key so that one data key annotated with two
        # different meanings across steps still resolves unambiguously.
        paths_by_data_key_iri = {
            (entry["data_key"], entry["iri"]): entry["path"]
            for entry in self._semantic_datasets.values()
        }
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
            if target.get("type") == "channel":
                # data_key is only present when it differs from the channel's
                # name (e.g. an alias); otherwise the name doubles as the key.
                data_key = target.get("data_key") or target.get("name", "")
                path = paths_by_data_key_iri.get((data_key, flat[IRI_ATTRIBUTE]))
                if path:
                    flat["path"] = path
            annotations.append(flat)
        return annotations, mapping.get("source", "manual_protocol_mapping")

    def _write_semantic_mapping(self):
        """Writes the consolidated mapping into the entry currently open.

        `stop` calls `_make_stop_entry` once per file of the run, so this may
        run several times with `self._entry` bound to a different file. The
        content is the same in each of them, so writing the same mapping into
        each is correct, but it must not be written twice into one.
        """
        annotations, source = self._mapped_annotations()
        unresolved = self._mixed_value_logs()
        if not annotations and not self._semantic_datasets and not unresolved:
            return
        details = self._entry["measurement_details"]
        if "semantic_mapping" in details:
            return
        mapping = {
            "schema_version": SCHEMA_VERSION,
            "source": source,
            "annotations": annotations,
        }
        if unresolved:
            mapping["unresolved"] = unresolved
        details["semantic_mapping"] = json.dumps(
            mapping, ensure_ascii=False, indent=2
        )
        details["semantic_mapping"].attrs["format"] = "application/json"
        details["semantic_mapping"].attrs["schema_version"] = SCHEMA_VERSION

    def _mixed_value_logs(self):
        """Reports channels whose merged per-channel view mixes meanings.

        A channel read with two different IRIs ends up in two streams, but its
        ``value_log`` concatenates all of them and carries no annotation. A
        reader using that view has to know it is looking at a mixture.
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
                "type": "value_log",
                "data_key": data_key,
                "semantic_iris": sorted(iris),
            }
            if path:
                entry["instrument_path"] = f"/{self._entry_name}/{path}/value_log"
            mixed.append(entry)
        return mixed
