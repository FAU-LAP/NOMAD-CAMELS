from PySide6.QtCore import QItemSelectionModel, Qt


def test_install_demo_device(qtbot):
    from nomad_camels.frontpanels import instrument_installer
    installer = instrument_installer.Instrument_Installer()
    qtbot.addWidget(installer)
    install_demo(qtbot, installer)

def install_demo(qtbot, installer):
    for box in installer.checkboxes:
        if box.text() == 'demo_device':
            box.setChecked(True)
            break
    with qtbot.waitSignal(installer.instruments_updated, timeout=60000) as blocker:
        qtbot.mouseClick(installer.pushButton_install_update_selected,
                         Qt.MouseButton.LeftButton)
    assert 'demo_device' in installer.installed_devs

def test_add_device(qtbot):
    from nomad_camels.frontpanels import manage_instruments
    manager = manage_instruments.ManageInstruments()
    installer = manager.installer
    if 'demo_device' not in installer.installed_devs:
        install_demo(qtbot, installer)
    conf = manager.config_widget
    conf.build_table()
    item1 = None
    item2 = None
    for row in range(conf.tableWidget_instruments.rowCount()):
        item1 = conf.tableWidget_instruments.item(row, 0)
        item2 = conf.tableWidget_instruments.item(row, 1)
        if item1.text() == 'demo_device':
            break
    assert item1 is not None
    assert item2 is not None
    index1 = conf.tableWidget_instruments.indexFromItem(item1)
    conf.tableWidget_instruments.selectionModel().select(index1, QItemSelectionModel.Select)
    index2 = conf.tableWidget_instruments.indexFromItem(item2)
    conf.tableWidget_instruments.selectionModel().select(index2, QItemSelectionModel.Select)
    conf.table_click()
    qtbot.mouseClick(conf.pushButton_add, Qt.MouseButton.LeftButton)

    def check_instr_in():
        instr = conf.get_config()
        assert 'demo_device' in instr
    qtbot.waitUntil(check_instr_in)

    qtbot.mouseClick(conf.pushButton_remove, Qt.MouseButton.LeftButton)
