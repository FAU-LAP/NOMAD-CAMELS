"""Tests that a semantic annotation reaches the data file, and only the datasets
it belongs to.

These drive the RunEngine and the serializer directly with plain ophyd signals
instead of building a protocol, so that they cover the mechanism itself without
depending on an instrument driver being installed.
"""

import json

import bluesky.plan_stubs as bps
import h5py
import pytest
from bluesky.bundlers import RunBundler
from event_model import RunRouter
from ophyd import Signal

from nomad_camels.bluesky_handling import helper_functions
from nomad_camels.bluesky_handling.run_engine_overwrite import RunEngineOverwrite

IRI_CURRENT = "http://purl.org/example#ElectricCurrent"
IRI_VOLTAGE = "http://purl.org/example#Voltage"

# `_prepare_stream` and `RunEngine.RunBundler` only exist from bluesky 1.11.0,
# while the declared minimum is 1.9.0. Below that the data is written as before,
# just without the annotation.
needs_descriptor_hook = pytest.mark.skipif(
    not hasattr(RunBundler, "_prepare_stream"),
    reason="bluesky < 1.11.0 cannot annotate descriptors",
)

READ_CHANNEL_MAPPING = {
    "schema_version": "1.1",
    "source": "manual_protocol_mapping",
    "annotations": [
        {
            "target": {
                "type": "channel",
                "name": "demo_detX",
                "step": "Read Channels (Read_Channels)",
            },
            "semantic": {"label": "current", "iri": IRI_CURRENT},
        }
    ],
}


def run_and_read(tmp_path, plan, session_name):
    """Runs `plan` through the CAMELS RunEngine into an HDF5 file and returns
    the path of that file."""
    save_path = tmp_path / session_name
    engine = RunEngineOverwrite()
    router = RunRouter(
        [
            lambda name, doc: helper_functions.saving_function(
                name, doc, str(save_path), False, None, False, 0
            )
        ]
    )
    engine.subscribe(router)
    engine(plan())
    return f"{save_path}.h5"


@pytest.fixture
def detectors():
    return Signal(name="demo_detX", value=1.0), Signal(name="demo_detY", value=2.0)


@needs_descriptor_hook
def test_annotation_reaches_the_dataset(tmp_path, detectors):
    """The case the whole mechanism exists for: one signal, read twice with a
    different meaning, and once without any."""
    det_x, det_y = detectors

    def plan():
        yield from bps.open_run(md={"session_name": "annotated"})
        yield from helper_functions.trigger_and_read(
            [det_x, det_y],
            name="primary",
            semantics={"demo_detX": {"label": "current", "iri": IRI_CURRENT}},
        )
        yield from helper_functions.trigger_and_read(
            [det_x],
            name="primary||sub_stream||primary_1",
            semantics={"demo_detX": {"label": "voltage", "iri": IRI_VOLTAGE}},
        )
        yield from helper_functions.trigger_and_read(
            [det_x, det_y], name="primary||sub_stream||primary_2"
        )
        yield from bps.close_run()

    with h5py.File(run_and_read(tmp_path, plan, "annotated"), "r") as file:
        data = file["CAMELS_annotated"]["data"]
        first = data["demo_detX"]
        second = data["primary"]["primary_1"]["demo_detX"]
        third = data["primary"]["primary_2"]["demo_detX"]

        assert first.attrs["semantic_iri"] == IRI_CURRENT
        assert first.attrs["semantic_label"] == "current"
        # the same signal, so this is what a per-signal annotation could not do
        assert second.attrs["semantic_iri"] == IRI_VOLTAGE
        # the data keys of a signal are cached and shared by every stream
        # reading it, so an annotation must not leak into an unannotated read
        assert "semantic_iri" not in third.attrs
        assert "semantic_iri" not in data["demo_detY"].attrs
        # what was written before has to survive
        assert "dtype" in first.attrs and "source" in first.attrs


@needs_descriptor_hook
def test_repeated_reads_keep_one_annotated_dataset(tmp_path, detectors):
    """A read inside a loop appends to one stream, the attribute is only written
    when the dataset is created."""
    det_x, _ = detectors

    def plan():
        yield from bps.open_run(md={"session_name": "looped"})
        for _ in range(3):
            yield from helper_functions.trigger_and_read(
                [det_x],
                name="primary",
                semantics={"demo_detX": {"label": "current", "iri": IRI_CURRENT}},
            )
        yield from bps.close_run()

    with h5py.File(run_and_read(tmp_path, plan, "looped"), "r") as file:
        entry = file["CAMELS_looped"]
        data = entry["data"]
        assert len(data["time"]) == 3
        assert data["demo_detX"].attrs["semantic_iri"] == IRI_CURRENT

        # nothing to report as unresolved here (one channel, one meaning, no
        # protocol-declared mapping) - the key must not show up empty
        mapping = json.loads(entry["measurement_details"]["semantic_mapping"][()])
        assert "unresolved" not in mapping


@needs_descriptor_hook
def test_semantic_mapping_lists_the_real_paths_and_mixed_channels(tmp_path, detectors):
    """The consolidated `semantic_mapping` entry carries the protocol's
    declared annotations, enriched with the real path a channel annotation
    resolves to, plus the mixed-meaning case that only run-time knowledge of
    the actual dataset paths can produce."""
    det_x, _ = detectors

    def plan():
        yield from bps.open_run(
            md={
                "session_name": "consolidated",
                "semantic_mapping": json.dumps(READ_CHANNEL_MAPPING),
            }
        )
        yield from helper_functions.trigger_and_read(
            [det_x],
            name="primary",
            semantics={"demo_detX": {"label": "current", "iri": IRI_CURRENT}},
        )
        yield from helper_functions.trigger_and_read(
            [det_x],
            name="primary||sub_stream||primary_1",
            semantics={"demo_detX": {"label": "voltage", "iri": IRI_VOLTAGE}},
        )
        yield from bps.close_run()

    with h5py.File(run_and_read(tmp_path, plan, "consolidated"), "r") as file:
        entry = file["CAMELS_consolidated"]
        mapping = json.loads(entry["measurement_details"]["semantic_mapping"][()])

        assert mapping["schema_version"] == "2.0"

        annotations = {a["name"]: a for a in mapping["annotations"]}
        resolved = annotations["demo_detX"]
        assert resolved["type"] == "channel"
        # the declared annotation now carries the real path it resolved to,
        # and that path really carries what it claims
        assert resolved["path"] in file
        assert file[resolved["path"]].attrs["semantic_iri"] == resolved["iri"]

        # a channel read with two meanings has a merged view mixing both,
        # reported separately since no single dataset can carry both IRIs;
        # set channels never produce an "unresolved" entry anymore, since
        # Set Channels no longer offers semantic mapping at all
        unresolved_types = {entry_["type"] for entry_ in mapping["unresolved"]}
        assert unresolved_types == {"value_log"}
        value_log = mapping["unresolved"][0]
        assert value_log["data_key"] == "demo_detX"
        assert value_log["iris"] == sorted([IRI_CURRENT, IRI_VOLTAGE])


def test_unannotated_run_stays_untouched(tmp_path, detectors):
    """A protocol that does not use semantic mapping has to produce the file it
    produced before: no index, no attributes."""
    det_x, det_y = detectors

    def plan():
        yield from bps.open_run(md={"session_name": "plain"})
        yield from helper_functions.trigger_and_read([det_x, det_y], name="primary")
        yield from bps.close_run()

    with h5py.File(run_and_read(tmp_path, plan, "plain"), "r") as file:
        entry = file["CAMELS_plain"]
        assert "semantic_mapping" not in entry["measurement_details"]
        for channel in ["demo_detX", "demo_detY"]:
            assert "semantic_iri" not in entry["data"][channel].attrs
            assert "semantic_label" not in entry["data"][channel].attrs
