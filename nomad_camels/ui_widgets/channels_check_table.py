from PySide6.QtWidgets import (
    QWidget,
    QTableWidgetItem,
    QLabel,
    QTableWidget,
    QGridLayout,
    QLineEdit,
    QMenu,
    QVBoxLayout,
    QWidgetAction,
    QPushButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QFont, QStandardItem

from nomad_camels.utility import variables_handling


class CheckableTableWidgetItem(QTableWidgetItem):
    def __init__(self, checkState=Qt.Unchecked):
        super().__init__()
        # Set the item to be checkable and enabled
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        if isinstance(checkState, bool):
            # Convert boolean to Qt.CheckState
            checkState = Qt.Checked if checkState else Qt.Unchecked
        self.setCheckState(checkState)

    def __lt__(self, other):
        # When comparing two checkable items, compare based on checkState.
        # Here, we treat Qt.Checked (2) as greater than Qt.Unchecked (0)
        if isinstance(other, QTableWidgetItem):
            # Use the checkState value for comparison if both items are checkable
            if self.checkState() == Qt.Checked and other.checkState() == Qt.Unchecked:
                return True
            elif self.checkState() == Qt.Unchecked and other.checkState() == Qt.Checked:
                return False
            elif self.checkState() == Qt.Checked and other.checkState() == Qt.Checked:
                return self.text() < other.text()
            elif (
                self.checkState() == Qt.Unchecked and other.checkState() == Qt.Unchecked
            ):
                return self.text() < other.text()
            else:
                # If both are checkable but not checked, compare based on the text
                return self.text() < other.text()
        return super().__lt__(other)


class Channels_Check_Table(QWidget):
    """ """

    def __init__(
        self,
        parent,
        headerLabels=None,
        only_output=False,
        info_dict=None,
        checkstrings=None,
        title="",
        channels=None,
        use_configs=False,
        checkables=None,
        use_aliases=True,
    ):
        super().__init__(parent)
        if use_configs:
            self.channels = channels or variables_handling.config_channels
        else:
            self.channels = channels or variables_handling.get_channels(use_aliases)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.only_output = only_output
        self.headerLabels = headerLabels or []
        self.checkstrings = checkstrings or []
        self.checkables = checkables or []
        self.info_dict = info_dict or {}
        if "channel" not in self.info_dict:
            self.info_dict["channel"] = []
        for lab in self.headerLabels[2:]:
            if lab not in self.info_dict:
                self.info_dict[lab] = []

        layout = QGridLayout()
        self.tableWidget_channels = QTableWidget()
        self.tableWidget_channels.setHorizontalHeaderLabels(self.headerLabels)
        label_search = QLabel("Search:")
        self.tableWidget_channels.clicked.connect(
            self.tableWidget_channels.resizeColumnsToContents
        )
        self.lineEdit_search = QLineEdit()
        # Add default text to the search bar
        self.lineEdit_search.setPlaceholderText("Filter instruments ...")
        self.lineEdit_search.textChanged.connect(self.change_search)

        self.setLayout(layout)
        if title:
            title_label = QLabel(title)
            layout.addWidget(title_label, 0, 0, 1, 2)
            font = QFont()
            font.setBold(True)
            title_label.setStyleSheet("font-size: 9pt")
            title_label.setFont(font)
        layout.addWidget(label_search, 1, 0)
        layout.addWidget(self.lineEdit_search, 1, 1)
        layout.addWidget(self.tableWidget_channels, 2, 0, 1, 2)
        layout.setContentsMargins(0, 0, 0, 0)
        self.build_channels_table()
        self.tableWidget_channels.itemChanged.connect(self.check_string)
        self.tableWidget_channels.clicked.connect(self.check_change)
        self.tableWidget_channels.setSortingEnabled(True)
        self.tableWidget_channels.sortByColumn(1, Qt.AscendingOrder)
        self._revertable_last_checks = {}

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
        ind = self.tableWidget_channels.selectedIndexes()
        if not ind:
            return
        ind = ind[0]
        if ind.column() == 1:
            return
        if ind.column() == 0 or ind.column() in self.checkables:
            self.menu = QMenu()
            action_check = self.menu.addAction("Check whole column")
            action_check.triggered.connect(
                lambda: self._check_uncheck_all(ind.column(), uncheck=False)
            )
            action_uncheck = self.menu.addAction("Uncheck whole column")
            action_uncheck.triggered.connect(
                lambda: self._check_uncheck_all(ind.column(), uncheck=True)
            )
            if ind.column() in self._revertable_last_checks:
                self.menu.addSeparator()
                action_revert = self.menu.addAction("Revert last (un-)check all")
                action_revert.triggered.connect(
                    lambda: self._revert_last_checks(ind.column())
                )
            self.menu.exec_(self.mapToGlobal(pos))
            return
        if self.parent() and hasattr(self.parent(), "loop_step"):
            prot = self.parent().loop_step.protocol
            variables_handling.protocol_variables = prot.variables
            prot.update_variables()
            variables_handling.loop_step_variables = prot.loop_step_variables
        self.menu = QMenu()
        search_bar = QLineEdit(self.menu)
        search_bar.setPlaceholderText("Search...")
        # Setting up layout for the menu
        layout = QVBoxLayout()
        layout.addWidget(search_bar)
        container = QWidget()
        container.setLayout(layout)

        # Adding the container widget to the menu
        action = QWidgetAction(self.menu)
        action.setDefaultWidget(container)
        self.menu.addAction(action)

        # putting the returned actions somewhere is necessary, otherwise
        # there will be none inside the single menus
        (self.channel_menu, self.variable_menu, self.function_menu), _ = (
            variables_handling.get_menus(self.insert_variable)
        )
        self.menu.addMenu(self.channel_menu)
        self.menu.addMenu(self.variable_menu)
        self.menu.addMenu(self.function_menu)
        # menu.addMenu(operator_menu)
        self.menu.addSeparator()
        (
            self.channel_menu2,
            self.variable_menu2,
            operator_menu2,
            self.function_menu2,
        ), __ = variables_handling.get_menus(self.append_variable, "Append")
        self.menu.addMenu(self.channel_menu2)
        self.menu.addMenu(self.variable_menu2)
        self.menu.addMenu(self.function_menu2)
        self.menu.addMenu(operator_menu2)

        # Connect the search bar to the filtering function
        search_bar.textChanged.connect(self.filter_actions)

        self.menu.exec_(self.mapToGlobal(pos))

    def filter_actions(self, query):
        for self.menu in [
            self.channel_menu,
            self.variable_menu,
            self.function_menu,
            self.channel_menu2,
            self.variable_menu2,
            self.function_menu2,
        ]:
            for action in self.menu.actions():
                action.setVisible(query.lower() in action.text().lower())

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
        item.setText(f"{text}{val}")

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
        item.setText(f"{val}")

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
            color = variables_handling.get_color("blue")
        else:
            color = variables_handling.get_color("white")
        item.setBackground(QBrush(color))
        self.tableWidget_channels.item(r, c + 1).setBackground(QBrush(color))

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
        if (
            self.tableWidget_channels.item(item.row(), 0).checkState()
            == Qt.CheckState.Unchecked
            and item.text() == ""
        ):
            color = variables_handling.get_color("white")
        elif variables_handling.check_eval(item.text()):
            color = variables_handling.get_color("green")
        else:
            color = variables_handling.get_color("red")
        item.setBackground(QBrush(color))

    def update_info(self):
        """ """
        channel_list = self.info_dict["channel"]
        self.value_dict = self.info_dict.copy()
        for i in range(self.tableWidget_channels.rowCount()):
            name = self.tableWidget_channels.item(i, 1).text()
            if (
                name not in channel_list
                and self.tableWidget_channels.item(i, 0).checkState()
                != Qt.CheckState.Unchecked
            ):
                channel_list.append(name)
            elif (
                name in channel_list
                and self.tableWidget_channels.item(i, 0).checkState()
                == Qt.CheckState.Unchecked
            ):
                n = channel_list.index(name)
                channel_list.remove(name)
                for lab in self.headerLabels[2:]:
                    if n < len(self.info_dict[lab]):
                        self.info_dict[lab].pop(n)
            if name in channel_list:
                n = channel_list.index(name)
                for j, lab in enumerate(self.headerLabels[2:]):
                    while len(self.info_dict[lab]) < n + 1:
                        self.info_dict[lab].append(None)
                    item = self.tableWidget_channels.item(i, 2 + j)
                    if j + 2 in self.checkables:
                        t = item.text()
                        if t == "None":
                            t = self.value_dict[lab][n]
                        self.info_dict[lab][n] = (
                            item.checkState() == Qt.CheckState.Checked
                        )
                    else:
                        t = item.text()
                        if not t:
                            raise Exception(
                                f"You need to enter a value for channel {name}!"
                            )
                        if t == "None":
                            t = self.value_dict[lab][n]
                        self.info_dict[lab][n] = t
        rems = []
        for channel in channel_list:
            if channel not in self.channels:
                rems.append(channel)
        for channel in rems:
            channel_list.remove(channel)

    def build_channels_table(self):
        """ """
        header = self.tableWidget_channels.horizontalHeader()
        sort_column = header.sortIndicatorSection()
        sort_order = header.sortIndicatorOrder()
        self.tableWidget_channels.sortByColumn(1, Qt.AscendingOrder)
        self.tableWidget_channels.setSortingEnabled(False)
        self.tableWidget_channels.clear()
        self.tableWidget_channels.setColumnCount(len(self.headerLabels))
        self.tableWidget_channels.setRowCount(0)
        self.tableWidget_channels.setHorizontalHeaderLabels(self.headerLabels)
        searchtext = self.lineEdit_search.text()
        channel_list = self.info_dict["channel"]
        n = 0
        for i, channel in enumerate(sorted(self.channels, key=lambda x: x.lower())):
            if searchtext.lower() not in channel.lower() or (
                not isinstance(self.channels, list)
                and self.only_output
                and not self.channels[channel].output
            ):
                continue
            metadata = ""
            if not isinstance(self.channels, list):
                metadata = self.channels[channel].get_meta_str()
            self.tableWidget_channels.setRowCount(n + 1)
            state = channel in channel_list
            item = CheckableTableWidgetItem(checkState=state)
            # item = QTableWidgetItem()
            # item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            # if channel in channel_list:
            #     item.setCheckState(Qt.CheckState.Checked)
            # else:
            #     item.setCheckState(Qt.CheckState.Unchecked)
            if metadata:
                item.setToolTip(
                    f"Hint: right-click to (un-)check complete column\n\n{metadata}"
                )
            self.tableWidget_channels.setItem(n, 0, item)
            item = QTableWidgetItem(channel)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            if metadata:
                item.setToolTip(metadata)
            self.tableWidget_channels.setItem(n, 1, item)
            pos = self.tableWidget_channels.model().createIndex(n, 0)
            self.check_change(pos)
            vals = []
            if channel in self.info_dict["channel"]:
                n_chan = self.info_dict["channel"].index(channel)
                for lab in self.headerLabels[2:]:
                    if n_chan < len(
                        self.info_dict[lab]
                    ):  # Check if index is within range
                        vals.append(str(self.info_dict[lab][n_chan]))
                    else:
                        vals.append("")  # Append empty string if index is out of range
            for j in range(len(self.headerLabels[2:])):
                if j + 2 in self.checkables:
                    state = (
                        Qt.CheckState.Checked
                        if vals and vals[j] == "True"
                        else Qt.CheckState.Unchecked
                    )
                    item = CheckableTableWidgetItem(checkState=state)

                    # item = QTableWidgetItem()
                    # # set item checkable by user but set it to be not editable
                    # item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                    # item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    # item.setCheckState(
                    #     Qt.CheckState.Checked
                    #     if vals and vals[j] == "True"
                    #     else Qt.CheckState.Unchecked
                    # )
                    self.tableWidget_channels.setItem(n, j + 2, item)
                    item.setToolTip("Hint: right-click to (un-)check complete column")
                else:
                    item = QTableWidgetItem(vals[j] if vals else "")
                    self.tableWidget_channels.setItem(n, j + 2, item)
                    self.check_string(item)
                if metadata:
                    item.setToolTip(item.toolTip() + metadata)
            n += 1
        self.tableWidget_channels.resizeColumnsToContents()
        self.tableWidget_channels.setSortingEnabled(True)
        self.tableWidget_channels.sortByColumn(sort_column, sort_order)

    def _get_column_check_state(self, column):
        """Get the check state of all items in a specific column."""
        states = []
        for row in range(self.tableWidget_channels.rowCount()):
            item = self.tableWidget_channels.item(row, column)
            states.append(item.checkState())
        return states

    def _revert_last_checks(self, column):
        """Revert the last check/uncheck action for a specific column."""
        if column not in self._revertable_last_checks:
            return
        last_states = self._revertable_last_checks.pop(column)
        for row in range(self.tableWidget_channels.rowCount()):
            item = self.tableWidget_channels.item(row, column)
            if item:
                item.setCheckState(last_states[row])
                self.check_change(self.tableWidget_channels.model().index(row, column))

    def _check_uncheck_all(self, column, uncheck=False):
        """Check or uncheck all items in a specific column."""
        self._revertable_last_checks[column] = self._get_column_check_state(column)
        for row in range(self.tableWidget_channels.rowCount()):
            item = self.tableWidget_channels.item(row, column)
            if item:
                item.setCheckState(Qt.Unchecked if uncheck else Qt.Checked)
                self.check_change(self.tableWidget_channels.model().index(row, column))


class Call_Functions_Table(QWidget):
    def __init__(
        self, parent=None, headerLabels=None, info_dict=None, title="", functions=None
    ):
        super().__init__(parent)
        self.functions = functions or variables_handling.get_non_channel_functions()
        self.headerLabels = headerLabels or []
        self.info_dict = info_dict or {}
        if "functions" not in self.info_dict:
            self.info_dict["functions"] = []

        layout = QGridLayout()
        self.tableWidget_functions = QTableWidget()
        self.tableWidget_functions.setHorizontalHeaderLabels(self.headerLabels)
        label_search = QLabel("Search:")
        self.tableWidget_functions.clicked.connect(
            self.tableWidget_functions.resizeColumnsToContents
        )
        self.lineEdit_search = QLineEdit()
        self.lineEdit_search.textChanged.connect(self.change_search)

        self.setLayout(layout)
        if title:
            title_label = QLabel(title)
            layout.addWidget(title_label, 0, 0, 1, 2)
            font = QFont()
            font.setBold(True)
            title_label.setStyleSheet("font-size: 9pt")
            title_label.setFont(font)
        layout.addWidget(label_search, 1, 0)
        layout.addWidget(self.lineEdit_search, 1, 1)
        layout.addWidget(self.tableWidget_functions, 2, 0, 1, 2)
        layout.setContentsMargins(0, 0, 0, 0)
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
            color = variables_handling.get_color("blue")
        else:
            color = variables_handling.get_color("white")
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
        func_list = self.info_dict["functions"]
        for k in self.info_dict:
            if k != "functions":
                self.info_dict[k].clear()
        for i in range(self.tableWidget_functions.rowCount()):
            name = self.tableWidget_functions.item(i, 1).text()
            if (
                name not in func_list
                and self.tableWidget_functions.item(i, 0).checkState()
                != Qt.CheckState.Unchecked
            ):
                func_list.append(name)
            elif (
                name in func_list
                and self.tableWidget_functions.item(i, 0).checkState()
                == Qt.CheckState.Unchecked
            ):
                func_list.remove(name)
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
        func_list = self.info_dict["functions"]
        n = 0
        for i, func in enumerate(sorted(self.functions, key=lambda x: x.lower())):
            if searchtext.lower() not in func.lower() or not isinstance(
                self.functions, list
            ):
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
            if func in self.info_dict["functions"]:
                n_chan = self.info_dict["functions"].index(func)
                for lab in self.headerLabels[2:]:
                    vals.append(str(self.info_dict[lab][n_chan]))
            for j in range(len(self.headerLabels[2:])):
                item = QTableWidgetItem(vals[j] if vals else "")
                self.tableWidget_functions.setItem(n, j + 2, item)
            n += 1
        self.tableWidget_functions.resizeColumnsToContents()
