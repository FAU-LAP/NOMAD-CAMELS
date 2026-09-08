"""Regression test for two historical VariableTable bugs triggered by toggling
the "Semantics" column on/off: rows silently disappearing, and the vertical/
horizontal header falling out of sync with the model. Both were fixed in
VariableTable.set_protocol() (removeRow() instead of model.clear(), and
keeping structural signals enabled during the rebuild) - this locks that in.
"""

from nomad_camels.main_classes.protocol_class import Measurement_Protocol
from nomad_camels.ui_widgets.variable_table import VariableTable

IRI_VOLTAGE = "http://test.example#Voltage"


def assert_consistent(table, expected_rows, expected_columns):
    assert table.model.rowCount() == expected_rows
    assert table.verticalHeader().count() == table.model.rowCount()
    assert table.horizontalHeader().count() == table.model.columnCount()
    assert table.model.columnCount() == expected_columns
    names = {table.model.item(row, 0).text() for row in range(table.model.rowCount())}
    assert names == {"var_a", "var_b", "var_c"}


def test_toggling_semantics_column_keeps_rows_and_headers_in_sync(qtbot):
    protocol = Measurement_Protocol()
    protocol.variables = {"var_a": "1", "var_b": "2", "var_c": "3"}
    table = VariableTable(protocol=protocol)
    qtbot.addWidget(table)

    # Baseline: no semantic options configured, so no "Semantics" column.
    assert_consistent(table, 3, 3)

    # Toggled on: an option becomes available (e.g. an experiment class with
    # physical quantities gets picked, or the checkbox is checked).
    table.get_semantic_options = lambda: [("Voltage", IRI_VOLTAGE, "")]
    table.set_protocol(protocol)
    assert_consistent(table, 3, 4)

    # Toggled off again (e.g. the checkbox is unchecked).
    table.get_semantic_options = lambda: []
    table.set_protocol(protocol)
    assert_consistent(table, 3, 3)

    # And on once more - the historical bugs were state-dependent, so a
    # single on/off pass was not enough to catch them.
    table.get_semantic_options = lambda: [("Voltage", IRI_VOLTAGE, "")]
    table.set_protocol(protocol)
    assert_consistent(table, 3, 4)
