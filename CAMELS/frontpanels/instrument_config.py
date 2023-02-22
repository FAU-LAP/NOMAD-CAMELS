import importlib

from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTabWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt

from CAMELS.gui.instrument_config import Ui_Form

from CAMELS.frontpanels.device_installer import getInstalledDevices


class Instrument_Config(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.installed_instr = getInstalledDevices()
        self.packages = {}
        self.active_instruments = {}
        for k in self.installed_instr:
            if k not in self.active_instruments:
                self.active_instruments[k] = []
        self.tableWidget_instruments.setColumnCount(2)

        self.tableWidget_instruments.verticalHeader().setHidden(True)
        self.current_instr = ''

        self.build_table()
        self.tableWidget_instruments.setMaximumWidth(350)
        self.lineEdit_search.setMaximumWidth(250)
        self.label.setMaximumWidth(100)
        self.lineEdit_search.textChanged.connect(self.build_table)
        self.tableWidget_instruments.clicked.connect(self.table_click)
        self.pushButton_add.clicked.connect(self.add_instance)
        self.pushButton_remove.clicked.connect(self.remove_instance)

    def table_click(self):
        ind = self.tableWidget_instruments.selectedIndexes()[0]
        instr = self.tableWidget_instruments.item(ind.row(), 0).text()
        self.get_current_config()
        self.current_instr = instr
        self.label_config.setText(f'Configure: {instr}')
        if instr not in self.packages:
            self.packages[instr] = importlib.import_module(f'camels_driver_{instr}.{instr}')
        self.config_tabs.clear()
        if not self.active_instruments[instr]:
            self.config_tabs.addTab(QLabel('Add an instrument\ninstance by clicking "+"'), 'no instrument')
            self.pushButton_remove.setEnabled(False)
        else:
            self.pushButton_remove.setEnabled(True)
            pack = self.packages[instr]
            for instrument in self.active_instruments[instr]:
                name = instrument.custom_name
                inst_widge = pack.subclass_config(parent=self,
                                                  data=name,
                                                  settings_dict=instrument.settings,
                                                  config_dict=instrument.config,
                                                  ioc_dict=instrument.ioc_settings,
                                                  additional_info=instrument.additional_info)
                self.config_tabs.addTab(inst_widge, name)
        self.pushButton_add.setEnabled(True)

    def get_config(self):
        self.get_current_config()
        instruments = {}
        for instr in self.active_instruments:
            for instrument in self.active_instruments[instr]:
                instruments[instrument.custom_name] = instrument
        return instruments

    def get_current_config(self):
        for i in range(self.config_tabs.count()):
            tab = self.config_tabs.widget(i)
            if not hasattr(tab, 'data'):
                continue
            self.active_instruments[self.current_instr][i].settings = tab.get_settings()
            self.active_instruments[self.current_instr][i].config = tab.get_config()
            self.active_instruments[self.current_instr][i].ioc_settings = tab.get_ioc_settings()
            self.active_instruments[self.current_instr][i].additional_info = tab.get_info()

    def add_instance(self):
        ind = self.tableWidget_instruments.selectedIndexes()[0]
        instr = self.tableWidget_instruments.item(ind.row(), 0).text()
        pack = self.packages[instr]
        if not self.active_instruments[instr]:
            self.config_tabs.clear()
            name = instr
            self.pushButton_remove.setEnabled(True)
        else:
            name = instr
            i = 1
            names = self.get_all_names()
            while name in names:
                name = f'{instr}_{i}'
                i += 1
        instr_instance = pack.subclass()
        instr_instance.custom_name = name
        self.active_instruments[instr].append(instr_instance)
        single_widge = pack.subclass_config(data=name, settings_dict={},
                                            config_dict={}, ioc_dict={},
                                            additional_info={})
        self.config_tabs.addTab(single_widge, name)
        self.tableWidget_instruments.item(ind.row(), 1).setText(str(len(self.active_instruments[instr])))

    def get_all_names(self):
        names = []
        for instr in self.active_instruments:
            names += [x.custom_name for x in self.active_instruments[instr]]
        return names


    def remove_instance(self):
        ind = self.config_tabs.currentIndex()
        name = self.config_tabs.tabText(ind)
        remove_dialog = QMessageBox.question(self, 'Remove entry?',
                                             f'Are you sure you want to remove the instrument {name}?',
                                             QMessageBox.Yes | QMessageBox.No)
        if remove_dialog != QMessageBox.Yes:
            return
        self.config_tabs.removeTab(ind)
        instr_ind = self.tableWidget_instruments.selectedIndexes()[0]
        instr = self.tableWidget_instruments.item(instr_ind.row(), 0).text()
        self.active_instruments[instr].pop(ind)
        if not self.active_instruments[instr]:
            self.config_tabs.addTab(QLabel('Add an instrument\ninstance by clicking "+"'), 'no instrument')
            self.pushButton_remove.setEnabled(False)
        self.tableWidget_instruments.item(instr_ind.row(), 1).setText(str(len(self.active_instruments[instr])))


    def build_table(self):
        search_text = self.lineEdit_search.text()
        self.tableWidget_instruments.clear()
        self.tableWidget_instruments.setRowCount(0)
        self.tableWidget_instruments.setHorizontalHeaderLabels(['instrument', 'number of instruments'])
        i = 0
        for dev in sorted(self.installed_instr.keys()):
            if search_text.lower() not in dev.lower():
                continue
            self.tableWidget_instruments.setRowCount(i+1)
            item = QTableWidgetItem(dev)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

            item_n = QTableWidgetItem(str(len(self.active_instruments[dev])))
            item_n.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.tableWidget_instruments.setItem(i, 0, item)
            self.tableWidget_instruments.setItem(i, 1, item_n)
            i += 1
        self.tableWidget_instruments.resizeColumnsToContents()




if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])

    widge = Instrument_Config()
    widge.show()
    app.exec_()