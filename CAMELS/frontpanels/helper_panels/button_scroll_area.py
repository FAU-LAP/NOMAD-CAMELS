from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QScrollArea, QMainWindow
from PyQt5.QtGui import QDrag
from PyQt5.QtCore import Qt, QMimeData

class DragButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            mimeData = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(Qt.MoveAction)

class BidirectionalDict:
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
        return self._forward.items()

    def keys(self):
        return self._forward.keys()

    def values(self):
        return self._forward.values()

    def get_key(self, value):
        return self._reverse[value]

    def get_value(self, key):
        return self._forward[key]

    def __repr__(self):
        return f"BidirectionalDict({self._forward})"




class DropArea(QWidget):
    def __init__(self):
        super().__init__()
        # self.initUI()
        self.buttons = BidirectionalDict()
        self.button_order = []
        self.button_size = 50
        layout = QGridLayout()
        # layout.setSpacing(10)
        for i in range(9):
            button = DragButton(f"Button {i+1}")
            button.setFixedSize(self.button_size, self.button_size)
            self.buttons[str(i)] = button
            layout.addWidget(button, i // 2, i % 2)
            self.button_order.append(str(i))
        self.setLayout(layout)
        self.setAcceptDrops(True)
        self.columnCount = 0
        self.rowCount = 0


    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        position = event.pos()
        event.setDropAction(Qt.MoveAction)
        event.accept()

        source_widget = event.source()
        layout = self.layout()

        drag_pos = self.buttons.get_key(source_widget)
        # drop_pos = self.buttons.get_key(self.childAt(position))
        drop_row, drop_col = self.get_drop_position(event.pos())
        if drop_row * self.columnCount + drop_col >= len(self.buttons):
            drop_col = len(self.buttons) - drop_row * self.columnCount - 1
        print(drop_row, drop_col)
        child_at = self.layout().itemAtPosition(drop_row, drop_col).widget()
        print(child_at.text())
        drop_pos = self.buttons.get_key(child_at)

        adding = 0
        if self.button_order.index(drag_pos) < self.button_order.index(drop_pos):
            adding = 1
        self.button_order.remove(drag_pos)
        insert_pos = self.button_order.index(drop_pos)
        self.button_order.insert(insert_pos + adding, drag_pos)
        self.updateLayout()
        return

    def get_drop_position(self, pos):
        rect = self.rect()
        center = rect.center()
        width = self.width()
        height = self.height()
        x_dist = (pos - center).x() + width/2
        y_dist = (pos - center).y() + height/2
        column_width = width / self.columnCount
        row_height = height / self.rowCount
        return y_dist // row_height, x_dist // column_width



    def updateLayout(self):
        width = self.width()

        # calculate minimum column width based on button size
        button_width = self.button_size
        min_column_width = button_width * 1.5

        # calculate number of columns based on current width
        columns = max(1, width // min_column_width)

        # calculate new positions of buttons based on columns
        positions = [(i // columns, i % columns) for i in range(len(self.buttons))]
        self.columnCount = columns
        self.rowCount = len(positions) // columns + (1 if len(positions) % columns else 0)
        for button, position in zip(self.button_order, positions):
            self.layout().addWidget(self.buttons[button], *position)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # create central widget
        self.central_widget = QScrollArea()
        self.drop_area = DropArea()
        self.central_widget.setWidget(self.drop_area)
        self.central_widget.setWidgetResizable(True)
        self.setCentralWidget(self.central_widget)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.drop_area.updateLayout()

if __name__ == '__main__':
    app = QApplication([])
    area = MainWindow()
    area.show()
    app.exec_()
