import pytest
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QApplication

from nomad_camels.main_classes.loop_step import (
    Loop_Step,
    Loop_Step_Container,
    Loop_Step_Config,
    Loop_Step_Name_Widget,
)


# Initialize the Qt Application for testing


@pytest.fixture(scope="module")
def app():
    """Fixture for creating a QApplication instance"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_loop_step_init():
    step = Loop_Step(
        name="Test Step",
        step_info={"description": "Test description", "is_active": True},
    )
    assert step.name == "Test Step"
    assert step.description == "Test description"
    assert step.is_active is True
    assert step.step_type == "Default"
    assert step.full_name == "Default (Test Step)"
    assert step.has_children is False
    assert step.children == []


def test_loop_step_update_full_name():
    step = Loop_Step(name="Test Step")
    step.update_full_name()
    assert step.full_name == "Default (Test Step)"


def test_loop_step_append_to_model(app):
    step = Loop_Step(name="Test Step")
    model = QStandardItemModel()
    item = step.append_to_model(model)
    assert item.text() == "Default (Test Step)"


def test_loop_step_get_protocol_string():
    step = Loop_Step(name="Test Step", step_info={"description": "Test description"})
    protocol_string = step.get_protocol_string()
    assert "Test description" in protocol_string


def test_loop_step_container_init():
    step = Loop_Step_Container(name="Container Step")
    assert step.name == "Container Step"
    assert step.step_type == "Container"
    assert step.has_children is True
    assert step.children == []


def test_loop_step_container_add_child():
    parent_step = Loop_Step_Container(name="Parent Step")
    child_step = Loop_Step(name="Child Step")
    parent_step.add_child(child_step)
    assert len(parent_step.children) == 1
    assert parent_step.children[0] == child_step


def test_loop_step_container_get_protocol_string():
    parent_step = Loop_Step_Container(name="Parent Step")
    child_step = Loop_Step(
        name="Child Step", step_info={"description": "Child description"}
    )
    parent_step.add_child(child_step)
    parent_step.update_time_weight()
    assert parent_step.time_weight == 2


def test_loop_step_name_widget_init(app):
    widget = Loop_Step_Name_Widget(name="Test Step", is_active=True)
    assert widget.lineEdit_name.text() == "Test Step"
    assert widget.checkBox_active.isChecked() is True


def test_loop_step_config_init(app):
    step = Loop_Step(
        name="Test Step",
        step_info={"description": "Test description", "is_active": True},
    )
    config_widget = Loop_Step_Config(loop_step=step)
    assert config_widget.name_widget.lineEdit_name.text() == "Test Step"
    assert config_widget.textEdit_desc.toPlainText() == "Test description"


def test_loop_step_config_change_name(app):
    step = Loop_Step(name="Old Name")
    config_widget = Loop_Step_Config(loop_step=step)
    config_widget.change_name("New Name")
    assert step.name == "New Name"
    assert step.full_name == "Default (New Name)"


def test_loop_step_config_change_active(app):
    step = Loop_Step(is_active=True)
    config_widget = Loop_Step_Config(loop_step=step)
    config_widget.change_active(False)
    assert step.is_active is False


def test_loop_step_config_update_step_config(app):
    step = Loop_Step(name="Test_Step", step_info={"description": "Old description"})
    config_widget = Loop_Step_Config(loop_step=step)
    config_widget.textEdit_desc.setPlainText("New description")
    config_widget.update_step_config()
    assert step.description == "New description"

def test_step_after_simple_sweep_starts_on_its_own_line():
    from nomad_camels.loop_steps.simple_sweep import Simple_Sweep
    from nomad_camels.loop_steps.wait_loop_step import Wait_Loop_Step

    sweep = Simple_Sweep(
        name="R1",
        step_info={
            "sweep_channel": "SMU_setV1",
            "read_channels": ["SMU_mesI1"],
            "start_val": "-voltage",
            "stop_val": "voltage",
            "n_points": "points_R",
            "loop_type": "start - stop",
        },
    )
    wait = Wait_Loop_Step(name="Wait_2", step_info={"wait_time": "wait_before"})
    overview = sweep.get_protocol_short_string() + wait.get_protocol_short_string()
    lines = overview.splitlines()
    assert lines[2].strip() == (
        "Values: (start: -voltage, stop: voltage, points: points_R)"
    )
    assert lines[3].startswith("Wait 'Wait_2'")
