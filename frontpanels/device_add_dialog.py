import json
import os

from gui.addDeviceDialog import Ui_Dialog_Add_Device
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QKeyEvent
from PyQt5.QtCore import Qt


import devices
from utility import treeView_functions

def getInstalledDevices():
    device_path = r'C:\Users\od93yces\FAIRmat\devices_drivers/'
    device_list = {}
    for f in os.listdir(device_path):
        full_path = f'{device_path}{f}'
        if f != 'Support' and os.path.isdir(full_path):
            files = os.listdir(full_path)
            info_file = f'{f}_info.json'
            if info_file not in files:
                continue
            with open(f'{full_path}/{info_file}', 'r') as file:
                info = json.load(file)
            device_list.update({info['name']: info})

    return device_list

def getAllDevices():
    return getInstalledDevices()


test_device_list = [devices.Test_Laser, devices.Test_SMU, devices.Test_PID]
device_dict = getInstalledDevices()

class AddDeviceDialog(QDialog, Ui_Dialog_Add_Device):
    """Dialog that handles adding new devices in the MainApp, should also download available drivers from the repository."""
    def __init__(self, active_devices_dict=None, parent=None):
        super(AddDeviceDialog, self).__init__(parent=parent)
        if active_devices_dict is None:
            active_devices_dict = {}
        self.active_devices_dict = active_devices_dict
        self.installed_devices_list = getInstalledDevices()

        self.setupUi(self)
        self.setWindowTitle('CECS - Add Device')

        self.item_model = QStandardItemModel(0,4)
        self.treeView_devices.setModel(self.item_model)
        self.treeView_devices.setColumnWidth(0, 200)
        self.item_model.setHeaderData(0, Qt.Horizontal, '')
        self.item_model.setHeaderData(1, Qt.Horizontal, 'installed')
        self.item_model.setHeaderData(2, Qt.Horizontal, 'version')
        self.item_model.setHeaderData(3, Qt.Horizontal, 'available version')

        active_devices = QStandardItem('Active Devices')
        active_devices.setEditable(False)
        all_devices = QStandardItem('All Devices')
        all_devices.setEditable(False)
        virtual_devices = QStandardItem('Virtual Devices')
        virtual_devices.setEditable(False)
        installed_devices = QStandardItem('Installed Devices')
        installed_devices.setEditable(False)
        by_tags = QStandardItem('Devices by tags')
        by_tags.setEditable(False)
        self.tags = []

        self.item_model.appendRow([active_devices])
        self.item_model.appendRow([installed_devices])
        self.item_model.appendRow([all_devices])
        self.item_model.appendRow([virtual_devices])
        self.item_model.appendRow([by_tags])
        self.build_tree()



        # connecting buttons
        self.lineEdit_search_tags.returnPressed.connect(self.search_by_tag)
        self.lineEdit_search_name.returnPressed.connect(self.search_by_name)

        self.treeView_devices.clicked.connect(self.tree_click)

        self.pushButton_activate_selected.clicked.connect(self.de_activate_device)

    def tree_click(self):
        index = self.treeView_devices.selectedIndexes()[0]
        dat = self.item_model.itemFromIndex(index).data()
        if dat is None:
            self.pushButton_activate_selected.setEnabled(False)
        elif dat.startswith('act:'):
            self.pushButton_activate_selected.setEnabled(True)
            self.pushButton_activate_selected.setText('Remove selected device')
        elif dat.startswith('inst:') or dat in self.installed_devices_list:
            self.pushButton_activate_selected.setEnabled(True)
            self.pushButton_activate_selected.setText('Add selected device')
        else:
            self.pushButton_activate_selected.setEnabled(False)


    def de_activate_device(self):
        ind = self.treeView_devices.selectedIndexes()[0]
        dat = self.item_model.itemFromIndex(ind).data()
        if dat.startswith('inst:'):
            dat = dat[5:]
        if dat.startswith('act:'):
            self.active_devices_dict.pop(dat[4:])
        elif dat in self.active_devices_dict:
            i = 2
            while True:
                name = f'{dat}_{i}'
                if name not in self.active_devices_dict:
                    self.active_devices_dict.update({name: device_dict[dat]})
                    break
                i += 1
        else:
            self.active_devices_dict.update({dat: device_dict[dat]})
        self.build_tree()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """Overwrites the keyPressEvent of the QDialog so that it does not close when pressing Enter/Return."""
        if a0.key() == Qt.Key_Enter or a0.key() == Qt.Key_Return:
            return
        super().keyPressEvent(a0)

    def search_by_name(self):
        """Called on pressing return inside the lineEdit_search_name.
        Calls the build_tree method with the text inside the lineEdit as search_text"""
        text = self.lineEdit_search_name.text()
        self.build_tree(search_text=text)

    def search_by_tag(self):
        """Called on pressing return inside the lineEdit_search_tags.
        Calls the build_tree method with the text inside the lineEdit as search_tag"""
        tag = self.lineEdit_search_tags.text()
        self.build_tree(search_tag=tag)

    def build_tree(self, search_text='', search_tag=''):
        """Builds the tree of devices.
        First it clears the tree and then iterates through all available devices in device_dict.
        If search_text is given, only devices whose name includes the string in search_text are added to the tree.
        If search_tag is given, only devices that have the exact tag given by search_tag are added to the tree."""
        for i in range(5):
            item = self.item_model.item(i,0)
            while item.rowCount() > 0:
                item.removeRow(0)
            self.tags = []
        for key in self.active_devices_dict:
            if search_text.lower() not in key.lower() or (search_tag and search_tag.lower() not in self.active_devices_dict[key]['tags']):
                continue
            item = QStandardItem(key)
            item.setEditable(False)
            item.setData(f'act:{key}')
            self.item_model.item(0,0).appendRow(item)
        for device in sorted(device_dict):
            if search_text.lower() not in device.lower() or (search_tag and search_tag.lower() not in device_dict[device].tags):
                continue
            if device in self.installed_devices_list:
                item = QStandardItem(device)
                item.setEditable(False)
                item.setData(f'inst:{device}')
                self.item_model.item(1,0).appendRow(item)
            item = QStandardItem(device)
            item.setEditable(False)
            item.setData(device)
            if device_dict[device]['virtual']:
                self.item_model.item(3,0).appendRow(item)
            else:
                self.item_model.item(2,0).appendRow(item)
            for tag in device_dict[device]['tags']:
                item = QStandardItem(device)
                item.setEditable(False)
                item.setData(device)
                if tag not in self.tags:
                    tag_item = QStandardItem(tag)
                    tag_item.setEditable(False)
                    tag_item.setData(tag)
                    self.item_model.item(4,0).appendRow([tag_item])
                    self.tags.append(tag)
                else:
                    ind = treeView_functions.getItemIndex(self.item_model, tag)
                    tag_item = self.item_model.itemFromIndex(ind)
                tag_item.appendRow([item])
