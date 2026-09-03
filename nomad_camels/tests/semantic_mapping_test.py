"""Tests for the semantic mapping, from what a protocol stores up to the source
that is generated from it.

These do not need an instrument driver or an ontology file: the channels are put
into `variables_handling` directly, and the labels and IRIs are set on the steps
the way the config widgets would set them.
"""

import pytest

from nomad_camels.loop_steps.read_channels import Read_Channels
from nomad_camels.main_classes.measurement_channel import Measurement_Channel
from nomad_camels.utility import load_save_functions, semantic_mapping, variables_handling

IRI_CURRENT = "http://purl.org/example#ElectricCurrent"
IRI_VOLTAGE = "http://purl.org/example#Voltage"


@pytest.fixture
def demo_channels():
    """Puts two channels of one instrument into `variables_handling` and takes
    everything back afterwards, since it is global state shared with the other
    test files."""
    old_channels = dict(variables_handling.channels)
    old_channel_aliases = variables_handling.channel_aliases
    old_instrument_aliases = variables_handling.instrument_aliases
    old_sets = list(variables_handling.read_channel_sets)
    old_names = list(variables_handling.read_channel_names)
    old_active = variables_handling.semantic_mapping_active

    variables_handling.channels.clear()
    for channel in ["detX", "detY"]:
        variables_handling.channels[f"demo_{channel}"] = Measurement_Channel(
            name=f"demo.{channel}", device="demo"
        )
    variables_handling.channel_aliases = {"channel": [], "Alias": []}
    variables_handling.instrument_aliases = {"Instrument": [], "Alias": []}
    yield
    variables_handling.channels.clear()
    variables_handling.channels.update(old_channels)
    variables_handling.channel_aliases = old_channel_aliases
    variables_handling.instrument_aliases = old_instrument_aliases
    variables_handling.read_channel_sets[:] = old_sets
    variables_handling.read_channel_names[:] = old_names
    variables_handling.semantic_mapping_active = old_active


def make_read_step(name, channels, iris, labels=None, descriptions=None):
    """Builds a read step the way a loaded protocol would. The config widget
    stores an empty label whenever no IRI was selected, which is mirrored here."""
    if labels is None:
        labels = [("quantity" if iri else "") for iri in iris]
    step_info = {
        "channel_list": list(channels),
        "channel_semantics": list(labels),
        "channel_semantic_iris": list(iris),
        "skip_failed": [False] * len(channels),
        "read_variables": False,
    }
    if descriptions is not None:
        step_info["channel_semantic_descriptions"] = list(descriptions)
    step = Read_Channels(name=name, step_info=step_info)
    # `Loop_Step.__init__` builds `full_name` before the subclass sets its
    # `step_type`; loading a protocol or drawing the tree fixes that afterwards.
    step.update_full_name()
    return step


def build_sources(steps, semantic_mapping_active):
    """Generates the protocol source of `steps`, with the registry cleared the
    way `protocol_builder.build_protocol` clears it."""
    variables_handling.read_channel_sets.clear()
    variables_handling.read_channel_names.clear()
    variables_handling.semantic_mapping_active = semantic_mapping_active
    return [step.get_protocol_string(1) for step in steps]


def stream_of(source):
    """The stream expression of a generated read line."""
    return source.split("name=")[1] if "name=" in source else source.split("stream=")[1]


# ---------------------------------------------------------------- name resolution


def test_channel_to_data_key(demo_channels):
    assert variables_handling.channel_to_data_key("demo_detX") == "demo_detX"


def test_channel_to_data_key_unknown_channel(demo_channels):
    assert variables_handling.channel_to_data_key("no_such_channel") is None


def test_channel_to_data_key_channel_alias(demo_channels):
    """An alias replaces the key of the channel dictionary, the data key has to
    stay the one of the channel behind it."""
    variables_handling.channel_aliases = {"channel": ["demo_detX"], "Alias": ["current"]}
    assert variables_handling.channel_to_data_key("current") == "demo_detX"


def test_channel_to_data_key_instrument_alias(demo_channels):
    variables_handling.instrument_aliases = {"Instrument": ["demo"], "Alias": ["source"]}
    assert variables_handling.channel_to_data_key("source_detX") == "demo_detX"


def test_channel_to_data_key_undefined_alias(demo_channels):
    """An alias that is not defined anywhere gets a channel whose name carries
    no device, it has to be passed through unchanged."""
    variables_handling.channel_aliases = {"channel": [], "Alias": ["undefined"]}
    assert variables_handling.channel_to_data_key("undefined") == "undefined"


# ------------------------------------------------------------------- annotations


def test_read_step_annotations(demo_channels):
    step = make_read_step("A", ["demo_detX", "demo_detY"], [IRI_CURRENT, IRI_VOLTAGE])
    assert semantic_mapping.read_step_annotations(step) == {
        "demo_detX": {"label": "quantity", "iri": IRI_CURRENT},
        "demo_detY": {"label": "quantity", "iri": IRI_VOLTAGE},
    }


def test_read_step_annotations_includes_the_physical_quantity_description(demo_channels):
    step = make_read_step(
        "A",
        ["demo_detX"],
        [IRI_CURRENT],
        descriptions=["An electric current."],
    )
    assert semantic_mapping.read_step_annotations(step) == {
        "demo_detX": {
            "label": "quantity",
            "iri": IRI_CURRENT,
            "description": "An electric current.",
        },
    }


def test_read_step_annotations_no_description_key_when_unset(demo_channels):
    step = make_read_step("A", ["demo_detX"], [IRI_CURRENT])
    assert "description" not in semantic_mapping.read_step_annotations(step)["demo_detX"]


def test_read_step_annotations_unannotated(demo_channels):
    step = make_read_step("A", ["demo_detX"], [""])
    assert semantic_mapping.read_step_annotations(step) == {}


def test_read_step_annotations_shorter_semantics(demo_channels):
    """An older protocol may carry fewer semantics than channels."""
    step = make_read_step("A", ["demo_detX", "demo_detY"], [IRI_CURRENT])
    assert list(semantic_mapping.read_step_annotations(step)) == ["demo_detX"]


def test_read_step_annotations_label_without_iri(demo_channels):
    """The IRI identifies the meaning, a label alone does not annotate data."""
    step = make_read_step("A", ["demo_detX"], [""], labels=["quantity"])
    assert semantic_mapping.read_step_annotations(step) == {}


def test_read_step_annotations_alias(demo_channels):
    variables_handling.channel_aliases = {"channel": ["demo_detX"], "Alias": ["current"]}
    step = make_read_step("A", ["current"], [IRI_CURRENT])
    assert list(semantic_mapping.read_step_annotations(step)) == ["demo_detX"]


def test_read_step_annotations_unknown_channel_is_skipped(demo_channels):
    """A failed lookup has to produce no annotation rather than a wrong one."""
    step = make_read_step("A", ["demo_detX", "gone"], [IRI_CURRENT, IRI_VOLTAGE])
    assert list(semantic_mapping.read_step_annotations(step)) == ["demo_detX"]


def test_read_step_annotations_data_key_collision(demo_channels):
    """Two channels can share a data key, since ophyd joins device and attribute
    with an underscore that may occur inside either name. Neither may be
    annotated then."""
    variables_handling.channels["a"] = Measurement_Channel(
        name="demo_x.y", device="demo_x"
    )
    variables_handling.channels["b"] = Measurement_Channel(
        name="demo.x_y", device="demo"
    )
    step = make_read_step("A", ["a", "b"], [IRI_CURRENT, IRI_VOLTAGE])
    assert semantic_mapping.read_step_annotations(step) == {}


def test_read_step_annotations_collision_with_equal_iri(demo_channels):
    """The same meaning twice is not a conflict."""
    variables_handling.channels["a"] = Measurement_Channel(
        name="demo_x.y", device="demo_x"
    )
    variables_handling.channels["b"] = Measurement_Channel(
        name="demo.x_y", device="demo"
    )
    step = make_read_step("A", ["a", "b"], [IRI_CURRENT, IRI_CURRENT])
    assert list(semantic_mapping.read_step_annotations(step)) == ["demo_x_y"]


# ---------------------------------------------------------------- the stream key


def test_stream_annotation_key_is_order_independent(demo_channels):
    first = make_read_step("A", ["demo_detX", "demo_detY"], [IRI_CURRENT, IRI_VOLTAGE])
    second = make_read_step("B", ["demo_detY", "demo_detX"], [IRI_VOLTAGE, IRI_CURRENT])
    assert semantic_mapping.stream_annotation_key(
        first
    ) == semantic_mapping.stream_annotation_key(second)


def test_stream_annotation_key_ignores_the_label(demo_channels):
    """Two labels for one IRI mean the same thing and must not split a stream."""
    first = make_read_step("A", ["demo_detX"], [IRI_CURRENT], labels=["current"])
    second = make_read_step("B", ["demo_detX"], [IRI_CURRENT], labels=["amperage"])
    assert semantic_mapping.stream_annotation_key(
        first
    ) == semantic_mapping.stream_annotation_key(second)


def test_stream_annotation_key_differs_for_other_iri(demo_channels):
    first = make_read_step("A", ["demo_detX"], [IRI_CURRENT])
    second = make_read_step("B", ["demo_detX"], [IRI_VOLTAGE])
    assert semantic_mapping.stream_annotation_key(
        first
    ) != semantic_mapping.stream_annotation_key(second)


def test_stream_annotation_key_empty_without_annotation(demo_channels):
    step = make_read_step("A", ["demo_detX"], [""])
    assert semantic_mapping.stream_annotation_key(step) == ()


# ------------------------------------------------------------- generated source


def test_same_channels_different_iri_split_the_stream(demo_channels):
    sources = build_sources(
        [
            make_read_step("A", ["demo_detX"], [IRI_CURRENT]),
            make_read_step("B", ["demo_detX"], [IRI_VOLTAGE]),
        ],
        semantic_mapping_active=True,
    )
    assert stream_of(sources[0]) != stream_of(sources[1])
    assert len(variables_handling.read_channel_names) == 2
    assert all("semantics=" in source for source in sources)


def test_same_channels_same_iri_share_the_stream(demo_channels):
    sources = build_sources(
        [
            make_read_step("A", ["demo_detX"], [IRI_CURRENT]),
            make_read_step("B", ["demo_detX"], [IRI_CURRENT]),
        ],
        semantic_mapping_active=True,
    )
    assert stream_of(sources[0]) == stream_of(sources[1])
    assert len(variables_handling.read_channel_names) == 1


def test_source_unchanged_without_semantic_mapping(demo_channels):
    """A protocol that does not use semantic mapping has to produce exactly the
    source it produced before, whether the IRIs are stored or not."""
    steps = [
        make_read_step("A", ["demo_detX"], [IRI_CURRENT]),
        make_read_step("B", ["demo_detY"], [IRI_VOLTAGE]),
    ]
    disabled = build_sources(steps, semantic_mapping_active=False)
    assert not any("semantics=" in source for source in disabled)

    unannotated = [
        make_read_step("A", ["demo_detX"], [""]),
        make_read_step("B", ["demo_detY"], [""]),
    ]
    assert build_sources(unannotated, semantic_mapping_active=True) == disabled


def test_annotated_source_passes_the_annotation_on(demo_channels):
    source = build_sources(
        [make_read_step("A", ["demo_detX"], [IRI_CURRENT])],
        semantic_mapping_active=True,
    )[0]
    expected = f"semantics={{'demo_detX': {{'label': 'quantity', 'iri': '{IRI_CURRENT}'}}}}"
    assert expected in source


def test_split_trigger_also_passes_the_annotation_on(demo_channels):
    step = make_read_step("A", ["demo_detX"], [IRI_CURRENT])
    step.split_trigger = True
    source = build_sources([step], semantic_mapping_active=True)[0]
    assert "read_wo_trigger" in source
    assert "semantics=" in source


# -------------------------------------------------------------- mapping document


def test_mapping_document_distinguishes_the_steps(demo_channels):
    """Without the step, two read steps annotating one channel differently
    produced two indistinguishable entries."""

    class Protocol:
        experiment_ontology_class = ""
        experiment_ontology_class_iri = ""
        variable_semantics = {}
        variable_semantic_iris = {}
        loop_step_dict = {}
        loop_steps = [
            make_read_step("A", ["demo_detX"], [IRI_CURRENT]),
            make_read_step("B", ["demo_detX"], [IRI_VOLTAGE]),
        ]

    mapping = semantic_mapping.build_semantic_mapping(Protocol())
    targets = [annotation["target"] for annotation in mapping["annotations"]]
    assert [target["step"] for target in targets] == [
        "Read Channels (A)",
        "Read Channels (B)",
    ]
    # data_key is only present when it differs from the name (e.g. an alias);
    # here it doesn't, so name alone already identifies the channel.
    assert all(target["name"] == "demo_detX" for target in targets)
    assert all("data_key" not in target for target in targets)


def test_mapping_document_data_key_present_only_when_it_differs(demo_channels):
    """data_key is only included when it differs from the channel's name in
    the protocol - e.g. because of an alias - since otherwise the name alone
    already identifies the data key."""
    variables_handling.channel_aliases = {
        "channel": ["demo_detX"],
        "Alias": ["current"],
    }

    class Protocol:
        experiment_ontology_class = ""
        experiment_ontology_class_iri = ""
        variable_semantics = {}
        variable_semantic_iris = {}
        loop_step_dict = {}
        loop_steps = [make_read_step("A", ["current"], [IRI_CURRENT])]

    mapping = semantic_mapping.build_semantic_mapping(Protocol())
    target = mapping["annotations"][0]["target"]
    assert target["name"] == "current"
    assert target["data_key"] == "demo_detX"


def test_mapping_document_keeps_unresolvable_channels(demo_channels):
    """The document is documentation, so it must not lose a channel just because
    the instrument is not currently loaded. It only loses the data key."""

    class Protocol:
        experiment_ontology_class = ""
        experiment_ontology_class_iri = ""
        variable_semantics = {}
        variable_semantic_iris = {}
        loop_step_dict = {}
        loop_steps = [make_read_step("A", ["gone"], [IRI_CURRENT])]

    mapping = semantic_mapping.build_semantic_mapping(Protocol())
    target = mapping["annotations"][0]["target"]
    assert target["name"] == "gone"
    assert "data_key" not in target


def test_mapping_document_disabled(demo_channels):
    assert semantic_mapping.build_semantic_mapping(object(), enabled=False) is None


def test_mapping_document_includes_experiment_class_description(demo_channels):
    """The selected experiment class's own ontology description carries into
    the document's "measurement" annotation, same as a read channel's or a
    protocol variable's own physical quantity description."""

    class Protocol:
        experiment_ontology_class = "FooExperiment"
        experiment_ontology_class_iri = IRI_CURRENT
        experiment_ontology_class_description = "Measures the foo of a sample."
        variable_semantics = {}
        variable_semantic_iris = {}
        loop_step_dict = {}
        loop_steps = []

    mapping = semantic_mapping.build_semantic_mapping(Protocol())
    annotation = mapping["annotations"][0]
    assert annotation["target"] == {"type": "measurement"}
    assert annotation["semantic"]["description"] == "Measures the foo of a sample."


def test_mapping_document_includes_read_channel_description(demo_channels):
    """A read channel's selected physical quantity carries its own ontology
    description into the document's `semantic` entry, same as a protocol
    variable's (see `test_mapping_document_includes_variable_description`)."""

    class Protocol:
        experiment_ontology_class = ""
        experiment_ontology_class_iri = ""
        variable_semantics = {}
        variable_semantic_iris = {}
        loop_step_dict = {}
        loop_steps = [
            make_read_step(
                "A",
                ["demo_detX"],
                [IRI_CURRENT],
                descriptions=["An electric current."],
            )
        ]

    mapping = semantic_mapping.build_semantic_mapping(Protocol())
    annotation = mapping["annotations"][0]
    assert annotation["target"]["name"] == "demo_detX"
    assert annotation["semantic"]["description"] == "An electric current."


def test_mapping_document_includes_variable_description(demo_channels):
    """A protocol variable's selected physical quantity carries its own
    ontology description too, same as a read channel's (see
    `Read_Channels_Config_Sub.update_step_config`) - stored on the protocol
    as `variable_semantic_descriptions` and surfaced in the document's
    `semantic` entry."""

    class Protocol:
        experiment_ontology_class = ""
        experiment_ontology_class_iri = ""
        variable_semantics = {"annotated_var": "current"}
        variable_semantic_iris = {"annotated_var": IRI_CURRENT}
        variable_semantic_descriptions = {
            "annotated_var": "An electric current."
        }
        loop_step_dict = {}
        loop_steps = []

    mapping = semantic_mapping.build_semantic_mapping(Protocol())
    annotation = mapping["annotations"][0]
    assert annotation["target"] == {"type": "variable", "name": "annotated_var"}
    assert annotation["semantic"]["description"] == "An electric current."


# ------------------------------------------------------------------ protocol load


def test_load_protocols_dict_restores_experiment_description():
    """experiment_ontology_class_description is saved generically (it is a
    plain Measurement_Protocol attribute), so it must be restored the same
    way its siblings experiment_ontology_class/_iri already are."""
    prot_data = {
        "old_protocol": {
            "experiment_ontology_class": "FooExperiment",
            "experiment_ontology_class_iri": "http://purl.org/example#FooExperiment",
            "experiment_ontology_class_description": "Does the foo.",
        }
    }
    protocols = {}
    load_save_functions.load_protocols_dict(prot_data, protocols)
    assert (
        protocols["old_protocol"].experiment_ontology_class_description
        == "Does the foo."
    )


def test_load_protocols_dict_defaults_missing_semantic_keys():
    """A protocol saved by the pre-semantic-mapping `development` branch has
    none of these keys at all. Loading it must not crash and must leave every
    new field at its safe, disabled default - both on the protocol and on a
    Read_Channels step, which pads its own semantic lists independently."""
    prot_data = {
        "old_protocol": {
            "filename": "old_protocol",
            "variables": {},
            "loop_steps": [
                {
                    "step_type": "Read Channels",
                    "name": "Read_Channels",
                    "full_name": "Read Channels (Read_Channels)",
                    "channel_list": ["demo_detX"],
                    "skip_failed": [False],
                }
            ],
        }
    }
    protocols = {}
    load_save_functions.load_protocols_dict(prot_data, protocols)
    prot = protocols["old_protocol"]

    assert prot.semantic_mapping_enabled is False
    assert prot.experiment_ontology_class == ""
    assert prot.experiment_ontology_class_iri == ""
    assert prot.experiment_ontology_class_description == ""
    assert prot.variable_semantics == {}
    assert prot.variable_semantic_iris == {}
    assert prot.variable_semantic_descriptions == {}

    step = prot.loop_step_dict["Read Channels (Read_Channels)"]
    assert step.channel_semantics == [""]
    assert step.channel_semantic_iris == [""]
    assert step.channel_semantic_descriptions == [""]
