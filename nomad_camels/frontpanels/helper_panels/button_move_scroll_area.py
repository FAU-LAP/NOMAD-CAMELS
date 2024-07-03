from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMenu,
    QDialog,
    QLabel,
    QWidget,
    QGridLayout,
    QPushButton,
    QScrollArea,
    QMainWindow,
    QTabWidget,
    QTabBar,
    QMessageBox,
    QComboBox,
)
from PySide6.QtGui import QDrag, QPixmap
from PySide6.QtCore import Qt, QMimeData, Signal, QByteArray, QMimeData


class DragButton(QPushButton):
    """ """

    def __init__(self, text):
        super().__init__(text)

    def mouseMoveEvent(self, event):
        """

        Parameters
        ----------
        event :


        Returns
        -------

        """
        if event.buttons() == Qt.LeftButton:
            mimeData = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(Qt.MoveAction)


class BidirectionalDict:
    """ """

    def __init__(self):
        self._forward = {}
        self._reverse = {}

    def __getitem__(self, key):
        return self._forward[key]

    def __setitem__(self, key, value):
        self._forward[key] = value
        self._reverse[value] = key

    def __delitem__(self, key):
        value = self._forward.pop(key)
        del self._reverse[value]

    def __len__(self):
        return len(self._forward)

    def __iter__(self):
        return iter(self._forward)

    def items(self):
        """ """
        return self._forward.items()

    def keys(self):
        """ """
        return self._forward.keys()

    def values(self):
        """ """
        return self._forward.values()

    def get_key(self, value):
        """

        Parameters
        ----------
        value :


        Returns
        -------

        """
        return self._reverse[value]

    def get_value(self, key):
        """

        Parameters
        ----------
        key :


        Returns
        -------

        """
        return self._forward[key]

    def pop(self, key):
        """

        Parameters
        ----------
        key :


        Returns
        -------

        """
        val = self._forward.pop(key)
        self._reverse.pop(val)
        return val

    def __repr__(self):
        return f"BidirectionalDict({self._forward})"

    def clear(self):
        self._forward.clear()
        self._reverse.clear()


class DropArea(QWidget):
    """ """

    order_changed = Signal(list)

    def __init__(self, button_wdith: int):
        super().__init__()
        # self.initUI()
        self.buttons = BidirectionalDict()
        self.button_order = []
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setAcceptDrops(True)
        self.columnCount = 0
        self.rowCount = 0

        self.min_column_width = button_wdith + 1

    def dragEnterEvent(self, event):
        """

        Parameters
        ----------
        event :


        Returns
        -------

        """
        event.accept()

    def dropEvent(self, event):
        """

        Parameters
        ----------
        event :


        Returns
        -------

        """
        event.setDropAction(Qt.MoveAction)
        event.accept()

        source_widget = event.source()

        if not source_widget in self.buttons.values():
            return
        drag_pos = self.buttons.get_key(source_widget)
        drop_row, drop_col = self.get_drop_position(event.pos())
        if drop_row * self.columnCount + drop_col >= len(self.buttons):
            drop_col = int(len(self.buttons) - drop_row * self.columnCount - 1)
        child_at = self.layout().itemAtPosition(drop_row, drop_col).widget()
        drop_pos = self.buttons.get_key(child_at)

        if drag_pos == drop_pos:
            return
        adding = 0
        if self.button_order.index(drag_pos) < self.button_order.index(drop_pos):
            adding = 1
        self.button_order.remove(drag_pos)
        insert_pos = self.button_order.index(drop_pos)
        self.button_order.insert(insert_pos + adding, drag_pos)
        self.updateLayout()
        self.order_changed.emit(self.button_order)

    def get_drop_position(self, pos):
        """

        Parameters
        ----------
        pos :


        Returns
        -------

        """
        rect = self.rect()
        center = rect.center()
        width = self.width()
        height = self.height()
        x_dist = (pos - center).x() + width / 2
        y_dist = (pos - center).y() + height / 2
        column_width = width / self.columnCount
        row_height = height / self.rowCount
        return int(y_dist // row_height), int(x_dist // column_width)

    def updateLayout(self):
        """ """
        width = self.width()

        # calculate number of columns based on current width
        columns = max(1, width // self.min_column_width)

        # calculate new positions of buttons based on columns
        positions = [(i // columns, i % columns) for i in range(len(self.buttons))]
        self.columnCount = columns
        self.rowCount = len(positions) // columns + (
            1 if len(positions) % columns else 0
        )
        for button, position in zip(self.button_order, positions):
            self.layout().addWidget(self.buttons[button], *position)


class Drop_Scroll_Area(QScrollArea):
    """ """

    order_changed = Signal(list)

    def __init__(self, parent=None, button_width=120, button_height=120):
        super().__init__(parent=parent)
        self.drop_area = DropArea(button_width)
        self.setWidget(self.drop_area)
        self.setWidgetResizable(True)
        self.drop_area.updateLayout()
        self.button_width = button_width
        self.button_height = button_height
        self.setMinimumWidth(button_width)
        self.setMinimumHeight(button_height)
        self.drop_area.order_changed.connect(self.order_changed.emit)

    def resizeEvent(self, a0):
        """

        Parameters
        ----------
        a0 :


        Returns
        -------

        """
        super().resizeEvent(a0)
        self.updateLayout()

    def updateLayout(self):
        """ """
        self.drop_area.updateLayout()

    def add_button(self, button, name):
        """

        Parameters
        ----------
        button :

        name :


        Returns
        -------

        """
        button.setFixedSize(self.button_width, self.button_height)
        self.drop_area.buttons[name] = button
        self.drop_area.button_order.append(name)
        self.drop_area.updateLayout()

    def remove_button(self, name):
        """

        Parameters
        ----------
        name :


        Returns
        -------

        """
        button = self.drop_area.buttons.pop(name)
        self.drop_area.button_order.remove(name)
        self.drop_area.updateLayout()
        button.deleteLater()

    def clear_area(self):
        for button in self.drop_area.buttons:
            self.drop_area.buttons[button].deleteLater()
        self.drop_area.buttons.clear()
        self.drop_area.button_order.clear()

    def get_button_order(self):
        """ """
        return self.drop_area.button_order

    def rename_button(self, old_name, new_name):
        """

        Parameters
        ----------
        old_name :

        new_name :


        Returns
        -------

        """
        button = self.drop_area.buttons.pop(old_name)
        self.drop_area.buttons[new_name] = button
        ind = self.drop_area.button_order.index(old_name)
        self.drop_area.button_order.pop(ind)
        self.drop_area.button_order.insert(ind, new_name)
        button.rename(new_name)
        return button

    def disable_run_buttons(self):
        """ """
        for button in self.drop_area.buttons.values():
            button.small_button.setEnabled(False)

    def enable_run_buttons(self):
        """ """
        for button in self.drop_area.buttons.values():
            button.small_button.setEnabled(True)

    def disable_single_run(self, name):
        """

        Parameters
        ----------
        name :


        Returns
        -------

        """
        if name in self.drop_area.buttons:
            self.drop_area.buttons[name].small_button.setEnabled(False)

    def enable_single_run(self, name):
        """

        Parameters
        ----------
        name :


        Returns
        -------

        """
        if name in self.drop_area.buttons:
            self.drop_area.buttons[name].small_button.setEnabled(True)


class RenameTabWidget(QTabWidget):
    order_changed = Signal(list)

    def __init__(self, parent=None, tab_button_dict=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.tabBar().setMovable(True)

        # Add the "plus" tab
        self.plus_tab = QPushButton("+")
        self.plus_tab.setFlat(True)
        self.plus_tab.setFocusPolicy(Qt.NoFocus)
        self.plus_tab.clicked.connect(self.create_new_tab)

        # Add the plus tab
        self.tab_button_dict = tab_button_dict or {}
        self.all_buttons = []
        self.editing_old_name = ""
        self.addPlusTab()

        # Add a context menu to the tab bar
        self.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabBar().customContextMenuRequested.connect(self.context_menu)

    def addPlusTab(self):
        self.addTab(QWidget(), "")
        self.tabBar().setTabButton(self.count() - 1, QTabBar.RightSide, self.plus_tab)
        self.plus_tab.setStyleSheet(
            """
            QPushButton {
                background-color: #999999; /* Dark grey */
                border: none; /* Remove border for a cleaner look */
                color: white; /* Text color */
                padding: 8px 16px; /* Adjust padding as needed */
                border-radius: 10px; /* Rounded corners with a radius of 10px */
            }
            QPushButton:hover {
                background-color: #777777; /* Slightly lighter grey on hover */
            }
            QPushButton:pressed {
                background-color: #444444; /* Slightly darker grey when pressed */
            }
            """
        )

    def context_menu(self, pos):
        tab_index = self.tabBar().tabAt(pos)
        if tab_index == -1 or self.tabText(tab_index) == "":
            return
        menu = QMenu()
        menu.addAction("Add Tab", self.create_new_tab)
        menu.addAction("Remove Tab", lambda: self.tab_removing(tab_index))
        menu.addSeparator()
        menu.addAction("Rename Tab", lambda: self.rename_tab(tab_index))
        menu.exec(self.tabBar().mapToGlobal(pos))

    def tab_removing(self, index):
        if self.tabText(index) == "":
            return
        delete_question = QMessageBox.question(
            self,
            "Remove Tab",
            f"Are you sure you want to delete the tab '{self.tabText(index)}'?\nAll protocols inside the tab will be deleted as well!",
            QMessageBox.Yes | QMessageBox.No,
        )
        if delete_question != QMessageBox.Yes:
            return
        self.removeTab(index)

    def rename_tab(self, index):
        if self.tabText(index) == "":
            return
        old_name = self.tabText(index)
        line_edit = QLineEdit(old_name)
        line_edit.selectAll()
        line_edit.editingFinished.connect(
            lambda: self.handle_editing_finished(index, line_edit)
        )
        self.tabBar().setTabText(index, "")
        self.tabBar().setTabButton(index, QTabBar.RightSide, line_edit)
        self.editing_old_name = old_name
        line_edit.setFocus()

    def handle_editing_finished(self, index, line_edit):
        old_name = self.editing_old_name
        new_name = line_edit.text()
        if new_name:
            self.tabBar().setTabText(index, new_name)
        else:
            self.tabBar().setTabText(index, old_name)
        self.tabBar().setTabButton(index, QTabBar.RightSide, None)
        self.tab_button_dict[new_name] = self.tab_button_dict.pop(old_name)

    def updateLayout(self):
        for tab in range(self.count() - 1):  # Skip the last tab (plus tab)
            self.widget(tab).updateLayout()

    def get_tab_by_name(self, name, make_new=False):
        for i in range(self.count() - 1):  # Skip the last tab (plus tab)
            if self.tabText(i) == name:
                return self.widget(i)
        if make_new:
            tab = Drop_Scroll_Area()
            self.insertTab(self.count() - 1, tab, name)  # Insert before the plus tab
            return tab
        return None

    def add_button(self, button, name, tab_name=""):
        self.all_buttons.append(button)
        widget = self.get_tab_by_name(tab_name, make_new=True)
        widget.add_button(button, name)

    def remove_button(self, name):
        for i in range(self.count() - 1):  # Skip the last tab (plus tab)
            try:
                self.widget(i).remove_button(name)
            except KeyError:
                pass

    def clear_area(self):
        for i in range(self.count() - 1):  # Skip the last tab (plus tab)
            self.widget(i).clear_area()

    def get_button_order(self, tab_name=""):
        for i in range(self.count() - 1):  # Skip the last tab (plus tab)
            if self.tabText(i) == tab_name:
                return self.widget(i).get_button_order()
        return []

    def rename_button(self, old_name, new_name):
        for i in range(self.count() - 1):  # Skip the last tab (plus tab)
            try:
                return self.widget(i).rename_button(old_name, new_name)
            except KeyError:
                pass

    def disable_run_buttons(self):
        for i in range(self.count() - 1):  # Skip the last tab (plus tab)
            self.widget(i).disable_run_buttons()

    def enable_run_buttons(self):
        for i in range(self.count() - 1):  # Skip the last tab (plus tab)
            self.widget(i).enable_run_buttons()

    def disable_single_run(self, name):
        for i in range(self.count() - 1):  # Skip the last tab (plus tab)
            self.widget(i).disable_single_run(name)

    def enable_single_run(self, name):
        for i in range(self.count() - 1):  # Skip the last tab (plus tab)
            self.widget(i).enable_single_run(name)

    def create_new_tab(self):
        name = "New Tab"
        i = 1
        while name in self.tab_button_dict:
            name = f"New Tab {i}"
            i += 1
        new_tab = Drop_Scroll_Area()
        self.insertTab(self.count() - 1, new_tab, name)  # Insert before the plus tab
        self.tab_button_dict[name] = []
        new_tab.order_changed.connect(self.update_order)

    def addTab(self, widget, name):
        super().addTab(widget, name)
        if name not in self.tab_button_dict and name != "":
            self.tab_button_dict[name] = []
        if name != "":
            widget.order_changed.connect(self.update_order)

    def get_active_tab(self):
        return self.tabText(self.currentIndex())

    def update_order(self):
        for i in range(self.count() - 1):  # Skip the last tab (plus tab)
            tab_name = self.tabText(i)
            self.tab_button_dict[tab_name] = self.widget(i).get_button_order()


class MoveDialog(QDialog):
    def __init__(self, parent=None, f=Qt.WindowFlags(), button_name=""):
        super().__init__(parent, f)
        self.setWindowTitle(f"Move {button_name}")
        layout = QGridLayout()
        self.setLayout(layout)
        self.label = QLabel(f'Select the tab where to move "{button_name}"')
        self.combo = QComboBox()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.label, 0, 0, 1, 2)
        layout.addWidget(self.combo, 1, 0, 1, 2)
        layout.addWidget(self.ok_button, 2, 0)
        layout.addWidget(self.cancel_button, 2, 1)

    def add_tabs_from_widget(self, widget):
        for i in range(widget.count()):
            self.combo.addItem(widget.tabText(i))

    def get_tab(self):
        return self.combo.currentText()


if __name__ == "__main__":
    app = QApplication([])
    main_window = QMainWindow()
    tabbing = RenameTabWidget()
    main_window.setCentralWidget(tabbing)

    area1 = Drop_Scroll_Area()
    tabbing.addTab(area1, "Tab 1")
    area2 = Drop_Scroll_Area()
    tabbing.addTab(area2, "Tab 2")
    for i in range(15):
        area1.add_button(DragButton(f"A {i}"), str(i))
        area2.add_button(DragButton(f"B {i}"), str(i))
    main_window.show()
    app.exec()
