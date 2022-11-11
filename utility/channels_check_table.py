from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QLabel, QComboBox, QTableWidget, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt
from main_classes.loop_step import Loop_Step, Loop_Step_Config

from gui.read_channels import Ui_read_channels_config

from utility import variables_handling, fit_variable_renaming


class Channels_Check_Table(QWidget):
    def __init__(self, parent, headerLabels=None, only_output=False,
                 info_dict=None):
        super().__init__(parent)
        self.only_output = only_output
        self.headerLabels = headerLabels or []
        self.info_dict = info_dict or {}
        if 'channel' not in info_dict:
            info_dict['channel'] = []
        for lab in headerLabels[2:]:
            if lab not in info_dict:
                info_dict[lab] = []

        layout = QGridLayout()
        self.tableWidget_channels = QTableWidget()
        self.tableWidget_channels.setHorizontalHeaderLabels(self.headerLabels)
        label_search = QLabel('Search:')
        self.lineEdit_search = QLineEdit()
        self.lineEdit_search.textChanged.connect(self.change_search)

        self.setLayout(layout)
        layout.addWidget(label_search, 0, 0)
        layout.addWidget(self.lineEdit_search, 0, 1)
        layout.addWidget(self.tableWidget_channels, 1, 0, 1, 2)
        layout.setContentsMargins(0,0,0,0)
        self.build_channels_table()

    def change_search(self):
        self.update_info()
        self.build_channels_table()

    def get_info(self):
        self.update_info()
        return self.info_dict

    def update_info(self):
        channel_list = self.info_dict['channel']
        for i in range(self.tableWidget_channels.rowCount()):
            name = self.tableWidget_channels.item(i, 1).text()
            if name not in channel_list and self.tableWidget_channels.item(i, 0).checkState() > 0:
                channel_list.append(name)
            elif name in channel_list and self.tableWidget_channels.item(i, 0).checkState() <= 0:
                channel_list.pop(name)
            if name in channel_list:
                n = channel_list.index(name)
                for j, lab in enumerate(self.headerLabels[2:]):
                    while len(self.info_dict[lab]) < n+1:
                        self.info_dict[lab].append(None)
                    item = self.tableWidget_channels.item(i, 2+j)
                    self.info_dict[lab][n] = item.text()



    def build_channels_table(self):
        self.tableWidget_channels.clear()
        self.tableWidget_channels.setColumnCount(len(self.headerLabels))
        self.tableWidget_channels.setRowCount(0)
        self.tableWidget_channels.setHorizontalHeaderLabels(self.headerLabels)
        searchtext = self.lineEdit_search.text()
        channel_list = self.info_dict['channel']
        n = 0
        for i, channel in enumerate(sorted(variables_handling.channels, key=lambda x: x.lower())):
            if searchtext not in channel or (self.only_output and not variables_handling.channels[channel].output):
                continue
            self.tableWidget_channels.setRowCount(n+1)
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if channel in channel_list:
                item.setCheckState(2)
            else:
                item.setCheckState(False)
            self.tableWidget_channels.setItem(n, 0, item)
            item = QTableWidgetItem(channel)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.tableWidget_channels.setItem(n, 1, item)
            n += 1
        self.tableWidget_channels.resizeColumnsToContents()
