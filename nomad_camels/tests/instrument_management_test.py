
def test_install_add_demo_device():
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QCoreApplication, QItemSelectionModel, Qt
    from PySide6.QtTest import QTest
    from nomad_camels.frontpanels import manage_instruments
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    manager = manage_instruments.ManageInstruments()
    installer = manager.installer
    for box in installer.checkboxes:
        if box.text() == 'demo_device':
            box.setChecked(True)
    QTest.mouseClick(installer.pushButton_install_update_selected,
                     Qt.MouseButton.LeftButton)
    conf = manager.config_widget
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
    conf.add_instance()
    instr = conf.get_config()
    app.processEvents()
    assert 'demo_device' in instr
