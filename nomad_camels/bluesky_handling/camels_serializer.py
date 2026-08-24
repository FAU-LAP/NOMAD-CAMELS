"""Adds the semantic index to the HDF5 file written by
`suitcase-nomad-camels-hdf5`.

Every dataset of an annotated channel carries its IRI as an attribute, written
by suitcase from the data keys of the descriptor (see
`run_engine_overwrite.SemanticRunBundler`). The index collects those attributes
into one place per run entry, together with the full path of the dataset they
sit on, so that a reader does not have to walk the file to find them.

It is built from what was actually written rather than from the protocol, so
the index and the attributes cannot drift apart. The serializer is the only
component that knows the real paths, which is why this lives here.
"""

import json
import logging

from suitcase.nomad_camels_hdf5 import Serializer

SCHEMA_VERSION = "1.0"
IRI_ATTRIBUTE = "semantic_iri"
LABEL_ATTRIBUTE = "semantic_label"


class CAMELSSerializer(Serializer):
    """A `Serializer` that additionally writes a semantic index into
    ``<entry>/measurement_details/semantic_index``."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # {dataset path: entry of the index}
        self._semantic_datasets = {}

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
            self._write_semantic_index()
        except Exception as e:
            logging.warning(f"Could not write the semantic index: {e}")
        super()._make_stop_entry(doc)

    def _write_semantic_index(self):
        """Writes the index into the entry currently open.

        `stop` calls `_make_stop_entry` once per file of the run, so this may
        run several times with `self._entry` bound to a different file. The
        paths are the same in each of them, so writing the same index into each
        is correct, but it must not be written twice into one.
        """
        unresolved = self._unresolved_annotations()
        if not self._semantic_datasets and not unresolved:
            return
        details = self._entry["measurement_details"]
        if "semantic_index" in details:
            return
        index = {
            "schema_version": SCHEMA_VERSION,
            "entry": self._entry_name,
            "attribute_names": {"iri": IRI_ATTRIBUTE, "label": LABEL_ATTRIBUTE},
            "datasets": [
                self._semantic_datasets[path]
                for path in sorted(self._semantic_datasets)
            ],
            "unresolved": unresolved,
        }
        details["semantic_index"] = json.dumps(index, ensure_ascii=False, indent=2)
        details["semantic_index"].attrs["format"] = "application/json"
        details["semantic_index"].attrs["schema_version"] = SCHEMA_VERSION

    def _unresolved_annotations(self):
        """Returns the annotations that exist but do not sit on a dataset.

        Set channels are the main case: they are never read, so they have no
        dataset. Their only per-channel object in the file is the actuator
        below ``instruments``, which is per channel and not per step, so
        annotating it would restore exactly the ambiguity this whole mechanism
        avoids. They are listed here instead, pointing at that actuator.
        """
        unresolved = []
        unresolved.extend(self._unresolved_set_channels())
        unresolved.extend(self._mixed_value_logs())
        return unresolved

    def _unresolved_set_channels(self):
        mapping = (self._start_doc or {}).get("semantic_mapping", None)
        if not mapping:
            return []
        if isinstance(mapping, str):
            mapping = json.loads(mapping)
        unresolved = []
        for annotation in mapping.get("annotations", []) or []:
            target = annotation.get("target", {}) or {}
            if target.get("role", "") != "set":
                continue
            semantic = annotation.get("semantic", {}) or {}
            entry = {
                "type": "set",
                "channel": target.get("name", ""),
                "step": target.get("step", ""),
                "iri": semantic.get("iri", ""),
                "label": semantic.get("label", ""),
            }
            if "value_expression" in target:
                entry["value_expression"] = target["value_expression"]
            data_key = target.get("data_key", "")
            if data_key:
                entry["data_key"] = data_key
                path = self._channel_paths.get(data_key, "")
                if path:
                    entry["instrument_path"] = f"/{self._entry_name}/{path}"
            unresolved.append(entry)
        return unresolved

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
                "iris": sorted(iris),
            }
            if path:
                entry["instrument_path"] = f"/{self._entry_name}/{path}/value_log"
            mixed.append(entry)
        return mixed
