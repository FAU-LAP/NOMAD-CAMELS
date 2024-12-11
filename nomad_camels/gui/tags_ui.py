import sys
from PySide6.QtCore import Qt, QRect, QPoint, QSize
from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
    QToolButton,
    QScrollArea,
    QFrame,
    QLayout,
)


class TagWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text

        # Tighter layout: less horizontal and vertical margins
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)  # smaller margins
        layout.setSpacing(2)  # reduce spacing between label and 'X'

        self.label = QLabel(text, self)
        layout.addWidget(self.label)

        # Smaller close button to appear more integrated
        self.close_button = QToolButton(self)
        self.close_button.setText("X")
        self.close_button.setFixedSize(12, 12)  # smaller button size
        self.close_button.clicked.connect(self.remove_self)

        # Style the button to blend well with the tag background
        self.close_button.setStyleSheet(
            """
        QToolButton {
            border: none; 
            padding: 0;
            margin: 0;
            font-weight: bold;
            color: #333;
            background: transparent;
        }
        QToolButton:hover {
            color: red;
        }
        """
        )

        layout.addWidget(self.close_button)

        # Style the tag widget as a cohesive "pill"
        self.setStyleSheet(
            """
        QWidget {
            background: #D0E9FF;
            border: 1px solid #8BBCE4;
            border-radius: 4px;
        }
        """
        )

    def remove_self(self):
        self.setParent(None)
        self.deleteLater()


class FlowLayout(QLayout):
    # A simple flow layout to arrange tags nicely
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self.itemList = []
        self.widgetList = []

    def get_all_tags(self):
        return [widget.text for widget in self.widgetList]

    def addWidget(self, widget):
        self.widgetList.append(widget)
        super().addWidget(widget)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.sizeHint())
        margins = self.contentsMargins()
        size += QSize(
            margins.left() + margins.right(), margins.top() + margins.bottom()
        )
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing()
            spaceY = self.spacing()
            nextX = x + wid.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + wid.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), wid.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, wid.sizeHint().height())

        return y + lineHeight - rect.y()
