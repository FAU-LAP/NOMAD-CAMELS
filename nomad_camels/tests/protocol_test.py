import importlib
import os.path
import sys
import databroker
import pytest

from PySide6.QtCore import Qt, QItemSelectionModel
from PySide6.QtWidgets import QMessageBox

from nomad_camels.frontpanels import protocol_config
from nomad_camels.bluesky_handling import make_catalog
from nomad_camels.frontpanels import instrument_installer
from nomad_camels.utility import variables_handling
from nomad_camels.utility.treeView_functions import getItemIndex
from threading import Thread
import asyncio
from zmq.error import ZMQError
from bluesky.callbacks.zmq import RemoteDispatcher, Publisher
from nomad_camels.main_classes.plot_proxy import StoppableProxy as Proxy

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session", autouse=True)
def zmq_setup():
    """
    Sets up a single ZMQ proxy, dispatcher, and publisher for all tests.
    Yields a tuple (publisher, dispatcher) for use in tests.
    Stops the proxy at the end of the session.
    """
    try:
        proxy = Proxy(5577, 5578)
        proxy_created = True
    except ZMQError:
        proxy = None  # Use already running proxy.
        proxy_created = False

    def start_proxy():
        if proxy_created and proxy is not None:
            proxy.start()

    # Setup dispatcher and its thread.
    dispatcher = RemoteDispatcher("localhost:5578")

    def start_dispatcher():
        try:
            dispatcher.start()
        except asyncio.exceptions.CancelledError:
            pass  # Ignore cancellation errors on shutdown.

    # Setup publisher.
    publisher = Publisher("localhost:5577")

    # Start proxy and dispatcher in daemon threads.
    proxy_thread = Thread(target=start_proxy, daemon=True)
    dispatcher_thread = Thread(target=start_dispatcher, daemon=True)
    proxy_thread.start()
    dispatcher_thread.start()

    # Yield the shared objects for tests.
    yield publisher, dispatcher

    # Teardown: stop the proxy once all tests have finished.
    if proxy_created and proxy is not None:
        proxy.stop()


@pytest.fixture(autouse=True)
def mock_message_box(monkeypatch):
    """If a messagebox, e.g. asking whether to discard all changes to the
    protocol, pops up, it is automatically accepted"""

    def mock_question(*args, **kwargs):
        return QMessageBox.Yes

    monkeypatch.setattr(QMessageBox, "question", mock_question)


def test_change_dev_config(qtbot, tmp_path, zmq_setup):
    """Opens the config for "change device config" tries to configure it for the
    demo instrument and tries to run a protocol with this step."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import change_device_config

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText(
        "test_change_dev_config_protocol"
    )
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Change Device Config")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, change_device_config.Change_DeviceConf_Config)
    conf_widge.comboBox_device.setCurrentText("demo_instrument")
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_change_dev_config_protocol"
    assert "Change Device Config (Change_Device_Config)" in prot.loop_step_dict
    assert prot.loop_steps[0].device == "demo_instrument"
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_for_loop(qtbot, tmp_path, zmq_setup):
    """Opens the config for a "For Loop" tries to configure it looping over a
    wait-step and tries to run a protocol with this step."""
    # ensure_demo_in_devices()
    from nomad_camels.loop_steps import for_while_loops

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_for_loop_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "For Loop")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, for_while_loops.For_Loop_Step_Config)
    conf_widge.sub_widget.lineEdit_start.setText("0")
    conf_widge.sub_widget.lineEdit_stop.setText("1")
    conf_widge.sub_widget.lineEdit_n_points.setText("11")

    action = get_action_from_name(conf.add_actions, "Wait")
    action.trigger()
    prot = conf.protocol

    select_step_by_name(conf, "Wait (Wait)")

    def wait_for_move_in():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1

    qtbot.waitUntil(wait_for_move_in)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot.name = "test_for_loop_protocol"
    assert "For Loop (For_Loop)" in prot.loop_step_dict
    assert prot.loop_steps[0].has_children
    assert prot.loop_steps[0].children[0].full_name == "Wait (Wait)"
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_gradient_descent(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Gradient Descent" tries to configure it for the
    demo instrument and tries to run a protocol with this step."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import gradient_descent

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText(
        "test_gradient_descent_protocol"
    )
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Gradient Descent")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, gradient_descent.Gradient_Descent_Config)
    conf_widge.sub_widget.lineEdit_momentum.setText("1")
    conf_widge.sub_widget.lineEdit_threshold.setText("1e-3")
    conf_widge.sub_widget.lineEdit_max_val.setText("1")
    conf_widge.sub_widget.lineEdit_min_val.setText("1")
    conf_widge.sub_widget.lineEdit_opt_func.setText("demo_instrument_detectorY")
    conf_widge.sub_widget.lineEdit_max_n_steps.setText("25")
    conf_widge.sub_widget.lineEdit_largest_step.setText("1")
    conf_widge.sub_widget.lineEdit_smallest_step.setText("0.01")
    conf_widge.sub_widget.lineEdit_learning_rate.setText("1")
    conf_widge.sub_widget.lineEdit_starting_val.setText("0")
    conf_widge.sub_widget.comboBox_extremum_type.setCurrentText("Maximum")
    conf_widge.sub_widget.comboBox_output_channel.setCurrentText(
        "demo_instrument_motorY"
    )
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.loop_steps[0].read_channels.append("demo_instrument_detectorY")
    prot.name = "test_gradient_descent_protocol"
    assert "Gradient Descent (Gradient_Descent)" in prot.loop_step_dict
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_if_and_set_variables(qtbot, tmp_path, zmq_setup):
    """Opens the config for "If" tries to configure to run the correct way if
    the variables have the correct value, which is done by a "Set Variables" step."""
    from nomad_camels.loop_steps import set_variables

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText(
        "test_if_and_set_variables_protocol"
    )
    prot = conf.protocol
    qtbot.addWidget(conf)
    qtbot.mouseClick(
        conf.general_settings.pushButton_add_variable, Qt.MouseButton.LeftButton
    )
    conf.general_settings.variable_table.model.item(0, 0).setText("condition")
    conf.general_settings.variable_table.model.item(0, 1).setText("1")
    single_variable_if(qtbot, conf, 1)
    assert "If (If)" in prot.loop_step_dict
    assert "If_Sub (If_condition != 1)" in prot.loop_step_dict
    assert "Elif_Sub (If_condition == 1)" in prot.loop_step_dict
    assert "Else_Sub (If_Else)" in prot.loop_step_dict

    action = get_action_from_name(conf.add_actions, "Set Variables")
    action.trigger()

    def wait_selection():
        """ """
        select_step_by_name(conf, f"Set Variables (Set_Variables)")
        conf.tree_click_sequence()
        assert isinstance(
            conf.loop_step_configuration_widget, set_variables.Set_Variables_Config
        )

    qtbot.waitUntil(wait_selection)
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(
        conf.loop_step_configuration_widget, set_variables.Set_Variables_Config
    )
    conf_widge.variables_table.add(["condition", "0"])

    single_variable_if(qtbot, conf, 0, 2, 1, 2)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_nd_sweep():
    """ """
    pass


def test_read_channels(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Read Channels" tries to configure it for the
    demo instrument and tries to run a protocol with this step."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import read_channels

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_read_channels_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Read Channels")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, read_channels.Read_Channels_Config)
    table = conf_widge.sub_widget.read_table.tableWidget_channels
    row = get_row_from_channel_table("demo_instrument_detectorX", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_read_channels_protocol"
    assert "Read Channels (Read_Channels)" in prot.loop_step_dict
    assert prot.loop_steps[0].channel_list == ["demo_instrument_detectorX"]
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_run_subprotocol():
    """ """
    pass


def test_set_channels(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Set Channels" tries to configure it for the
    demo instrument and tries to run a protocol with this step."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import set_channels

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_set_channels_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Set Channels")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, set_channels.Set_Channels_Config)
    table = conf_widge.sub_widget.tableWidget_channels
    row = get_row_from_channel_table("demo_instrument_motorX", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)
    table.item(row, 2).setText("1")
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_set_channels_protocol"
    assert "Set Channels (Set_Channels)" in prot.loop_step_dict
    assert prot.loop_steps[0].channels_values == {
        "Channels": ["demo_instrument_motorX"],
        "Values": ["1"],
    }
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_simple_sweep_with_plot_and_fit(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Simple Sweep" tries to configure it for the
    demo instrument. Further it adds a plot and a fit to the sweep and tries to
    run a protocol with this step."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import simple_sweep
    from nomad_camels.frontpanels import plot_definer

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_simple_sweep_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Simple Sweep")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, simple_sweep.Simple_Sweep_Config)
    conf_widge.sweep_widget.lineEdit_start.setText("-10")
    conf_widge.sweep_widget.lineEdit_stop.setText("10")
    conf_widge.sweep_widget.lineEdit_n_points.setText("21")
    conf_widge.comboBox_sweep_channel.setCurrentText("demo_instrument_motorY")

    table = conf_widge.read_table.tableWidget_channels
    row = get_row_from_channel_table("demo_instrument_detectorY", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)
    row = get_row_from_channel_table("demo_instrument_motorY", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)

    fit = plot_definer.Fit_Info(
        True, "Gaussian", x="demo_instrument_motorY", y="demo_instrument_detectorY"
    )
    plot = plot_definer.Plot_Info(
        x_axis="demo_instrument_motorY",
        y_axes={"formula": ["demo_instrument_detectorY"], "axis": ["left"]},
        fits=[fit],
    )
    conf_widge.plot_widge.plot_data = [plot]

    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_simple_sweep_protocol"
    assert "Simple Sweep (Simple_Sweep)" in prot.loop_step_dict
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)
    assert "True" == "True"


def test_for_loop_set_var_with_plot_and_linear_fit(qtbot, tmp_path, zmq_setup):
    """Creates a For Loop from -1 to 1 that, on each iteration,
    sets the variable 'set_var' to the loop value and waits for 0.001s.
    The protocol is configured to plot 'set_var' versus the loop value
    and perform a linear fit that is expected to be perfect (slope=1, intercept=0)."""
    # Create the protocol config widget and set the protocol name.
    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText(
        "test_for_loop_set_var_protocol"
    )
    qtbot.addWidget(conf)

    # Add a global variable "set_var" (initial value is arbitrary here).
    qtbot.mouseClick(
        conf.general_settings.pushButton_add_variable, Qt.MouseButton.LeftButton
    )
    conf.general_settings.variable_table.model.item(0, 0).setText("set_var")
    conf.general_settings.variable_table.model.item(0, 1).setText("0")

    # --- Add For Loop step ---
    action = get_action_from_name(conf.add_actions, "For Loop")
    action.trigger()
    from nomad_camels.loop_steps import for_while_loops

    conf_widge_loop = conf.loop_step_configuration_widget
    assert isinstance(conf_widge_loop, for_while_loops.For_Loop_Step_Config)
    conf_widge_loop.sub_widget.lineEdit_start.setText("-1")
    conf_widge_loop.sub_widget.lineEdit_stop.setText("1")
    conf_widge_loop.sub_widget.lineEdit_n_points.setText("21")

    # --- Add child step: Set Variables ---
    action = get_action_from_name(conf.add_actions, "Set Variables")
    action.trigger()
    from nomad_camels.loop_steps import set_variables

    def wait_selection_sv():
        select_step_by_name(conf, "Set Variables (Set_Variables)")
        conf.tree_click_sequence()
        assert isinstance(
            conf.loop_step_configuration_widget, set_variables.Set_Variables_Config
        )

    qtbot.waitUntil(wait_selection_sv)
    conf_widge_sv = conf.loop_step_configuration_widget
    # Configure the Set Variables step to assign the current for loop value to "set_var".
    # Here we assume that the expression "for_loop_value" is evaluated at runtime.
    conf_widge_sv.variables_table.add(["set_var", "For_Loop_Value"])

    # --- Read Channels ---
    action = get_action_from_name(conf.add_actions, "Read Channels")
    action.trigger()
    from nomad_camels.loop_steps import read_channels

    def wait_selection_rc():
        select_step_by_name(conf, "Read Channels (Read_Channels)")
        conf.tree_click_sequence()
        assert isinstance(
            conf.loop_step_configuration_widget, read_channels.Read_Channels_Config
        )

    qtbot.waitUntil(wait_selection_rc)

    # --- Add child step: Wait ---
    action = get_action_from_name(conf.add_actions, "Wait")
    action.trigger()

    from nomad_camels.loop_steps import wait_loop_step

    def wait_for_wait_widget():
        select_step_by_name(conf, "Wait (Wait)")
        conf.tree_click_sequence()
        return isinstance(
            conf.loop_step_configuration_widget, wait_loop_step.Wait_Loop_Step_Config
        )

    qtbot.waitUntil(wait_for_wait_widget)
    conf_widge_wait = conf.loop_step_configuration_widget
    assert isinstance(conf_widge_wait, wait_loop_step.Wait_Loop_Step_Config)
    conf_widge_wait.sub_widget.lineEdit_duration.setText("0.01")

    # --- Add a Plot definition with a linear fit ---
    from nomad_camels.frontpanels import plot_definer

    fit = plot_definer.Fit_Info(True, "Linear", x="For_Loop_Value", y="set_var")
    plot = plot_definer.Plot_Info(
        x_axis="For_Loop_Value",
        y_axes={"formula": ["set_var"], "axis": ["left"]},
        fits=[fit],
    )

    # Accept the protocol configuration.
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_for_loop_set_var_protocol"
    prot.plots.append(plot)

    def wait_for_move_in():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        print(len(prot.loop_steps))

    select_step_by_name(conf, "Set Variables (Set_Variables)")
    qtbot.waitUntil(wait_for_move_in)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    select_step_by_name(conf, "Read Channels (Read_Channels)")
    qtbot.waitUntil(wait_for_move_in)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    select_step_by_name(conf, "Wait (Wait)")
    qtbot.waitUntil(wait_for_move_in)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()

    # Build the catalog and run the protocol.
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)

    # --- After the protocol run, open the Nexus file and perform a linear fit ---
    # We assume that the protocol saves two datasets: one for the for-loop values
    # (named "for_loop_value") and one for the variable "set_var".
    import h5py
    import numpy as np

    if prot.use_nexus:
        file_ending = ".nxs"
    else:
        file_ending = ".h5"
    savepath = tmp_path / (prot.name + file_ending)
    with h5py.File(savepath, "r") as f:
        x_data = f[list(f.keys())[0]]["data"][
            "test_for_loop_set_var_protocol_variable_signal"
        ]["For_Loop_Value"][
            :
        ]  # for-loop (x-axis) values
        y_data = f[list(f.keys())[0]]["data"][
            "test_for_loop_set_var_protocol_variable_signal"
        ]["set_var"][
            :
        ]  # recorded set_var values
        slope_camels_fit = f[list(f.keys())[0]]["data"]["fits"][
            "Linear_set_var_v_For_Loop_Value_primary"
        ]["slope"][
            :
        ]  # linear fit values
        intercept_camels_fit = f[list(f.keys())[0]]["data"]["fits"][
            "Linear_set_var_v_For_Loop_Value_primary"
        ]["intercept"][
            :
        ]  # linear fit intercept

    # Compute a linear fit on the data.
    slope, intercept = np.polyfit(x_data, y_data, 1)
    # Check that the slope and intercept from the CAMELS fit are the same as the ones computed from the data.
    assert np.isclose(slope_camels_fit, slope, atol=0.05)
    assert np.isclose(intercept_camels_fit, intercept, atol=0.05)
    # Check that the slope is 1 and the intercept is 0 (within a small tolerance).
    assert np.isclose(slope, 1, atol=0.05)
    assert np.isclose(intercept, 0, atol=0.05)


def test_trigger_and_read_channels(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Read Channels" tries to configure it with a split
    triggering of the channels, then configures the trigger-step and tries to
    run a protocol with these steps."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import read_channels

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_trigger_protocol")
    qtbot.addWidget(conf)
    prot = conf.protocol
    variables_handling.current_protocol = prot
    action = get_action_from_name(conf.add_actions, "Read Channels")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, read_channels.Read_Channels_Config)
    conf_widge.sub_widget.checkBox_split_trigger.setChecked(True)
    conf_widge.sub_widget.checkBox_read_all.setChecked(True)

    action = get_action_from_name(conf.add_actions, "Trigger Channels")
    action.trigger()
    select_step_by_name(conf, "Trigger Channels (Trigger_Channels)")
    conf.tree_click_sequence()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, read_channels.Trigger_Channels_Config)

    def wait_for_move():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_up, Qt.MouseButton.LeftButton)
        assert isinstance(prot.loop_steps[0], read_channels.Trigger_Channels_Step)

    qtbot.waitUntil(wait_for_move)

    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot.name = "test_trigger_protocol"
    assert "Read Channels (Read_Channels)" in prot.loop_step_dict
    assert prot.loop_steps[1].read_all
    assert "Trigger Channels (Trigger_Channels)" in prot.loop_step_dict
    assert prot.loop_steps[0].read_step == "Read Channels (Read_Channels)"

    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_while_loop(qtbot, tmp_path, zmq_setup):
    """Opens the config for a "While Loop" and tries to configure it with the
    condition being `While_Loop_Count < 5`. Into the loop, a wait-step is added.
    Tries to run a protocol with this step."""
    from nomad_camels.loop_steps import for_while_loops

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_while_loop_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "While Loop")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, for_while_loops.While_Loop_Step_Config)
    conf_widge.sub_widget.lineEdit_condition.setText("While_Loop_Count < 5")

    action = get_action_from_name(conf.add_actions, "Wait")
    action.trigger()
    prot = conf.protocol

    select_step_by_name(conf, "Wait (Wait)")

    def wait_for_move_in():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1

    qtbot.waitUntil(wait_for_move_in)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot.name = "test_while_loop_protocol"
    assert "While Loop (While_Loop)" in prot.loop_step_dict
    assert prot.loop_steps[0].has_children
    assert prot.loop_steps[0].children[0].full_name == "Wait (Wait)"
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_wait(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Wait" tries to configure it to a wait time of
    1.0 second and tries to run a protocol with this step."""
    from nomad_camels.loop_steps import wait_loop_step

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_wait_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Wait")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, wait_loop_step.Wait_Loop_Step_Config)
    conf_widge.sub_widget.lineEdit_duration.setText("1.0")
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_wait_protocol"
    assert "Wait (Wait)" in prot.loop_step_dict
    assert prot.loop_steps[0].wait_time == "1.0"
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def single_variable_if(qtbot, conf, wait_in=1, n_prompt=0, n_if=0, len_prot=0):
    """

    Parameters
    ----------
    qtbot :

    conf :

    wait_in :
         (Default value = 1)
    n_prompt :
         (Default value = 0)
    n_if :
         (Default value = 0)
    len_prot :
         (Default value = 0)

    Returns
    -------

    """
    from nomad_camels.loop_steps import if_step

    action = get_action_from_name(conf.add_actions, "If")
    action.trigger()

    def wait_selection():
        """ """
        if n_if:
            select_step_by_name(conf, f"If (If_{n_if})")
        else:
            select_step_by_name(conf, f"If (If)")
        conf.tree_click_sequence()
        assert isinstance(conf.loop_step_configuration_widget, if_step.If_Step_Config)

    qtbot.waitUntil(wait_selection)
    conf_widge = conf.loop_step_configuration_widget
    conf_widge.sub_widget.lineEdit_condition.setText("condition != 1")
    conf_widge.sub_widget.elif_table.add("condition == 1")
    conf_widge.sub_widget.checkBox_use_else.setChecked(True)
    nam = "Prompt" if 0 != wait_in else "Wait"
    action = get_action_from_name(conf.add_actions, nam)
    action.trigger()
    prot = conf.protocol

    if n_prompt > 0 and nam == "Prompt":
        select_step_by_name(conf, f"{nam} ({nam}_{n_prompt})")
        n_prompt += 1
    elif nam == "Wait" and n_if:
        select_step_by_name(conf, f"{nam} ({nam}_{n_if})")
    else:
        select_step_by_name(conf, f"{nam} ({nam})")

    def wait_for_move():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_out, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_up, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_up, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1 + len_prot

    qtbot.waitUntil(wait_for_move)

    nam = "Prompt" if 1 != wait_in else "Wait"
    action = get_action_from_name(conf.add_actions, nam)
    action.trigger()
    if n_prompt > 0 and nam == "Prompt":
        select_step_by_name(conf, f"{nam} ({nam}_{n_prompt})")
        n_prompt += 1
    elif nam == "Wait" and n_if:
        select_step_by_name(conf, f"{nam} ({nam}_{n_if})")
    else:
        select_step_by_name(conf, f"{nam} ({nam})")

    def wait_for_move():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_out, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_up, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1 + len_prot

    qtbot.waitUntil(wait_for_move)

    action = get_action_from_name(conf.add_actions, "Prompt")
    action.trigger()
    if n_prompt == 0:
        n_prompt += 1
    select_step_by_name(conf, f"Prompt (Prompt_{n_prompt})")

    def wait_for_move():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1 + len_prot

    qtbot.waitUntil(wait_for_move)


def select_step_by_name(conf, name):
    """

    Parameters
    ----------
    conf :

    name :


    Returns
    -------

    """
    model = conf.treeView_protocol_sequence.model()
    conf.treeView_protocol_sequence.selectionModel().clearSelection()
    index = getItemIndex(model, name)
    conf.treeView_protocol_sequence.selectionModel().select(
        index, QItemSelectionModel.Select
    )
    conf.check_movability()


def get_row_from_channel_table(name, table):
    """

    Parameters
    ----------
    name :

    table :


    Returns
    -------

    """
    for i in range(table.rowCount()):
        row_name = table.item(i, 1).text()
        if name == row_name:
            return i


def ensure_demo_in_devices():
    """Ensure that only the demo_instrument is loaded in the devices dictionary."""
    instr, packs = instrument_installer.getInstalledDevices(True, True)
    if "demo_instrument" not in instr:
        instrument_installer.install_instrument("demo_instrument")
        instr, packs = instrument_installer.getInstalledDevices(True, True)
        assert "demo_instrument" in instr

    # Clear all devices and keep only demo_instrument
    if "demo_instrument" in variables_handling.devices:
        demo_inst = variables_handling.devices["demo_instrument"]
        variables_handling.devices.clear()
        variables_handling.devices["demo_instrument"] = demo_inst
    else:
        variables_handling.devices.clear()
        inst = packs["demo_instrument"].subclass()
        variables_handling.devices["demo_instrument"] = inst

    assert "demo_instrument" in variables_handling.devices
    assert (
        len(variables_handling.devices) == 1
    ), "Only demo_instrument should be present"

    # Clear and repopulate channels
    variables_handling.channels.clear()
    for dev in variables_handling.devices.values():
        variables_handling.channels.update(dev.get_channels())


def catalog_maker(tmp_path):
    """

    Parameters
    ----------
    tmp_path :


    Returns
    -------

    """
    if tmp_path is None:
        tmp_path = ""
    if "test_catalog" not in list(databroker.catalog):
        make_catalog.make_yml(tmp_path, "test_catalog")


def run_test_protocol(tmp_path, protocol, publisher, dispatcher):
    """

    Parameters
    ----------
    tmp_path :

    protocol :


    Returns
    -------

    """
    from nomad_camels.bluesky_handling import protocol_builder

    file = tmp_path / (protocol.name + ".py")
    savepath = tmp_path / protocol.name
    protocol_builder.build_protocol(protocol, file, savepath, "test_catalog")
    sys.path.append(str(tmp_path))
    py_package = importlib.import_module(protocol.name)
    py_package.main(dispatcher=dispatcher, publisher=publisher)
    if protocol.use_nexus:
        file_ending = ".nxs"
    else:
        file_ending = ".h5"
    savepath = f"{savepath}{file_ending}"
    assert os.path.isfile(savepath)


def get_action_from_name(actions, name):
    """

    Parameters
    ----------
    actions :

    name :


    Returns
    -------

    """
    for act in actions:
        if act.text() == name:
            return act
    return None
