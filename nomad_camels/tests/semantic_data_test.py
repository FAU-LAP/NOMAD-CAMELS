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

from nomad_camels.bluesky_handling import helper_functions, variable_reading
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
def test_physical_quantity_description_reaches_the_dataset(tmp_path, detectors):
    """The selected physical quantity's own ontology description (distinct
    from the whole-experiment description) is stamped onto its channel's
    dataset, next to semantic_iri/semantic_label."""
    det_x, det_y = detectors

    def plan():
        yield from bps.open_run(md={"session_name": "quantity_described"})
        yield from helper_functions.trigger_and_read(
            [det_x, det_y],
            name="primary",
            semantics={
                "demo_detX": {
                    "label": "current",
                    "iri": IRI_CURRENT,
                    "description": "An electric current.",
                }
            },
        )
        yield from bps.close_run()

    with h5py.File(
        run_and_read(tmp_path, plan, "quantity_described"), "r"
    ) as file:
        data = file["CAMELS_quantity_described"]["data"]
        assert data["demo_detX"].attrs["semantic_description"] == "An electric current."
        # demo_detY has no semantics at all, so it gets nothing either
        assert "semantic_description" not in data["demo_detY"].attrs


@needs_descriptor_hook
def test_annotation_without_description_omits_the_attribute(tmp_path, detectors):
    det_x, _ = detectors

    def plan():
        yield from bps.open_run(md={"session_name": "no_quantity_description"})
        yield from helper_functions.trigger_and_read(
            [det_x],
            name="primary",
            semantics={"demo_detX": {"label": "current", "iri": IRI_CURRENT}},
        )
        yield from bps.close_run()

    with h5py.File(
        run_and_read(tmp_path, plan, "no_quantity_description"), "r"
    ) as file:
        data = file["CAMELS_no_quantity_description"]["data"]
        assert "semantic_iri" in data["demo_detX"].attrs
        assert "semantic_description" not in data["demo_detX"].attrs


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

        # nothing to report here (one channel, one meaning, no
        # protocol-declared mapping) - the key must not show up empty
        mapping = json.loads(entry["measurement_details"]["semantic_mapping"][()])
        assert "mixed_value_logs" not in mapping


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

        assert mapping["schema_version"] == "2.2"

        annotations = {a["name"]: a for a in mapping["annotations"]}
        resolved = annotations["demo_detX"]
        assert resolved["type"] == "channel"
        # the declared annotation now carries the real path it resolved to,
        # and that path really carries what it claims
        assert resolved["path"] in file
        assert (
            file[resolved["path"]].attrs["semantic_iri"] == resolved["semantic_iri"]
        )

        # a channel deliberately read with two meanings has a merged
        # value_log view mixing both; reported separately since no single
        # dataset attribute can carry both IRIs
        channels = {entry_["data_key"]: entry_ for entry_ in mapping["mixed_value_logs"]}
        value_log = channels["demo_detX"]
        assert value_log["semantic_iris"] == sorted([IRI_CURRENT, IRI_VOLTAGE])
        assert "type" not in value_log


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


@needs_descriptor_hook
def test_experiment_description_reaches_every_dataset(tmp_path, detectors):
    """The selected experiment class's description is stamped onto every read
    channel's dataset, not just ones that also carry their own semantic_iri/
    semantic_label annotation."""
    det_x, det_y = detectors

    def plan():
        yield from bps.open_run(md={"session_name": "described"})
        helper_functions.set_experiment_description("Measures the foo of a sample.")
        yield from helper_functions.trigger_and_read(
            [det_x, det_y],
            name="primary",
            semantics={"demo_detX": {"label": "current", "iri": IRI_CURRENT}},
        )
        yield from bps.close_run()

    with h5py.File(run_and_read(tmp_path, plan, "described"), "r") as file:
        data = file["CAMELS_described"]["data"]
        # both the annotated and the unannotated channel carry it
        assert data["demo_detX"].attrs["experiment_description"] == (
            "Measures the foo of a sample."
        )
        assert data["demo_detY"].attrs["experiment_description"] == (
            "Measures the foo of a sample."
        )
        # its own annotation is unaffected
        assert data["demo_detX"].attrs["semantic_iri"] == IRI_CURRENT
        assert "semantic_iri" not in data["demo_detY"].attrs


def test_variable_annotation_reaches_its_own_dataset(tmp_path):
    """A protocol variable's own nested HDF5 dataset (one dataset per variable
    inside the shared Variable_Signal's group) carries semantic_iri/
    semantic_label, without leaking onto an unannotated variable read through
    that same signal. This does not go through the descriptor hook at all
    (unlike channels), since every variable shares one descriptor data key -
    it is stamped from the consolidated semantic_mapping document at stop
    time instead, so it works independently of `needs_descriptor_hook`."""
    var_signal = variable_reading.Variable_Signal(
        name="myprotocol_variable_signal",
        variables_dict={"annotated_var": 1, "plain_var": 2},
    )
    mapping = {
        "schema_version": "1.1",
        "source": "manual_protocol_mapping",
        "annotations": [
            {
                "target": {"type": "variable", "name": "annotated_var"},
                "semantic": {"label": "current", "iri": IRI_CURRENT},
            }
        ],
    }

    def plan():
        yield from bps.open_run(
            md={
                "session_name": "variable_annotated",
                "semantic_mapping": json.dumps(mapping),
            }
        )
        yield from helper_functions.trigger_and_read([var_signal], name="primary")
        yield from bps.close_run()

    with h5py.File(
        run_and_read(tmp_path, plan, "variable_annotated"), "r"
    ) as file:
        entry = file["CAMELS_variable_annotated"]
        data = entry["data"]["myprotocol_variable_signal"]
        assert data["annotated_var"].attrs["semantic_iri"] == IRI_CURRENT
        assert data["annotated_var"].attrs["semantic_label"] == "current"
        assert "semantic_iri" not in data["plain_var"].attrs

        mapping_out = json.loads(entry["measurement_details"]["semantic_mapping"][()])
        resolved = next(
            a for a in mapping_out["annotations"] if a["name"] == "annotated_var"
        )
        assert resolved["type"] == "variable"
        # the declared annotation now carries every real path it resolved
        # to, plural - the singular key is gone entirely for variables
        assert "path" not in resolved
        assert resolved["paths"] == [data["annotated_var"].name]
        assert resolved["paths"][0] in file
        assert file[resolved["paths"][0]].attrs["semantic_iri"] == IRI_CURRENT


def test_variable_read_into_two_streams_lists_both_paths(tmp_path):
    """A protocol variable backed by one shared, mutable namespace can
    legitimately be read into more than one stream (e.g. once per
    `reading_N`), each a distinct, real snapshot of its value at that point
    in the run - so its annotation must list every real path, not silently
    keep just one of them."""
    var_signal = variable_reading.Variable_Signal(
        name="myprotocol_variable_signal",
        variables_dict={"annotated_var": 1},
    )
    mapping = {
        "schema_version": "1.1",
        "source": "manual_protocol_mapping",
        "annotations": [
            {
                "target": {"type": "variable", "name": "annotated_var"},
                "semantic": {"label": "current", "iri": IRI_CURRENT},
            }
        ],
    }

    def plan():
        yield from bps.open_run(
            md={
                "session_name": "variable_multi_stream",
                "semantic_mapping": json.dumps(mapping),
            }
        )
        yield from helper_functions.trigger_and_read([var_signal], name="primary")
        yield from helper_functions.trigger_and_read(
            [var_signal], name="primary||sub_stream||primary_1"
        )
        yield from bps.close_run()

    with h5py.File(
        run_and_read(tmp_path, plan, "variable_multi_stream"), "r"
    ) as file:
        entry = file["CAMELS_variable_multi_stream"]
        data = entry["data"]
        first = data["myprotocol_variable_signal"]["annotated_var"]
        second = data["primary"]["primary_1"]["myprotocol_variable_signal"][
            "annotated_var"
        ]

        mapping_out = json.loads(entry["measurement_details"]["semantic_mapping"][()])
        resolved = next(
            a for a in mapping_out["annotations"] if a["name"] == "annotated_var"
        )
        assert resolved["type"] == "variable"
        assert "path" not in resolved
        assert resolved["paths"] == sorted([first.name, second.name])
        for path in resolved["paths"]:
            assert path in file
            assert file[path].attrs["semantic_iri"] == IRI_CURRENT


def test_experiment_description_does_not_leak_into_the_next_run(tmp_path, detectors):
    """A run that never sets a description must not see the previous run's."""
    det_x, det_y = detectors

    def described_plan():
        yield from bps.open_run(md={"session_name": "described2"})
        helper_functions.set_experiment_description("Measures the foo of a sample.")
        yield from helper_functions.trigger_and_read([det_x, det_y], name="primary")
        yield from bps.close_run()

    def plain_plan():
        yield from bps.open_run(md={"session_name": "plain2"})
        yield from helper_functions.trigger_and_read([det_x, det_y], name="primary")
        yield from bps.close_run()

    run_and_read(tmp_path, described_plan, "described2")
    with h5py.File(run_and_read(tmp_path, plain_plan, "plain2"), "r") as file:
        data = file["CAMELS_plain2"]["data"]
        assert "experiment_description" not in data["demo_detX"].attrs
        assert "experiment_description" not in data["demo_detY"].attrs
