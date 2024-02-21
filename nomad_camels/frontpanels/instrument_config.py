import importlib

import importlib_metadata
from PySide6.QtWidgets import (
    QWidget,
    QTableWidgetItem,
    QLabel,
    QMessageBox,
    QTextBrowser,
)
from PySide6.QtCore import Qt

from nomad_camels.gui.instrument_config import Ui_Form

from nomad_camels.frontpanels.instrument_installer import (
    getInstalledDevices,
    Info_Widget,
)

from nomad_camels.utility import variables_handling, device_handling

from nomad_camels.ui_widgets.warn_popup import WarnPopup


class Instrument_Config(Ui_Form, QWidget):
    """ """

    def __init__(self, active_instruments=None, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.installed_instr, self.packages = getInstalledDevices(return_packages=True)
        active_instruments = active_instruments or {}
        self.active_instruments = {}
        for instrument in active_instruments.values():
            instr = instrument.name
            if instr in self.active_instruments:
                self.active_instruments[instr].append(instrument)
            else:
                self.active_instruments[instr] = [instrument]
        for k in self.installed_instr:
            if k not in self.active_instruments:
                self.active_instruments[k] = []
        for k in self.active_instruments:
            if k not in self.installed_instr:
                WarnPopup(
                    text=f'Instrument type "{k}" in active instruments, but is not installed!',
                    title="instrument not installed",
                )
                # raise Warning(f'Instrument type "{k}" in active instruments, but is not installed!')
        self.tableWidget_instruments.setColumnCount(2)

        self.tableWidget_instruments.verticalHeader().setHidden(True)
        self.current_instr = ""

        self.build_table()
        self.tableWidget_instruments.setMaximumWidth(350)
        self.lineEdit_search.setMaximumWidth(250)
        self.label.setMaximumWidth(100)
        self.lineEdit_search.textChanged.connect(self.build_table)
        self.tableWidget_instruments.clicked.connect(self.table_click)
        self.pushButton_add.clicked.connect(self.add_instance)
        self.pushButton_remove.clicked.connect(self.remove_instance)
        self.info_widge = Info_Widget(self)
        self.info_widge.setHidden(True)
        self.layout().addWidget(self.info_widge, 0, 5, 3, 1)

        self.hide_info = False
        self.toggle_info_hidden()
        self.pushButton_info.clicked.connect(self.toggle_info_hidden)

    def toggle_info_hidden(self):
        if self.hide_info:
            self.pushButton_info.setText("hide info")
        else:
            self.pushButton_info.setText("show info")
        self.hide_info = not self.hide_info
        self.show_hide_info()

    def show_hide_info(self):
        self.info_widge.setHidden(self.hide_info)

    def table_click(self):
        """ """
        self.setCursor(Qt.WaitCursor)
        try:
            ind = self.tableWidget_instruments.selectedIndexes()[0]
            instr = self.tableWidget_instruments.item(ind.row(), 0).text()
            self.get_current_config()
            self.current_instr = instr
            self.label_config.setText(f"Configure: {instr}")
            if instr not in self.packages:
                self.packages[instr] = importlib.import_module(
                    f"nomad_camels_driver_{instr}.{instr}"
                )
            self.config_tabs.clear()
            if not self.active_instruments[instr]:
                self.config_tabs.addTab(
                    QLabel('Add an instrument\ninstance by clicking "+"'),
                    "no instrument",
                )
                self.pushButton_remove.setEnabled(False)
            else:
                self.pushButton_remove.setEnabled(True)
                pack = self.packages[instr]
                for instrument in self.active_instruments[instr]:
                    name = instrument.custom_name
                    inst_widge = pack.subclass_config(
                        parent=self,
                        data=name,
                        settings_dict=instrument.settings,
                        config_dict=instrument.config,
                        additional_info=instrument.additional_info,
                    )
                    self.config_tabs.addTab(inst_widge, name)
                    inst_widge.name_change.connect(self.name_config_changed)
            self.pushButton_add.setEnabled(True)
            self.info_widge.update_texts(instr)
            self.pushButton_info.setHidden(not self.info_widge.info)
            self.show_hide_info()
        finally:
            self.setCursor(Qt.ArrowCursor)

    def name_config_changed(self, new_name):
        """

        Parameters
        ----------
        new_name :


        Returns
        -------

        """
        current_tab = self.config_tabs.currentIndex()
        conf = self.config_tabs.widget(current_tab)
        ind = self.tableWidget_instruments.selectedIndexes()[0]
        instr = self.tableWidget_instruments.item(ind.row(), 0).text()

        if hasattr(conf, "data") and new_name not in self.get_all_names():
            self.active_instruments[instr][current_tab].custom_name = new_name
            conf.data = new_name
            self.config_tabs.setTabText(current_tab, new_name)

    def get_config(self):
        """ """
        self.get_current_config()
        instruments = {}
        for instr in self.active_instruments:
            for instrument in self.active_instruments[instr]:
                instruments[instrument.custom_name] = instrument
        return instruments

    def get_current_config(self):
        """ """
        for i in range(self.config_tabs.count()):
            tab = self.config_tabs.widget(i)
            if not hasattr(tab, "data"):
                continue
            cust_name = self.active_instruments[self.current_instr][i].custom_name
            given_name = tab.lineEdit_custom_name.text()
            if given_name != cust_name:
                WarnPopup(
                    self,
                    f'Instrument name "{given_name}" is either already in use or not allowed (e.g. the instrument`s class is named that way). Using "{cust_name}" instead.',
                    "Instrument name not possible",
                )
            variables_handling.check_variable_name(
                cust_name, parent=self, raise_not_warn=True
            )
            self.active_instruments[self.current_instr][i].settings = tab.get_settings()
            self.active_instruments[self.current_instr][i].config = tab.get_config()
            self.active_instruments[self.current_instr][
                i
            ].additional_info = tab.get_info()
        self.update_channels()

    def update_channels(self):
        """Called when the active devices change.
        The channels in variables_handling are updated with the ones
        provided by the active devices.

        Parameters
        ----------

        Returns
        -------

        """
        variables_handling.channels.clear()
        instruments = {}
        for instr in self.active_instruments:
            for instrument in self.active_instruments[instr]:
                instruments[instrument.custom_name] = instrument
        for key, dev in instruments.items():
            variables_handling.channels.update(dev.get_channels())
            variables_handling.config_channels.update(dev.config_channels)

    def add_instance(self):
        """ """
        self.setCursor(Qt.WaitCursor)
        try:
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
                    name = f"{instr}_{i}"
                    i += 1
            instr_instance = pack.subclass()
            instr_instance.custom_name = name
            self.active_instruments[instr].append(instr_instance)
            single_widge = pack.subclass_config(
                data=name,
                settings_dict=instr_instance.settings,
                config_dict=instr_instance.config,
                additional_info=instr_instance.additional_info,
            )
            self.config_tabs.addTab(single_widge, name)
            single_widge.name_change.connect(self.name_config_changed)
            self.tableWidget_instruments.item(ind.row(), 1).setText(
                str(len(self.active_instruments[instr]))
            )
        finally:
            self.setCursor(Qt.ArrowCursor)

    def get_all_names(self):
        """ """
        names = []
        for instr in self.active_instruments:
            if self.active_instruments[instr]:
                names += [x.custom_name for x in self.active_instruments[instr]]
                names += [self.active_instruments[instr][0].ophyd_class_name]
                names += ["numpy", "np", "StartTime", "ElapsedTime"]
        return names

    def remove_instance(self):
        """ """
        ind = self.config_tabs.currentIndex()
        name = self.config_tabs.tabText(ind)
        remove_dialog = QMessageBox.question(
            self,
            "Remove instrument?",
            f"Are you sure you want to remove the instrument {name}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if remove_dialog != QMessageBox.Yes:
            return
        self.config_tabs.removeTab(ind)
        instr_ind = self.tableWidget_instruments.selectedIndexes()[0]
        instr = self.tableWidget_instruments.item(instr_ind.row(), 0).text()
        self.active_instruments[instr].pop(ind)
        if not self.active_instruments[instr]:
            self.config_tabs.addTab(
                QLabel('Add an instrument\ninstance by clicking "+"'), "no instrument"
            )
            self.pushButton_remove.setEnabled(False)
        self.tableWidget_instruments.item(instr_ind.row(), 1).setText(
            str(len(self.active_instruments[instr]))
        )

    def build_table(self):
        """ """
        search_text = self.lineEdit_search.text()
        self.installed_instr = getInstalledDevices()
        self.tableWidget_instruments.clear()
        self.tableWidget_instruments.setRowCount(0)
        self.tableWidget_instruments.setHorizontalHeaderLabels(
            ["instrument", "number of instruments"]
        )
        i = 0
        for dev in sorted(self.installed_instr.keys()):
            if dev in device_handling.from_manual_controls:
                continue
            if search_text.lower() not in dev.lower():
                continue
            self.tableWidget_instruments.setRowCount(i + 1)
            item = QTableWidgetItem(dev)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

            if dev not in self.active_instruments:
                self.active_instruments[dev] = []
            item_n = QTableWidgetItem(str(len(self.active_instruments[dev])))
            item_n.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.tableWidget_instruments.setItem(i, 0, item)
            self.tableWidget_instruments.setItem(i, 1, item_n)
            i += 1
        self.tableWidget_instruments.resizeColumnsToContents()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    widge = Instrument_Config()
    widge.show()
    app.exec()
