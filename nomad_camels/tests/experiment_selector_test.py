"""Tests for the experiment-class selector's tooltip wiring in
General_Protocol_Settings (protocol_class.py).

These call the relevant methods against a minimal stand-in instead of a real
General_Protocol_Settings (which needs Ui_Protocol_Settings.setupUi() and a
configured, loadable ontology to reach the experiment menu at all) - the
methods under test only ever touch protocol/_selected_experiment_class*/
experiment_menu_button, so a stand-in carrying just those is enough.
"""

from PySide6.QtWidgets import QMenu

from nomad_camels.main_classes.protocol_class import (
    ExperimentMenuComboBox,
    General_Protocol_Settings,
)

DEFAULT_TOOLTIP = "Select an experiment class from the ontology hierarchy."


class _StubProtocol:
    def __init__(self):
        self.experiment_ontology_class = ""
        self.experiment_ontology_class_iri = ""
        self.experiment_ontology_class_description = ""


class _StubSettings:
    """Minimal stand-in carrying only what the methods under test touch."""

    def __init__(self):
        self.protocol = _StubProtocol()
        self._selected_experiment_class = ""
        self._selected_experiment_class_iri = ""
        self._selected_experiment_class_description = ""
        self.experiment_menu_button = ExperimentMenuComboBox()
        # _set_experiment_class checks hasattr(self.variable_table, ...);
        # None keeps that check False without needing a real VariableTable.
        self.variable_table = None

    _build_experiment_submenus = General_Protocol_Settings._build_experiment_submenus
    _set_experiment_class = General_Protocol_Settings._set_experiment_class
    _update_experiment_button_text = General_Protocol_Settings._update_experiment_button_text


def test_build_experiment_submenus_sets_action_tooltip(qtbot):
    settings = _StubSettings()
    menu = QMenu()
    nodes = [
        {
            "name": "FooExperiment",
            "iri": "http://test.example#Foo",
            "description": "Does the foo.",
            "children": [],
        }
    ]
    settings._build_experiment_submenus(menu, nodes)
    actions = menu.actions()
    assert len(actions) == 1
    assert actions[0].toolTip() == "Does the foo."


def test_build_experiment_submenus_handles_missing_description(qtbot):
    """Qt falls back an action's tooltip to its text when none is set
    explicitly (an empty string counts as "none") - not blank, but harmless."""
    settings = _StubSettings()
    menu = QMenu()
    nodes = [{"name": "FooExperiment", "iri": "http://test.example#Foo", "children": []}]
    settings._build_experiment_submenus(menu, nodes)
    assert menu.actions()[0].toolTip() == "FooExperiment"


def test_set_experiment_class_updates_button_tooltip_and_protocol(qtbot):
    settings = _StubSettings()
    settings._set_experiment_class("FooExperiment", "http://test.example#Foo", "Does the foo.")
    assert settings.experiment_menu_button.toolTip() == "Does the foo."
    assert settings.protocol.experiment_ontology_class == "FooExperiment"
    assert settings.protocol.experiment_ontology_class_iri == "http://test.example#Foo"
    assert settings.protocol.experiment_ontology_class_description == "Does the foo."


def test_update_experiment_button_text_falls_back_to_default_tooltip(qtbot):
    settings = _StubSettings()
    settings._update_experiment_button_text()
    assert settings.experiment_menu_button.toolTip() == DEFAULT_TOOLTIP
