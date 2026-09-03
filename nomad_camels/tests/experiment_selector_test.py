"""Tests for the experiment-class selector in General_Protocol_Settings
(protocol_class.py): the selected class's description is stored (needed for
the "data" group's semantic_description HDF5 attribute), but deliberately not
shown as a tooltip on the selector itself - that's reserved for
physical-quantity options instead (see physical_quantity_tooltip_test.py).

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


def test_build_experiment_submenus_does_not_enable_tooltips(qtbot):
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
    assert menu.actions()[0].text() == "FooExperiment"
    # Qt only ever shows an action's tooltip in a menu if this is True; it's
    # left at its default (False) here, so no tooltip is displayed at all.
    assert menu.toolTipsVisible() is False


def test_set_experiment_class_stores_description_without_setting_a_tooltip(qtbot):
    settings = _StubSettings()
    settings._set_experiment_class("FooExperiment", "http://test.example#Foo", "Does the foo.")
    assert settings.protocol.experiment_ontology_class == "FooExperiment"
    assert settings.protocol.experiment_ontology_class_iri == "http://test.example#Foo"
    assert settings.protocol.experiment_ontology_class_description == "Does the foo."
    # the button's tooltip is untouched, whatever it was before selection
    assert settings.experiment_menu_button.toolTip() == ""


def test_update_experiment_button_text_does_not_touch_the_tooltip(qtbot):
    settings = _StubSettings()
    settings.experiment_menu_button.setToolTip("something set elsewhere")
    settings._update_experiment_button_text()
    assert settings.experiment_menu_button.toolTip() == "something set elsewhere"
