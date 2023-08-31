from PySide6.QtWidgets import QWidget, QTableWidgetItem, QLabel,  QTableWidget, QGridLayout, QLineEdit, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QFont

from nomad_camels.utility import variables_handling


class Channels_Check_Table(QWidget):
    """ """
    def __init__(self, parent, headerLabels=None, only_output=False,
                 info_dict=None, checkstrings=None, title='', channels=None):
        super().__init__(parent)
        self.channels = channels or variables_handling.channels
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.only_output = only_output
        self.headerLabels = headerLabels or []
        self.checkstrings = checkstrings or []
        self.info_dict = info_dict or {}
        if 'channel' not in self.info_dict:
            self.info_dict['channel'] = []
        for lab in self.headerLabels[2:]:
            if lab not in self.info_dict:
                self.info_dict[lab] = []

        layout = QGridLayout()
        self.tableWidget_channels = QTableWidget()
        self.tableWidget_channels.setHorizontalHeaderLabels(self.headerLabels)
        label_search = QLabel('Search:')
        self.tableWidget_channels.clicked.connect(self.tableWidget_channels.resizeColumnsToContents)
        self.lineEdit_search = QLineEdit()
        self.lineEdit_search.textChanged.connect(self.change_search)

        self.setLayout(layout)
        if title:
            title_label = QLabel(title)
            layout.addWidget(title_label, 0, 0, 1, 2)
            font = QFont()
            font.setBold(True)
            title_label.setStyleSheet('font-size: 9pt')
            title_label.setFont(font)
        layout.addWidget(label_search, 1, 0)
        layout.addWidget(self.lineEdit_search, 1, 1)
        layout.addWidget(self.tableWidget_channels, 2, 0, 1, 2)
        layout.setContentsMargins(0,0,0,0)
        self.build_channels_table()
        self.tableWidget_channels.itemChanged.connect(self.check_string)
        self.tableWidget_channels.clicked.connect(self.check_change)


    def context_menu(self, pos):
        """Generates the right-click-menu.
        There are entries for inserting (replace) and appending the
        variables, channels, functions and operators.

        Parameters
        ----------
        pos :
            

        Returns
        -------

        """
        if self.parent() and hasattr(self.parent(), 'loop_step'):
            prot = self.parent().loop_step.protocol
            variables_handling.protocol_variables = prot.variables
            prot.update_variables()
            variables_handling.loop_step_variables = prot.loop_step_variables
        menu = QMenu()
        # putting the returned actions somewhere is necessary, otherwise
        # there will be none inside the single menus
        (channel_menu, variable_menu, function_menu), _ = \
            variables_handling.get_menus(self.insert_variable)
        menu.addMenu(variable_menu)
        menu.addMenu(channel_menu)
        menu.addMenu(function_menu)
        # menu.addMenu(operator_menu)
        menu.addSeparator()
        (channel_menu2, variable_menu2, operator_menu2, function_menu2), __ = \
            variables_handling.get_menus(self.append_variable, 'Append')
        menu.addMenu(variable_menu2)
        menu.addMenu(channel_menu2)
        menu.addMenu(function_menu2)
        menu.addMenu(operator_menu2)
        menu.exec_(self.mapToGlobal(pos))

    def append_variable(self, val):
        """Used for the single actions of the context menu.

        Parameters
        ----------
        val :
            

        Returns
        -------

        """
        ind = self.tableWidget_channels.selectedIndexes()[0]
        item = self.tableWidget_channels.itemFromIndex(ind)
        text = item.text()
        item.setText(f'{text}{val}')

    def insert_variable(self, val):
        """Used for the single actions of the context menu.

        Parameters
        ----------
        val :
            

        Returns
        -------

        """
        ind = self.tableWidget_channels.selectedIndexes()[0]
        item = self.tableWidget_channels.itemFromIndex(ind)
        item.setText(f'{val}')


    def check_change(self, pos):
        """

        Parameters
        ----------
        pos :
            

        Returns
        -------

        """
        c = pos.column()
        if c != 0:
            return
        r = pos.row()
        item = self.tableWidget_channels.item(r, c)
        if item.checkState() != Qt.CheckState.Unchecked:
            color = variables_handling.get_color('blue')
        else:
            color = variables_handling.get_color('white')
        item.setBackground(QBrush(color))
        self.tableWidget_channels.item(r, c+1).setBackground(QBrush(color))

    def change_search(self):
        """ """
        self.update_info()
        self.build_channels_table()

    def get_info(self):
        """ """
        self.update_info()
        return self.info_dict

    def check_string(self, item):
        """If an element is part of the checkstrings, the item becomes
        green if valid, red otherwise and white if empty.

        Parameters
        ----------
        item :
            

        Returns
        -------

        """
        if item.column() not in self.checkstrings:
            return
        if self.tableWidget_channels.item(item.row(), 0).checkState() == Qt.CheckState.Unchecked and item.text() == '':
            color = variables_handling.get_color('white')
        elif variables_handling.check_eval(item.text()):
            color = variables_handling.get_color('green')
        else:
            color = variables_handling.get_color('red')
        item.setBackground(QBrush(color))

    def update_info(self):
        """ """
        channel_list = self.info_dict['channel']
        for k in self.info_dict:
            if k != 'channel':
                self.info_dict[k].clear()
        for i in range(self.tableWidget_channels.rowCount()):
            name = self.tableWidget_channels.item(i, 1).text()
            if name not in channel_list and self.tableWidget_channels.item(i, 0).checkState() != Qt.CheckState.Unchecked:
                channel_list.append(name)
            elif name in channel_list and self.tableWidget_channels.item(i, 0).checkState() == Qt.CheckState.Unchecked:
                channel_list.remove(name)
            if name in channel_list:
                n = channel_list.index(name)
                for j, lab in enumerate(self.headerLabels[2:]):
                    while len(self.info_dict[lab]) < n+1:
                        self.info_dict[lab].append(None)
                    item = self.tableWidget_channels.item(i, 2+j)
                    t = item.text()
                    if not t:
                        raise Exception(f'You need to enter a value for channel {name}!')
                    self.info_dict[lab][n] = t
        rems = []
        for channel in channel_list:
            if channel not in self.channels:
                rems.append(channel)
        for channel in rems:
            channel_list.remove(channel)



    def build_channels_table(self):
        """ """
        self.tableWidget_channels.clear()
        self.tableWidget_channels.setColumnCount(len(self.headerLabels))
        self.tableWidget_channels.setRowCount(0)
        self.tableWidget_channels.setHorizontalHeaderLabels(self.headerLabels)
        searchtext = self.lineEdit_search.text()
        channel_list = self.info_dict['channel']
        n = 0
        for i, channel in enumerate(sorted(self.channels, key=lambda x: x.lower())):
            if searchtext.lower() not in channel.lower() or (not isinstance(self.channels, list) and self.only_output and not self.channels[channel].output):
                continue
            metadata = self.channels[channel].get_meta_str()
            self.tableWidget_channels.setRowCount(n+1)
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if channel in channel_list:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            if metadata:
                item.setToolTip(metadata)
            self.tableWidget_channels.setItem(n, 0, item)
            item = QTableWidgetItem(channel)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            if metadata:
                item.setToolTip(metadata)
            self.tableWidget_channels.setItem(n, 1, item)
            pos = self.tableWidget_channels.model().createIndex(n, 0)
            self.check_change(pos)
            vals = []
            if channel in self.info_dict['channel']:
                n_chan = self.info_dict['channel'].index(channel)
                for lab in self.headerLabels[2:]:
                    vals.append(str(self.info_dict[lab][n_chan]))
            for j in range(len(self.headerLabels[2:])):
                item = QTableWidgetItem(vals[j] if vals else '')
                self.tableWidget_channels.setItem(n, j+2, item)
                self.check_string(item)
                if metadata:
                    item.setToolTip(metadata)
            n += 1
        self.tableWidget_channels.resizeColumnsToContents()


class Call_Functions_Table(QWidget):
    def __init__(self, parent=None, headerLabels=None,
                 info_dict=None, title='', functions=None):
        super().__init__(parent)
        self.functions = functions or variables_handling.get_non_channel_functions()
        self.headerLabels = headerLabels or []
        self.info_dict = info_dict or {}
        if 'functions' not in self.info_dict:
            self.info_dict['functions'] = []

        layout = QGridLayout()
        self.tableWidget_functions = QTableWidget()
        self.tableWidget_functions.setHorizontalHeaderLabels(self.headerLabels)
        label_search = QLabel('Search:')
        self.tableWidget_functions.clicked.connect(self.tableWidget_functions.resizeColumnsToContents)
        self.lineEdit_search = QLineEdit()
        self.lineEdit_search.textChanged.connect(self.change_search)

        self.setLayout(layout)
        if title:
            title_label = QLabel(title)
            layout.addWidget(title_label, 0, 0, 1, 2)
            font = QFont()
            font.setBold(True)
            title_label.setStyleSheet('font-size: 9pt')
            title_label.setFont(font)
        layout.addWidget(label_search, 1, 0)
        layout.addWidget(self.lineEdit_search, 1, 1)
        layout.addWidget(self.tableWidget_functions, 2, 0, 1, 2)
        layout.setContentsMargins(0,0,0,0)
        self.build_table()
        self.tableWidget_functions.clicked.connect(self.check_change)


    def check_change(self, pos):
        """ """
        c = pos.column()
        if c != 0:
            return
        r = pos.row()
        item = self.tableWidget_functions.item(r, c)
        if item.checkState() != Qt.CheckState.Unchecked:
            color = variables_handling.get_color('blue')
        else:
            color = variables_handling.get_color('white')
        item.setBackground(QBrush(color))
        self.tableWidget_functions.item(r, c + 1).setBackground(QBrush(color))

    def change_search(self):
        """ """
        self.update_info()
        self.build_table()

    def get_info(self):
        """ """
        self.update_info()
        return self.info_dict

    def update_info(self):
        """ """
        func_list = self.info_dict['functions']
        for k in self.info_dict:
            if k != 'functions':
                self.info_dict[k].clear()
        for i in range(self.tableWidget_functions.rowCount()):
            name = self.tableWidget_functions.item(i, 1).text()
            if name not in func_list and self.tableWidget_functions.item(i, 0).checkState() != Qt.CheckState.Unchecked:
                func_list.append(name)
            elif name in func_list and self.tableWidget_functions.item(i, 0).checkState() == Qt.CheckState.Unchecked:
                func_list.remove(name)
            if name in func_list:
                n = func_list.index(name)
                # for j, lab in enumerate(self.headerLabels[2:]):
                #     while len(self.info_dict[lab]) < n+1:
                #         self.info_dict[lab].append(None)
                #     item = self.tableWidget_functions.item(i, 2 + j)
                #     t = item.text()
                #     if not t:
                #         raise Exception(f'You need to enter a value for channel {name}!')
                #     self.info_dict[lab][n] = t
        rems = []
        for func in func_list:
            if func not in self.functions:
                rems.append(func)
        for func in rems:
            func_list.remove(func)



    def build_table(self):
        """ """
        self.tableWidget_functions.clear()
        self.tableWidget_functions.setColumnCount(len(self.headerLabels))
        self.tableWidget_functions.setRowCount(0)
        self.tableWidget_functions.setHorizontalHeaderLabels(self.headerLabels)
        searchtext = self.lineEdit_search.text()
        func_list = self.info_dict['functions']
        n = 0
        for i, func in enumerate(sorted(self.functions, key=lambda x: x.lower())):
            if searchtext.lower() not in func.lower() or not isinstance(self.functions, list):
                continue
            self.tableWidget_functions.setRowCount(n + 1)
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if func in func_list:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            self.tableWidget_functions.setItem(n, 0, item)
            item = QTableWidgetItem(func)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.tableWidget_functions.setItem(n, 1, item)
            pos = self.tableWidget_functions.model().createIndex(n, 0)
            self.check_change(pos)
            vals = []
            if func in self.info_dict['functions']:
                n_chan = self.info_dict['functions'].index(func)
                for lab in self.headerLabels[2:]:
                    vals.append(str(self.info_dict[lab][n_chan]))
            for j in range(len(self.headerLabels[2:])):
                item = QTableWidgetItem(vals[j] if vals else '')
                self.tableWidget_functions.setItem(n, j + 2, item)
            n += 1
        self.tableWidget_functions.resizeColumnsToContents()

