from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QTableView, QLabel, QComboBox, QMenu
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QBrush, QColor
from PyQt5.QtCore import Qt

import numpy as np
import pandas as pd

from utility import variables_handling


class AddRemoveTable(QWidget):
    def __init__(self, addLabel='+', removeLabel='-', horizontal=True, editables=None, checkables=(), headerLabels=None, orderBy=None, parent=None, tableData=None, title='', comboBoxes=None, subtables=None, growsize=True, checkstrings=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        layout = QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.checkables = checkables if not type(checkables) is int else [checkables]
        if checkstrings is None:
            checkstrings = []
        self.checkstrings = checkstrings if not type(checkstrings) is int else [checkstrings]
        self.horizontal = horizontal
        self.orderBy = orderBy
        self.comboBoxes = {} if comboBoxes is None else comboBoxes
        self.subtables = {} if subtables is None else subtables
        self.growsize = growsize
        self.boxes = []
        self.tables = []
        if headerLabels is None and tableData is not None:
            headerLabels = tableData.keys()
        elif tableData is None and headerLabels is not None:
            tableData = {}
        elif tableData is None and headerLabels is None:
            raise Exception('Cannot create a table without Data Format (AddRemoveTable)')
        if isinstance(tableData, dict):
            tableData = pd.DataFrame(tableData)
        for label in headerLabels:
            if label not in tableData:
                tableData.insert(headerLabels.index(label), label, ['']*len(tableData))
        self.tableData = tableData
        if editables is None:
            editables = range(len(headerLabels))
        self.editables = editables if not type(editables) is int else [editables]

        self.addButton = QPushButton(addLabel)
        self.removeButton = QPushButton(removeLabel)
        self.table = QTableView()
        self.table_model = QStandardItemModel()
        self.table.setModel(self.table_model)
        mover = 0
        if len(title):
            label = QLabel(title)
            layout.addWidget(label, 0, 0)
            font = QFont()
            font.setBold(True)
            label.setStyleSheet('font-size: 9pt')
            label.setFont(font)
            mover = 1
        layout.addWidget(self.addButton, 0, 0+mover)
        layout.addWidget(self.removeButton, 0, 1+mover)
        layout.addWidget(self.table, 1, 0, 1, 2+mover)

        self.headerLabels = headerLabels
        if horizontal:
            self.table.verticalHeader().hide()
            if len(headerLabels):
                self.table_model.setHorizontalHeaderLabels(headerLabels)
                self.table_model.setColumnCount(len(headerLabels))
            else:
                self.table_model.setColumnCount(1)
                self.table.horizontalHeader().hide()
        else:
            self.table.horizontalHeader().hide()
            if len(headerLabels):
                self.table_model.setVerticalHeaderLabels(headerLabels)
                self.table_model.setRowCount(len(headerLabels))
            else:
                self.table_model.setRowCount(1)
                self.table.verticalHeader().hide()

        self.addButton.clicked.connect(lambda x: self.add())
        self.removeButton.clicked.connect(self.remove)
        self.table.clicked.connect(self.table.resizeColumnsToContents)
        self.table.clicked.connect(self.table.resizeRowsToContents)
        self.load_table_data()
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.update_max_hight()
        self.table_model.itemChanged.connect(self.check_string)

    def update_max_hight(self):
        if self.growsize:
            self.setMaximumHeight(90 + self.table_model.rowCount()*100)
        else:
            self.setMaximumHeight(100)

    def load_table_data(self):
        if self.horizontal:
            while self.table_model.rowCount():
                self.table_model.removeRow(0)
        else:
            while self.table_model.columnCount():
                self.table_model.removeColumn(0)
        data = np.array(self.tableData)
        for dat in data:
            self.add(dat)

    def context_menu(self, pos):
        menu = QMenu()
        (channel_menu, variable_menu, operator_menu, function_menu), _ = variables_handling.get_menus(self.insert_variable)
        menu.addMenu(variable_menu)
        menu.addMenu(channel_menu)
        menu.addMenu(function_menu)
        menu.addMenu(operator_menu)
        menu.exec_(self.mapToGlobal(pos))

    def insert_variable(self, val):
        ind = self.table.selectedIndexes()[0]
        item = self.table_model.itemFromIndex(ind)
        text = item.text()
        item.setText(f'{text}{val}')

    def check_string(self, item):
        ind = item.index()
        pos = ind.column() if self.horizontal else ind.row()
        if pos not in self.checkstrings or item.text() == '':
            color = variables_handling.get_color('white')
        elif variables_handling.check_eval(item.text()):
            color = variables_handling.get_color('green')
        else:
            color = variables_handling.get_color('red')
        self.table_model.setData(self.table_model.indexFromItem(item), QBrush(color), Qt.BackgroundRole)

    def add(self, vals=None):
        if vals is None:
            vals = [''] * len(self.headerLabels) if len(self.headerLabels) else ''
        items = []
        box_indexes = []
        boxes = []
        table_indexes = []
        tables = []
        for i, name in enumerate(self.headerLabels):
            item = QStandardItem()
            if name in self.comboBoxes:
                box = QComboBox()
                for text in self.comboBoxes[name]:
                    box.addItem(text)
                self.boxes.append(box)
                box_indexes.append(i)
                boxes.append(box)
                if vals[i] in self.comboBoxes[name]:
                    box.setCurrentText(vals[i])
            elif name in self.subtables:
                if type(vals[i]) is not list:
                    vals[i] = []
                checksting = 0 if i in self.checkstrings else None
                table = AddRemoveTable(horizontal=self.horizontal, headerLabels=[], tableData=vals[i], growsize=False, checkstrings=checksting)
                self.tables.append(table)
                table_indexes.append(i)
                tables.append(table)
                if vals[i] in self.subtables[name]:
                    table.setCurrentText(vals[i])
            else:
                item = QStandardItem(str(vals[i]))
            item.setEditable(i in self.editables)
            item.setCheckable(i in self.checkables)
            items.append(item)
        if len(self.headerLabels) == 0:
            item = QStandardItem(vals)
            items.append(item)
        if self.horizontal:
            self.table_model.appendRow(items)
            for j, i in enumerate(box_indexes):
                index = self.table_model.index(self.table_model.rowCount()-1, i)
                self.table.setIndexWidget(index, boxes[j])
            for j, i in enumerate(table_indexes):
                index = self.table_model.index(self.table_model.rowCount()-1, i)
                self.table.setIndexWidget(index, tables[j])
        else:
            self.table_model.appendColumn(items)
            for j, i in enumerate(box_indexes):
                index = self.table_model.index(i, self.table_model.columnCount()-1)
                self.table.setIndexWidget(index, boxes[j])
            for j, i in enumerate(table_indexes):
                index = self.table_model.index(i, self.table_model.columnCount()-1)
                self.table.setIndexWidget(index, tables[j])
        for item in items:
            self.check_string(item)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.update_max_hight()

    def remove(self):
        try:
            index = self.table.selectedIndexes()[0]
        except IndexError:
            raise Exception('You need to select a row first!')
        row = index.row()
        col = index.column()
        if self.horizontal and row >= 0:
            self.table_model.removeRow(row)
        elif not self.horizontal and col >= 0:
            self.table_model.removeColumn(col)
        self.update_table_data()
        self.update_max_hight()

    def update_table_data(self):
        self.tableData = {}
        for i, lab in enumerate(self.headerLabels):
            vals = []
            self.tableData.update({lab: vals})
            if self.horizontal:
                for j in range(self.table_model.rowCount()):
                    ind = self.table_model.index(j, i)
                    if lab in self.comboBoxes:
                        vals.append(self.table.indexWidget(ind).currentText())
                    elif lab in self.subtables:
                        tab = self.table.indexWidget(ind)
                        tab.update_table_data()
                        vals.append(tab.tableData)
                    else:
                        try:
                            vals.append(int(self.table_model.item(j, i).text()))
                        except:
                            try:
                                vals.append(float(self.table_model.item(j, i).text()))
                            except:
                                vals.append(self.table_model.item(j, i).text())
            else:
                for j in range(self.table_model.columnCount()):
                    ind = self.table_model.index(i, j)
                    if lab in self.comboBoxes:
                        vals.append(self.table.indexWidget(ind).currentText())
                    elif lab in self.subtables:
                        tab = self.table.indexWidget(ind)
                        tab.update_table_data()
                        vals.append(tab.tableData)
                    else:
                        try:
                            vals.append(float(self.table_model.item(i, j).text()))
                        except:
                            vals.append(self.table_model.item(i, j).text())
        if len(self.headerLabels) == 0:
            self.tableData = []
            if self.horizontal:
                for j in range(self.table_model.rowCount()):
                    try:
                        self.tableData.append(float(self.table_model.item(j, 0).text()))
                    except:
                        self.tableData.append(self.table_model.item(j, 0).text())
            else:
                for j in range(self.table_model.columnCount()):
                    try:
                        self.tableData.append(float(self.table_model.item(0,j).text()))
                    except:
                        self.tableData.append(self.table_model.item(0,j).text())




