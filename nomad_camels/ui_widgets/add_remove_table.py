from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QTableView,
    QLabel,
    QComboBox,
    QMenu,
    QDialog,
    QDialogButtonBox,
    QMessageBox,
    QLineEdit,
    QVBoxLayout,
    QWidgetAction,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont, QBrush, QKeyEvent
from PySide6.QtCore import Qt, Signal

import numpy as np
import pandas as pd

from nomad_camels.utility import variables_handling


class AddRemoveTable(QWidget):
    """This widget provides a QTableView and two buttons for adding /
    removing rows / columns.

    Parameters
    ----------

    Returns
    -------

    """

    sizechange = Signal()
    added = Signal(int)
    removed = Signal(int)

    def __init__(
        self,
        addLabel="+",
        removeLabel="-",
        horizontal=True,
        editables=None,
        checkables=(),
        headerLabels=None,
        orderBy=None,
        parent=None,
        tableData=None,
        title="",
        comboBoxes=None,
        subtables=None,
        growsize=False,
        checkstrings=None,
        askdelete=False,
        fixedsize=False,
        enableds=None,
        default_values=None,
        add_tooltip=None,
        remove_tooltip=None,
    ):
        """

        Parameters
        ----------
        addLabel : str, default "+"
            The label of the add-button
        removeLabel : str, default "-"
            The label of the remove-button
        horizontal : bool, default True
            True if the header is horizontal (thus the data in columns),
            False if it is the other way round
        editables : int, list of int, default None
            Positions of the columns (if horizontal) that are editable,
            If None, all are
        checkables : int, list of int, default None
            Positions of the columns (if horizontal) that have a
            Checkbox, if None, none have
        headerLabels : list of str, default None
            The labels of the header, they are also used to provide the
            format of the data returned by the AddRemoveTable
        orderBy : None
            not used (yet)
        parent : QWidget
            Parent of the Widget
        tableData : dict, pd.DataFrame, list, default None
            The data that should be put into the table. Should have the
            format of headerLabels. If it is a dict, the format should
            best look like {"column1": [data1, data2, ...], ...}
            A list should be used, if the table is a subtable inside
            another one
        title : str, default ""
            adds a QLabel on the top-right with `title`. If an empty
            string, no label is added
        comboBoxes : dict of lists of str
            the keys of the dict specify in which columns (same name), a
            comboBox should be used, the corresponding value gives the
            possible choices of the comboBox
        subtables : dict of lists
            the keys of the dict specify in which columns (same name),
            an additional AddRemoveTable should be contained
        growsize : bool, default True
            Whether to increase the MaximumSize of the Widget when more
            data is contained
        checkstrings : int, list of int, default None
            Positions of the columns (if horizontal) that are to be
            checked for validity, if None, none are
        askdelete : bool, default False
            Whether to have a PopUp make sure, that the user wants to
            delete the selected column
        fixedsize : bool, default False
            Whether the widget should have a fixed size
        enableds : int, list of int, default None
            Positions of the columns (if horizontal) that are enabled,
            If None, all are
        default_values : dict, default None
            A dict with the default values for the table. The keys are
            the column names and the values are the default values. If
            a column is not in the dict, the default value is an empty
            string. If None, all default values are empty strings.
            The default values are used for new entries.
        """
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.askdelete = askdelete
        self.checkables = checkables if not type(checkables) is int else [checkables]
        if checkstrings is None:
            checkstrings = []
        self.checkstrings = (
            checkstrings if not type(checkstrings) is int else [checkstrings]
        )
        self.horizontal = horizontal
        self.orderBy = orderBy
        self.comboBoxes = {} if comboBoxes is None else comboBoxes
        self.subtables = {} if subtables is None else subtables
        self.default_values = {} if default_values is None else default_values
        self.growsize = growsize
        self.fixedsize = fixedsize
        self.boxes = []
        self.tables = []
        if headerLabels is None and tableData is not None:
            headerLabels = tableData.keys()
        elif tableData is None and headerLabels is not None:
            tableData = {}
        elif tableData is None and headerLabels is None:
            raise Exception(
                "Cannot create a table without Data Format (AddRemoveTable)"
            )
        if isinstance(tableData, dict):
            tableData = pd.DataFrame(tableData)
        for label in headerLabels:
            if label not in tableData:
                tableData.insert(
                    headerLabels.index(label), label, [""] * len(tableData)
                )
        self.tableData = tableData
        if editables is None:
            editables = range(len(headerLabels))
        self.editables = editables if not isinstance(editables, int) else [editables]
        if enableds is None:
            enableds = range(len(headerLabels))
        self.enableds = enableds if not isinstance(enableds, int) else [enableds]

        self.addButton = QPushButton(addLabel)
        if add_tooltip:
            self.addButton.setToolTip(add_tooltip)
        self.addButton.setMaximumHeight(24)
        self.addButton.setStyleSheet(
            "QPushButton {\n"
            "                                background-color: #4CAF50; \n"
            "                                color: white; \n"
            "                                border: none; \n"
            "                                padding: 0px; \n"
            "                                padding-bottom: 5px;\n"
            "                                text-align: center; \n"
            "                                text-decoration: none; \n"
            "                                font-size: 15px; \n"
            "                                margin: 2px 2px; \n"
            "                                border-radius: 6px;\n"
            "								font-weight: bold;\n"
            "                            }\n"
            "\n"
            "                            QPushButton:hover {\n"
            "                                background-color: #45a049;\n"
            "                            }\n"
            "\n"
            "                            QPushButton:disabled {\n"
            "                                background-color: #808080;\n"
            "                                color: white;\n"
            "                            }"
        )
        self.removeButton = QPushButton(removeLabel)
        if remove_tooltip:
            self.removeButton.setToolTip(remove_tooltip)
        self.removeButton.setMaximumHeight(24)
        self.removeButton.setStyleSheet(
            "QPushButton {\n"
            "                                background-color:  #FF3333; \n"
            "                                color: white; \n"
            "                                border: none; \n"
            "                                padding: 0px; \n"
            "                                padding-bottom: 5px;\n"
            "                                text-align: center; \n"
            "                                text-decoration: none; \n"
            "                                font-size: 15px; \n"
            "                                margin: 2px 2px; \n"
            "                                border-radius: 6px;\n"
            "								font-weight: bold;\n"
            "                            }\n"
            "\n"
            "            QPushButton:hover {\n"
            "                background-color: #B22222;\n"
            "            }"
            "\n"
            "                            QPushButton:disabled {\n"
            "                                background-color: #808080;\n"
            "                                color: white;\n"
            "                            }"
        )
        self.table = QTableView()
        self.table_model = QStandardItemModel()
        self.table.setModel(self.table_model)
        mover = 0
        if len(title):
            label = QLabel(title)
            layout.addWidget(label, 0, 0)
            font = QFont()
            font.setBold(True)
            label.setStyleSheet("font-size: 9pt")
            label.setFont(font)
            mover = 1
        layout.addWidget(self.addButton, 0, 0 + mover)
        layout.addWidget(self.removeButton, 0, 1 + mover)
        layout.addWidget(self.table, 1, 0, 1, 2 + mover)

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
        self.table.selectionModel().selectionChanged.connect(self.check_selection)
        self.check_selection()

    def check_selection(self):
        if self.table.selectedIndexes():
            self.removeButton.setEnabled(True)
        else:
            self.removeButton.setEnabled(False)

    def update_max_hight(self):
        """ """
        if self.growsize:
            self.setMaximumHeight(90 + self.table_model.rowCount() * 100)
            self.sizechange.emit()
        elif self.fixedsize:
            self.setMaximumHeight(100)
            self.setMaximumWidth(200)
        elif not self.horizontal:
            self.setMaximumHeight(30 * len(self.headerLabels) + 30)

    def change_table_data(self, tableData, change_focus=False):
        """

        Parameters
        ----------
        tableData :


        Returns
        -------

        """
        if isinstance(tableData, dict):
            tableData = pd.DataFrame(tableData)
        self.tableData = tableData
        self.load_table_data(change_focus)

    def load_table_data(self, change_focus=False):
        """Putting the `tableData` into the table."""
        if self.horizontal:
            while self.table_model.rowCount():
                self.table_model.removeRow(0)
        else:
            while self.table_model.columnCount():
                self.table_model.removeColumn(0)
        if isinstance(self.tableData, dict):
            self.tableData = pd.DataFrame(self.tableData)
        data = np.array(self.tableData)
        for dat in data:
            self.add(dat, change_focus)

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
        menu = QMenu()
        search_bar = QLineEdit(menu)
        search_bar.setPlaceholderText("Search...")
        # Setting up layout for the menu
        layout = QVBoxLayout()
        layout.addWidget(search_bar)
        container = QWidget()
        container.setLayout(layout)

        # Adding the container widget to the menu
        action = QWidgetAction(menu)
        action.setDefaultWidget(container)
        menu.addAction(action)

        # putting the returned actions somewhere is necessary, otherwise
        # there will be none inside the single menus
        (self.channel_menu, self.variable_menu, self.function_menu), _ = (
            variables_handling.get_menus(self.insert_variable)
        )
        menu.addMenu(self.channel_menu)
        menu.addMenu(self.variable_menu)
        menu.addMenu(self.function_menu)
        # menu.addMenu(operator_menu)
        menu.addSeparator()
        (
            self.channel_menu2,
            self.variable_menu2,
            operator_menu2,
            self.function_menu2,
        ), __ = variables_handling.get_menus(self.append_variable, "Append")
        menu.addMenu(self.channel_menu2)
        menu.addMenu(self.variable_menu2)
        menu.addMenu(self.function_menu2)
        menu.addMenu(operator_menu2)

        # Connect the search bar to the filtering function
        search_bar.textChanged.connect(self.filter_actions)

        menu.exec_(self.mapToGlobal(pos))

    def filter_actions(self, query):
        for menu in [
            self.channel_menu,
            self.variable_menu,
            self.function_menu,
            self.channel_menu2,
            self.variable_menu2,
            self.function_menu2,
        ]:
            for action in menu.actions():
                action.setVisible(query.lower() in action.text().lower())

    def append_variable(self, val):
        """Used for the single actions of the context menu.

        Parameters
        ----------
        val :


        Returns
        -------

        """
        ind = self.table.selectedIndexes()[0]
        item = self.table_model.itemFromIndex(ind)
        text = item.text()
        item.setText(f"{text}{val}")

    def insert_variable(self, val):
        """Used for the single actions of the context menu.

        Parameters
        ----------
        val :


        Returns
        -------

        """
        ind = self.table.selectedIndexes()[0]
        item = self.table_model.itemFromIndex(ind)
        item.setText(f"{val}")

    def check_string(self, item):
        """If an element is part of the checkstrings, the item becomes
        green if valid, red otherwise and white if empty.

        Parameters
        ----------
        item :


        Returns
        -------

        """
        ind = item.index()
        pos = ind.column() if self.horizontal else ind.row()
        if pos not in self.checkstrings or item.text() == "":
            color = variables_handling.get_color("white")
        elif variables_handling.check_eval(item.text()):
            color = variables_handling.get_color("green")
        else:
            color = variables_handling.get_color("red")
        self.table_model.setData(
            self.table_model.indexFromItem(item), QBrush(color), Qt.BackgroundRole
        )

    def add(self, vals=None, change_focus=False):
        """Add the `vals` to the table as a new line. Checks are done
        for each part, whether there should be a comboBox etc.

        Parameters
        ----------
        vals :
            (Default value = None)

        Returns
        -------

        """
        if vals is None:
            vals = [""] * len(self.headerLabels) if len(self.headerLabels) else ""
            if self.default_values:
                for i, name in enumerate(self.headerLabels):
                    if name in self.default_values:
                        vals[i] = self.default_values[name]
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
                table = AddRemoveTable(
                    horizontal=self.horizontal,
                    headerLabels=[],
                    tableData=vals[i],
                    growsize=False,
                    checkstrings=checksting,
                    fixedsize=True,
                )
                self.tables.append(table)
                table_indexes.append(i)
                tables.append(table)
                if vals[i] in self.subtables[name]:
                    table.setCurrentText(vals[i])
            elif i in self.checkables:
                item.setCheckable(True)
                item.setCheckState(
                    Qt.CheckState.Checked if vals[i] else Qt.CheckState.Unchecked
                )
            else:
                item = QStandardItem(str(vals[i]))
            item.setEditable(i in self.editables)
            item.setEnabled(i in self.enableds)
            items.append(item)
        if len(self.headerLabels) == 0:
            if self.comboBoxes:
                box = QComboBox()
                box.addItems(self.comboBoxes)
                self.boxes.append(box)
                box_indexes.append(0)
                boxes.append(box)
                if vals in self.comboBoxes:
                    box.setCurrentText(vals)
            item = QStandardItem(str(vals))
            items.append(item)
        if self.horizontal:
            self.table_model.appendRow(items)
            for j, i in enumerate(box_indexes):
                index = self.table_model.index(self.table_model.rowCount() - 1, i)
                self.table.setIndexWidget(index, boxes[j])
            for j, i in enumerate(table_indexes):
                index = self.table_model.index(self.table_model.rowCount() - 1, i)
                self.table.setIndexWidget(index, tables[j])
            # Set focus to the first editable cell in the newly added row
            focus_index = self.table_model.index(self.table_model.rowCount() - 1, 0)
            if change_focus:
                self.table.setCurrentIndex(focus_index)
                self.table.edit(focus_index)
        else:
            self.table_model.appendColumn(items)
            for j, i in enumerate(box_indexes):
                index = self.table_model.index(i, self.table_model.columnCount() - 1)
                self.table.setIndexWidget(index, boxes[j])
            for j, i in enumerate(table_indexes):
                index = self.table_model.index(i, self.table_model.columnCount() - 1)
                self.table.setIndexWidget(index, tables[j])
            # Set focus to the first editable cell in the newly added column
            focus_index = self.table_model.index(0, self.table_model.columnCount() - 1)
            if change_focus:
                self.table.setCurrentIndex(focus_index)
                self.table.edit(focus_index)
        for item in items:
            self.check_string(item)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.update_max_hight()
        if self.horizontal:
            self.added.emit(items[0].row())
        else:
            self.added.emit(items[0].column())
        self.check_selection()

    def remove(self):
        """ """
        try:
            index = self.table.selectedIndexes()[0]
        except IndexError:
            raise Exception("You need to select a row first!")
        if self.askdelete:
            entry = self.table_model.itemFromIndex(index).text()
            remove_dialog = QMessageBox.question(
                self,
                "Remove entry?",
                f"Are you sure you want to remove the entry {entry}?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if remove_dialog != QMessageBox.Yes:
                return
        row = index.row()
        col = index.column()
        if self.horizontal and row >= 0:
            self.table_model.removeRow(row)
            if not self.headerLabels and self.comboBoxes:
                self.boxes.pop(row)
            self.removed.emit(row)
        elif not self.horizontal and col >= 0:
            self.table_model.removeColumn(col)
            if not self.headerLabels and self.comboBoxes:
                self.boxes.pop(col)
            self.removed.emit(col)
        self.update_table_data()
        self.update_max_hight()
        self.check_selection()

    def update_table_data(self):
        """Reading all the data of the table, putting it as dict into
        `self.tableData` and returning it.

        Parameters
        ----------

        Returns
        -------

        """
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
                    elif i in self.checkables:
                        vals.append(
                            self.table_model.item(j, i).checkState()
                            != Qt.CheckState.Unchecked
                        )
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
            if self.comboBoxes:
                for box in self.boxes:
                    self.tableData.append(box.currentText())
            elif self.horizontal:
                for j in range(self.table_model.rowCount()):
                    try:
                        self.tableData.append(float(self.table_model.item(j, 0).text()))
                    except:
                        self.tableData.append(self.table_model.item(j, 0).text())
            else:
                for j in range(self.table_model.columnCount()):
                    try:
                        self.tableData.append(float(self.table_model.item(0, j).text()))
                    except:
                        self.tableData.append(self.table_model.item(0, j).text())
        return self.tableData


class AddRemoveDialoge(QDialog):
    """A QDialog providing an AddRemoveTable."""

    def __init__(
        self,
        addLabel="+",
        removeLabel="-",
        horizontal=True,
        editables=None,
        checkables=(),
        headerLabels=None,
        orderBy=None,
        parent=None,
        tableData=None,
        title="",
        comboBoxes=None,
        subtables=None,
        checkstrings=None,
        askdelete=False,
        default_values=None,
    ):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        self.table = AddRemoveTable(
            addLabel=addLabel,
            removeLabel=removeLabel,
            horizontal=horizontal,
            editables=editables,
            checkables=checkables,
            headerLabels=headerLabels,
            orderBy=orderBy,
            parent=self,
            tableData=tableData,
            title=title,
            comboBoxes=comboBoxes,
            subtables=subtables,
            growsize=False,
            checkstrings=checkstrings,
            askdelete=askdelete,
            default_values=default_values,
        )

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.table, 0, 0)
        layout.addWidget(self.buttonBox, 1, 0)
        self.setWindowTitle(title)
        self.table.sizechange.connect(self.adjustSize)
        self.adjustSize()
        self.setMinimumWidth(len(headerLabels) * 70)

    def get_data(self):
        """ """
        return self.table.update_table_data()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """Overwrites the keyPressEvent of the QDialog so that it does
        not close when pressing Enter/Return.

        Parameters
        ----------
        a0: QKeyEvent :


        Returns
        -------

        """
        if a0.key() == Qt.Key_Enter or a0.key() == Qt.Key_Return:
            return
        super().keyPressEvent(a0)


class MultiTableDialog(QDialog):
    """A QDialog providing an AddRemoveTable."""

    def __init__(
        self,
        table_args=[],  # list of dicts with arguments for AddRemoveTable
        parent=None,
        title="",
    ):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        self.tables = []
        max_labels = 0
        for args in table_args:
            table = AddRemoveTable(**args)
            table.sizechange.connect(self.adjustSize)
            self.tables.append(table)
            if "headerLabels" in args:
                max_labels = max(max_labels, len(args["headerLabels"]))

        layout = QGridLayout()
        self.setLayout(layout)
        for i, table in enumerate(self.tables):
            layout.addWidget(table, i, 0)
        layout.addWidget(self.buttonBox, len(self.tables), 0)
        self.setWindowTitle(title)
        self.adjustSize()
        self.setMinimumWidth(max_labels * 100)

    def get_data(self):
        """ """
        data = []
        for table in self.tables:
            data.append(table.update_table_data())
        return data

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """Overwrites the keyPressEvent of the QDialog so that it does
        not close when pressing Enter/Return.

        Parameters
        ----------
        a0: QKeyEvent :


        Returns
        -------

        """
        if a0.key() == Qt.Key_Enter or a0.key() == Qt.Key_Return:
            return
        super().keyPressEvent(a0)

    def hide_add_remove_buttons(self):
        """ """
        for table in self.tables:
            table.addButton.hide()
            table.removeButton.hide()
