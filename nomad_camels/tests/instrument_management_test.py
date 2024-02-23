from PySide6.QtCore import QItemSelectionModel, Qt


def test_install_demo_instrument(qtbot):
    """This test tries to install the demo device, using the
    instrument_installer widget."""
    from nomad_camels.frontpanels import instrument_installer

    installer = instrument_installer.Instrument_Installer()
    qtbot.addWidget(
        installer
    )  # used to run the qt-app and close the widget after the test
    install_demo(qtbot, installer)


def install_demo(qtbot, installer):
    """A helper function, used by `test_install_demo_instrument` and also by
    `test_add_device`, if the device is not yet installed"""
    for box in installer.checkboxes:
        if box.text() == "demo_instrument":
            box.setChecked(True)
            break
    with qtbot.waitSignal(installer.instruments_updated, timeout=60000) as blocker:
        qtbot.mouseClick(
            installer.pushButton_install_update_selected, Qt.MouseButton.LeftButton
        )
        # the instruments_updated signal is being waited for, after clicking on
        # the install/update button
    assert "demo_instrument" in installer.installed_devs


def test_add_device(qtbot):
    """Going through the instrument management, if demo_instrument is not installed,
    it will be. Then the config widget is used to add a demo_instrument.
    In the end there is a check whether it is in the list of devices."""
    from nomad_camels.frontpanels import manage_instruments

    manager = manage_instruments.ManageInstruments()
    qtbot.addWidget(manager)
    installer = manager.installer
    if "demo_instrument" not in installer.installed_devs:
        install_demo(qtbot, installer)  # install if not there
    conf = manager.config_widget
    conf.build_table()
    item1 = None
    item2 = None
    for row in range(conf.tableWidget_instruments.rowCount()):
        item1 = conf.tableWidget_instruments.item(row, 0)
        item2 = conf.tableWidget_instruments.item(row, 1)
        if item1.text() == "demo_instrument":
            break
    assert item1 is not None  # demo_instrument should be in the installed table
    assert item2 is not None
    index1 = conf.tableWidget_instruments.indexFromItem(item1)
    conf.tableWidget_instruments.selectionModel().select(
        index1, QItemSelectionModel.Select
    )
    index2 = conf.tableWidget_instruments.indexFromItem(item2)
    conf.tableWidget_instruments.selectionModel().select(
        index2, QItemSelectionModel.Select
    )
    # two items need to be selected, since with a real click, the selection also
    # returns a list
    conf.table_click()  # select

    def check_instr_in():
        """ """
        # clicking on an added device, check whether it is actually added
        qtbot.mouseClick(conf.pushButton_add, Qt.MouseButton.LeftButton)
        instr = conf.get_config()
        assert "demo_instrument" in instr

    qtbot.waitUntil(check_instr_in)  # wait for the qt event loops
