"""Tests that a physical-quantity option's ontology description shows up as a
tooltip on its combo-box item, in both places semantics options are offered:
Channels_Check_Table (used by Read_Channels) and VariableTable (protocol
variables)."""

from PySide6.QtCore import Qt

from nomad_camels.main_classes.measurement_channel import Measurement_Channel
from nomad_camels.main_classes.protocol_class import Measurement_Protocol
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table
from nomad_camels.ui_widgets.variable_table import VariableTable

IRI_VOLTAGE = "http://test.example#Voltage"
DESCRIPTION = "A potential difference between two points."


def test_channels_check_table_combo_item_has_description_tooltip(qtbot):
    channels = {"chan1": Measurement_Channel(name="dev.chan1", device="dev", output=True)}
    table = Channels_Check_Table(
        None,
        ["set", "channel", "semantics"],
        True,
        {"channel": ["chan1"], "semantics": [""], "semantic_iris": [""]},
        [],
        channels=channels,
        combo_boxes={"semantics": [("Voltage", IRI_VOLTAGE, DESCRIPTION)]},
        combo_data_keys={"semantics": "semantic_iris"},
    )
    row = table.info_dict["channel"].index("chan1")
    combo = table.tableWidget_channels.cellWidget(row, 2)
    assert combo is not None
    # index 0 is the "no selection" sentinel, index 1 is the real option
    assert combo.itemText(1) == "Voltage"
    assert combo.itemData(1, Qt.ToolTipRole) == DESCRIPTION
    # the sentinel itself carries no tooltip
    assert combo.itemData(0, Qt.ToolTipRole) is None


def test_variable_table_semantics_combo_item_has_description_tooltip(qtbot):
    protocol = Measurement_Protocol()
    table = VariableTable(protocol=protocol)
    table.get_semantic_options = lambda: [("Voltage", IRI_VOLTAGE, DESCRIPTION)]
    combo = table.make_semantics_combo("my_var")
    assert combo.itemText(1) == "Voltage"
    assert combo.itemData(1, Qt.ToolTipRole) == DESCRIPTION
    assert combo.itemData(0, Qt.ToolTipRole) is None
