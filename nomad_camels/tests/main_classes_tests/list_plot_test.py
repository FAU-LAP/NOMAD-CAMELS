import pytest
from PySide6.QtWidgets import QApplication, QTableWidget, QWidget
from PySide6.QtTest import QSignalSpy

from nomad_camels.main_classes.list_plot import (
    Values_List_Plot,
    Live_List,
    Teleporter,
    handle_teleport,
)


@pytest.fixture(scope="module")
def app():
    """Fixture for creating a Qt application."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def value_list():
    return ["value1", "value2", "value3"]


@pytest.fixture
def table():
    return QTableWidget()


@pytest.fixture
def live_list(value_list, table):
    return Live_List(value_list, table)


def test_values_list_plot_initialization(app, value_list):
    widget = Values_List_Plot(value_list)
    assert isinstance(widget, QWidget)
    assert widget.windowTitle() == "value1 ..."
    assert widget.table.rowCount() == len(value_list)


def test_values_list_plot_show_again(app, value_list, qtbot):
    widget = Values_List_Plot(value_list)
    widget.hide()
    spy = QSignalSpy(widget.reopened)
    widget.show_again()
    assert widget.isVisible()
    assert spy.count() == 1


def test_live_list_initialization(live_list, value_list):
    assert isinstance(live_list, Live_List)
    assert live_list.value_list == value_list
    assert live_list.table.rowCount() == len(value_list)
    assert live_list.table.columnCount() == 2


def test_live_list_event_handling(live_list, qtbot):
    doc = {
        "descriptor": "test_descriptor",
        "data": {"value1": 1.23, "value2": 4.56, "value3": 7.89},
        "time": 1234567890.0,
    }
    live_list.desc = "test_descriptor"
    live_list.event(doc)
    for i, val in enumerate(live_list.value_list):
        assert live_list.val_items[i].text() == f"{doc['data'][val]:7e}"


def test_live_list_add_to_table(live_list):
    live_list.add_to_table("new_value")
    assert live_list.table.rowCount() == len(live_list.value_list) + 1
    assert live_list.table.item(len(live_list.value_list), 0).text() == "new_value"


def test_live_list_descriptor(live_list):
    doc = {"name": "primary", "uid": "test_uid"}
    live_list.descriptor(doc)
    assert live_list.desc == "test_uid"


def test_live_list_start(live_list):
    doc = {"time": 1234567890.0}
    live_list.start(doc)
    assert live_list.epoch_offset == doc["time"]


def test_teleporter():
    teleporter = Teleporter()
    spy = QSignalSpy(teleporter.name_doc_escape)
    teleporter.name_doc_escape.emit("test_name", {}, None)
    assert spy.count() == 1


def test_handle_teleport():
    class MockObj:
        def __call__(self, name, doc, escape):
            self.name = name
            self.doc = doc
            self.escape = escape

    mock_obj = MockObj()
    handle_teleport("test_name", {}, mock_obj)
    assert mock_obj.name == "test_name"
    assert mock_obj.doc == {}
    assert mock_obj.escape


def test_live_list_call(live_list, qtbot):
    doc = {
        "descriptor": "test_descriptor",
        "data": {"value1": 1.23, "value2": 4.56, "value3": 7.89},
        "time": 1234567890.0,
    }
    live_list.desc = "test_descriptor"
    spy = QSignalSpy(live_list.new_data)
    live_list.__call__("event", doc)
    assert spy.count() == 1
