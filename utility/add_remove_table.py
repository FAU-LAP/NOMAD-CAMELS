from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

import numpy as np
import pandas as pd


class AddRemoveTable(QWidget):
    def __init__(self, addLabel='+', removeLabel='-', horizontal=True, editables=None, checkables=(), headerLabels=None, orderBy=None, parent=None, tableData=None):
        super().__init__(parent)
        layout = QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.checkables = checkables if not type(checkables) is int else [checkables]
        self.horizontal = horizontal
        self.orderBy = orderBy
        if headerLabels is None and tableData is not None:
            headerLabels = tableData.keys()
        elif tableData is None and headerLabels is not None:
            tableData = {}
            for label in headerLabels:
                tableData.update({label: []})
        elif tableData is None and headerLabels is None:
            raise Exception('Cannot create a table without Data Format (AddRemoveTable)')
        if type(tableData) is dict:
            tableData = pd.DataFrame(tableData)
        self.tableData = tableData
        if editables is None:
            editables = range(len(headerLabels))
        self.editables = editables if not type(editables) is int else [editables]

        self.addButton = QPushButton(addLabel)
        self.removeButton = QPushButton(removeLabel)

        self.table = QTableView()
        self.table_model = QStandardItemModel()
        self.table.setModel(self.table_model)
        layout.addWidget(self.addButton, 0, 0)
        layout.addWidget(self.removeButton, 0, 1)
        layout.addWidget(self.table, 1, 0, 1, 2)

        self.headerLabels = headerLabels
        if horizontal:
            self.table.verticalHeader().hide()
            self.table_model.setHorizontalHeaderLabels(headerLabels)
            self.table_model.setColumnCount(len(headerLabels))
        else:
            self.table.horizontalHeader().hide()
            self.table_model.setVerticalHeaderLabels(headerLabels)
            self.table_model.setRowCount(len(headerLabels))

        self.addButton.clicked.connect(lambda x: self.add())
        self.removeButton.clicked.connect(self.remove)
        self.load_table_data()

    def load_table_data(self):
        data = np.array(self.tableData)
        for dat in data:
            self.add(dat)

    def add(self, vals=None):
        if vals is None:
            vals = [''] * len(self.headerLabels)
        items = []
        for i in range(len(self.headerLabels)):
            item = QStandardItem(vals[i])
            item.setEditable(i in self.editables)
            item.setCheckable(i in self.checkables)
            items.append(item)
        if self.horizontal:
            self.table_model.appendRow(items)
        else:
            self.table_model.appendColumn(items)

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

    def update_table_data(self):
        self.tableData = {}
        for i, lab in enumerate(self.headerLabels):
            vals = []
            self.tableData.update({lab: vals})
            if self.horizontal:
                for j in range(self.table_model.rowCount()):
                    vals.append(self.table_model.item(i, j).text())
            else:
                for j in range(self.table_model.columnCount()):
                    vals.append(self.table_model.item(j, i).text())
        self.tableData = pd.DataFrame(self.tableData)

