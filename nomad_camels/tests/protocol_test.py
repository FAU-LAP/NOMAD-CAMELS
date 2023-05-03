import importlib
import os.path
import sys
import databroker
from nomad_camels.frontpanels import protocol_config
from nomad_camels.bluesky_handling import make_catalog
from nomad_camels.frontpanels import instrument_installer
from nomad_camels.utility import variables_handling
from nomad_camels.utility.treeView_functions import getItemIndex
from PySide6.QtCore import Qt, QItemSelectionModel


def test_change_dev_config(qtbot, tmp_path):
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import change_device_config
    conf = protocol_config.Protocol_Config()
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, 'Change Device Config')
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge,
                      change_device_config.Change_DeviceConf_Config)
    conf_widge.comboBox_device.setCurrentText('demo_device')
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = 'test_change_dev_config_protocol'
    assert 'Change Device Config (Change_Device_Config)' in prot.loop_step_dict
    assert prot.loop_steps[0].device == 'demo_device'
    catalog_maker(tmp_path)
    run_test_protocol(tmp_path, prot)

def test_for_loop(qtbot, tmp_path):
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import for_while_loops
    conf = protocol_config.Protocol_Config()
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, 'For Loop')
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge,
                      for_while_loops.For_Loop_Step_Config)
    conf_widge.sub_widget.lineEdit_start.setText('0')
    conf_widge.sub_widget.lineEdit_stop.setText('1')
    conf_widge.sub_widget.lineEdit_n_points.setText('11')

    action = get_action_from_name(conf.add_actions, 'Wait')
    action.trigger()
    prot = conf.protocol

    select_step_by_name(conf, 'Wait (Wait)')

    def wait_for_move_in():
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1
    qtbot.waitUntil(wait_for_move_in)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot.name = 'test_for_loop_protocol'
    assert 'For Loop (For_Loop)' in prot.loop_step_dict
    assert prot.loop_steps[0].has_children
    assert prot.loop_steps[0].children[0].full_name == 'Wait (Wait)'
    catalog_maker(tmp_path)
    run_test_protocol(tmp_path, prot)

def test_gradient_descent(qtbot, tmp_path):
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import gradient_descent
    conf = protocol_config.Protocol_Config()
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, 'Gradient Descent')
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge,
                      gradient_descent.Gradient_Descent_Config)
    conf_widge.sub_widget.lineEdit_momentum.setText('1')
    conf_widge.sub_widget.lineEdit_threshold.setText('1e-3')
    conf_widge.sub_widget.lineEdit_max_val.setText('1')
    conf_widge.sub_widget.lineEdit_min_val.setText('1')
    conf_widge.sub_widget.lineEdit_opt_func.setText('demo_device_detectorY')
    conf_widge.sub_widget.lineEdit_max_n_steps.setText('25')
    conf_widge.sub_widget.lineEdit_largest_step.setText('1')
    conf_widge.sub_widget.lineEdit_smallest_step.setText('0.01')
    conf_widge.sub_widget.lineEdit_learning_rate.setText('1')
    conf_widge.sub_widget.lineEdit_starting_val.setText('0')
    conf_widge.sub_widget.comboBox_extremum_type.setCurrentText('Maximum')
    conf_widge.sub_widget.comboBox_output_channel.setCurrentText('demo_device_motorY')
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.loop_steps[0].read_channels.append('demo_device_detectorY')
    prot.name = 'test_gradient_descent_protocol'
    assert 'Gradient Descent (Gradient_Descent)' in prot.loop_step_dict
    catalog_maker(tmp_path)
    run_test_protocol(tmp_path, prot)

def test_if_and_set_variables(qtbot, tmp_path):
    from nomad_camels.loop_steps import set_variables
    conf = protocol_config.Protocol_Config()
    prot = conf.protocol
    qtbot.addWidget(conf)
    qtbot.mouseClick(conf.general_settings.pushButton_add_variable,
                     Qt.MouseButton.LeftButton)
    conf.general_settings.variable_model.item(0, 0).setText('condition')
    conf.general_settings.variable_model.item(0, 1).setText('1')
    single_variable_if(qtbot, conf, 1)
    assert 'If (If)' in prot.loop_step_dict
    assert 'If_Sub (If_condition != 1)' in prot.loop_step_dict
    assert 'Elif_Sub (If_condition == 1)' in prot.loop_step_dict
    assert 'Else_Sub (If_Else)' in prot.loop_step_dict

    action = get_action_from_name(conf.add_actions, 'Set Variables')
    action.trigger()

    def wait_selection():
        select_step_by_name(conf, f'Set Variables (Set_Variables)')
        conf.tree_click_sequence()
        assert isinstance(conf.loop_step_configuration_widget,
                          set_variables.Set_Variables_Config)
    qtbot.waitUntil(wait_selection)
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf.loop_step_configuration_widget,
                      set_variables.Set_Variables_Config)
    conf_widge.variables_table.add(['condition', '0'])

    single_variable_if(qtbot, conf, 0, 2, 1, 2)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    catalog_maker(tmp_path)
    run_test_protocol(tmp_path, prot)

def test_nd_sweep():
    pass

def test_read_channels(qtbot, tmp_path):
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import read_channels
    conf = protocol_config.Protocol_Config()
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, 'Read Channels')
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge,
                      read_channels.Read_Channels_Config)
    table = conf_widge.sub_widget.read_table.tableWidget_channels
    row = get_row_from_channel_table('demo_device_detectorX', table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = 'test_read_channels_protocol'
    assert 'Read Channels (Read_Channels)' in prot.loop_step_dict
    assert prot.loop_steps[0].channel_list == ['demo_device_detectorX']
    catalog_maker(tmp_path)
    run_test_protocol(tmp_path, prot)

def test_run_subprotocol():
    pass

def test_set_channels(qtbot, tmp_path):
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import set_channels
    conf = protocol_config.Protocol_Config()
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, 'Set Channels')
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge,
                      set_channels.Set_Channels_Config)
    table = conf_widge.sub_widget.tableWidget_channels
    row = get_row_from_channel_table('demo_device_motorX', table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)
    table.item(row, 2).setText('1')
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = 'test_set_channels_protocol'
    assert 'Set Channels (Set_Channels)' in prot.loop_step_dict
    assert prot.loop_steps[0].channels_values == {'Channels': ['demo_device_motorX'], 'Values': ['1']}
    catalog_maker(tmp_path)
    run_test_protocol(tmp_path, prot)

def test_simple_sweep():
    pass

def test_trigger_and_read_channels(qtbot, tmp_path):
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import read_channels
    conf = protocol_config.Protocol_Config()
    qtbot.addWidget(conf)
    prot = conf.protocol
    variables_handling.current_protocol = prot
    action = get_action_from_name(conf.add_actions, 'Read Channels')
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge,
                      read_channels.Read_Channels_Config)
    conf_widge.sub_widget.checkBox_split_trigger.setChecked(True)
    conf_widge.sub_widget.checkBox_read_all.setChecked(True)

    action = get_action_from_name(conf.add_actions, 'Trigger Channels')
    action.trigger()
    select_step_by_name(conf, 'Trigger Channels (Trigger_Channels)')
    conf.tree_click_sequence()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge,
                      read_channels.Trigger_Channels_Config)

    def wait_for_move():
        qtbot.mouseClick(conf.pushButton_move_step_up, Qt.MouseButton.LeftButton)
        assert isinstance(prot.loop_steps[0], read_channels.Trigger_Channels_Step)
    qtbot.waitUntil(wait_for_move)

    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot.name = 'test_read_channels_protocol'
    assert 'Read Channels (Read_Channels)' in prot.loop_step_dict
    assert prot.loop_steps[1].read_all
    assert 'Trigger Channels (Trigger_Channels)' in prot.loop_step_dict
    assert prot.loop_steps[0].read_step == 'Read Channels (Read_Channels)'

    catalog_maker(tmp_path)
    run_test_protocol(tmp_path, prot)

def test_while_loop():
    pass

def test_wait(qtbot, tmp_path):
    from nomad_camels.loop_steps import wait_loop_step
    conf = protocol_config.Protocol_Config()
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, 'Wait')
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge,
                      wait_loop_step.Wait_Loop_Step_Config)
    conf_widge.sub_widget.lineEdit_duration.setText('1.0')
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = 'test_wait_protocol'
    assert 'Wait (Wait)' in prot.loop_step_dict
    assert prot.loop_steps[0].wait_time == '1.0'
    catalog_maker(tmp_path)
    run_test_protocol(tmp_path, prot)






def single_variable_if(qtbot, conf, wait_in=1, n_prompt=0, n_if=0, len_prot=0):
    from nomad_camels.loop_steps import if_step
    action = get_action_from_name(conf.add_actions, 'If')
    action.trigger()

    def wait_selection():
        if n_if:
            select_step_by_name(conf, f'If (If_{n_if})')
        else:
            select_step_by_name(conf, f'If (If)')
        conf.tree_click_sequence()
        assert isinstance(conf.loop_step_configuration_widget,
                          if_step.If_Step_Config)
    qtbot.waitUntil(wait_selection)
    conf_widge = conf.loop_step_configuration_widget
    conf_widge.sub_widget.lineEdit_condition.setText('condition != 1')
    conf_widge.sub_widget.elif_table.add('condition == 1')
    conf_widge.sub_widget.checkBox_use_else.setChecked(True)
    nam = 'Prompt' if 0 != wait_in else 'Wait'
    action = get_action_from_name(conf.add_actions, nam)
    action.trigger()
    prot = conf.protocol

    if n_prompt > 0 and nam == 'Prompt':
        select_step_by_name(conf, f'{nam} ({nam}_{n_prompt})')
        n_prompt += 1
    elif nam == 'Wait' and n_if:
        select_step_by_name(conf, f'{nam} ({nam}_{n_if})')
    else:
        select_step_by_name(conf, f'{nam} ({nam})')

    def wait_for_move():
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_out, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_up, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_up, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1 + len_prot
    qtbot.waitUntil(wait_for_move)


    nam = 'Prompt' if 1 != wait_in else 'Wait'
    action = get_action_from_name(conf.add_actions, nam)
    action.trigger()
    if n_prompt > 0 and nam == 'Prompt':
        select_step_by_name(conf, f'{nam} ({nam}_{n_prompt})')
        n_prompt += 1
    elif nam == 'Wait' and n_if:
        select_step_by_name(conf, f'{nam} ({nam}_{n_if})')
    else:
        select_step_by_name(conf, f'{nam} ({nam})')

    def wait_for_move():
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_out, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_up, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1 + len_prot
    qtbot.waitUntil(wait_for_move)

    action = get_action_from_name(conf.add_actions, 'Prompt')
    action.trigger()
    if n_prompt == 0:
        n_prompt += 1
    select_step_by_name(conf, f'Prompt (Prompt_{n_prompt})')

    def wait_for_move():
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1 + len_prot
    qtbot.waitUntil(wait_for_move)


def select_step_by_name(conf, name):
    model = conf.treeView_protocol_sequence.model()
    conf.treeView_protocol_sequence.selectionModel().clearSelection()
    index = getItemIndex(model, name)
    conf.treeView_protocol_sequence.selectionModel().select(index, QItemSelectionModel.Select)


def get_row_from_channel_table(name, table):
    for i in range(table.rowCount()):
        row_name = table.item(i, 1).text()
        if name == row_name:
            return i


def ensure_demo_in_devices():
    instr, packs = instrument_installer.getInstalledDevices(True, True)
    if 'demo_device' not in instr:
        instrument_installer.install_instrument('demo_device')
        instr, packs = instrument_installer.getInstalledDevices(True, True)
        assert 'demo_device' in instr
    if 'demo_device' not in variables_handling.devices:
        inst = packs['demo_device'].subclass()
        variables_handling.devices['demo_device'] = inst
    assert 'demo_device' in variables_handling.devices
    variables_handling.channels.clear()
    for key, dev in variables_handling.devices.items():
        for channel in dev.get_channels():
            variables_handling.channels.update({channel: dev.channels[channel]})


def catalog_maker(tmp_path):
    if 'test_catalog' not in list(databroker.catalog):
        make_catalog.make_yml(tmp_path, 'test_catalog')

def run_test_protocol(tmp_path, protocol):
    from nomad_camels.bluesky_handling import protocol_builder
    file = tmp_path / (protocol.name + '.py')
    savepath = tmp_path / (protocol.name + '.h5')
    protocol_builder.build_protocol(protocol, file, savepath, 'test_catalog')
    sys.path.append(str(tmp_path))
    py_package = importlib.import_module(protocol.name)
    py_package.main()
    assert os.path.isfile(savepath)

def get_action_from_name(actions, name):
    for act in actions:
        if act.text() == name:
            return act
    return None
