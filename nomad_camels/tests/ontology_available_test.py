"""Tests the real, preference-driven `semantic_mapping_available()` path end
to end through a real `General_Protocol_Settings` widget.

Every other test file (ontology_helper_test.py, semantic_mapping_test.py,
physical_quantity_tooltip_test.py, experiment_selector_test.py) deliberately
bypasses this path via monkeypatching or a stand-in, specifically because it
needs "a configured, loadable ontology to reach the experiment menu at all"
(see experiment_selector_test.py's docstring) - so the real GUI-enablement
gate (checkbox becomes usable, menu gets built, "Semantics" column appears)
has had no coverage of its "available" branch anywhere.

Building the ontology through owlready2's global default_world and then
letting `ontology_helper.load_local_ontology` load the same file a second
time in that world produces duplicated/aliased classes (owlready2 indexes a
loaded ontology by its own declared IRI, not by the file path used to load
it - confirmed by a throwaway repro, not part of this suite). Building it in
an isolated `owlready2.World()` instead avoids that entirely. So
`load_local_ontology` is monkeypatched to hand back that already-built
in-memory object rather than re-parsing the file - but the file itself is
real, on disk, and the preference genuinely points at it, so every check
downstream of the load (path existence, suffix, checkbox enabling, menu
building, column toggling) still runs for real, unpatched.
"""

from owlready2 import ObjectProperty, Thing, World

from nomad_camels.main_classes.protocol_class import (
    General_Protocol_Settings,
    Measurement_Protocol,
)
from nomad_camels.utility import ontology_helper, variables_handling

DESCRIPTION = "A potential difference between two points."


def build_ontology(tmp_path):
    """Builds a minimal, real ontology (LAPExperiment -> FooExperiment, with a
    relatesToQuantity restriction to Voltage) in an isolated World, saves it
    to a real file, and returns (ontology, file_path)."""
    world = World()
    onto = world.get_ontology("http://test.example/lap_et_available_test.owl")
    with onto:

        class LAPExperiment(Thing):
            pass

        class relatesToQuantity(ObjectProperty):
            pass

        class Voltage(Thing):
            comment = [DESCRIPTION]

        class FooExperiment(LAPExperiment):
            comment = ["Does the foo."]
            equivalent_to = [relatesToQuantity.some(Voltage)]

    path = tmp_path / "lap_et_available_test.owl"
    onto.save(file=str(path))
    return onto, path


def test_real_ontology_path_enables_checkbox_menu_and_semantics_column(
    qtbot, tmp_path, monkeypatch
):
    onto, path = build_ontology(tmp_path)
    monkeypatch.setattr(ontology_helper, "load_local_ontology", lambda *a, **k: onto)
    monkeypatch.setitem(
        variables_handling.preferences,
        "experimental_techniques_ontology_path",
        str(path),
    )

    # Sanity check: the real, preference-driven path itself reports
    # available - no monkeypatching of this function, unlike every other
    # test file.
    assert ontology_helper.semantic_mapping_available() is True

    protocol = Measurement_Protocol()
    settings = General_Protocol_Settings(protocol=protocol)
    qtbot.addWidget(settings)

    assert settings.checkBox_semantic_mapping.isEnabled() is True
    assert protocol.semantic_mapping_enabled is False  # starts unchecked

    menu = settings.experiment_menu_button._menu
    assert menu is not None
    assert [action.text() for action in menu.actions()] == ["FooExperiment"]
    # Not enabled yet: semantic mapping itself is still off.
    assert settings.experiment_menu_button.isEnabled() is False

    settings.checkBox_semantic_mapping.setChecked(True)
    assert protocol.semantic_mapping_enabled is True
    assert settings.experiment_menu_button.isEnabled() is True

    assert settings.variable_table.semantic_column_enabled() is False
    settings._set_experiment_class(
        "FooExperiment", onto["FooExperiment"].iri, "Does the foo."
    )
    assert settings.variable_table.semantic_column_enabled() is True
    assert "Semantics" in settings.variable_table.get_table_headers()
