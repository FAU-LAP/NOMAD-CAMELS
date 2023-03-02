from PyQt5.QtWidgets import QPushButton, QApplication, QMainWindow, QLabel, QStyle, QFrame
from PyQt5.QtGui import QPainter, QColor, QBrush, QDrag
from PyQt5.QtCore import Qt, QSize, QMimeData

from CAMELS.utility.variables_handling import get_color


class SimpleWrapLabel(QLabel):
    def __init__(self, text='', parent=None):
        if ' ' not in text:
            text = text.replace('_', ' ')
            text = text.replace('-', ' ')
        super().__init__(text=text, parent=parent)


    def setText(self, a0: str) -> None:
        if ' ' not in a0:
            a0 = a0.replace('_', ' ')
            a0 = a0.replace('-', ' ')
        super().setText(a0)


class Dots_Button(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.setIconSize(self.size())
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        # self.setStyleSheet("QPushButton {text-align: left; font-weight: bold; font-size: 10pt; padding-bottom: -60px; font-family: Calibri; }")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the brush and pen for the painter
        brush = QBrush(QColor(get_color('black')))
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        # Draw three dots using the painter
        painter.drawEllipse(90, 80, 4, 4)
        painter.drawEllipse(90, 87, 4, 4)
        painter.drawEllipse(90, 94, 4, 4)
        super().paintEvent(event)

    def sizeHint(self):
        return self.minimumSizeHint()


class Options_Run_Button(QFrame):
    def __init__(self, text='', size=100):
        super().__init__()
        self.label = SimpleWrapLabel(text, parent=self)
        self.label.setGeometry(5,0,size-20,size)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("QLabel {font-weight: bold; font-size: 11pt; font-family: Calibri;}")
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.button = Dots_Button(parent=self)
        self.button.setGeometry(0,0,size,size)
        self.small_button = QPushButton('run', parent=self)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        self.small_button.setIcon(icon)
        self.small_button.setIconSize(QSize(int(size/4), int(size/4)))
        self.small_button.setGeometry(int(size/4),5,int(size/2),int(size/3))

        self.setFixedSize(size,size)
        self.setFrameStyle(1)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            mimeData = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(Qt.MoveAction)

    def rename(self, new_name):
        self.label.setText(new_name)


if __name__ == '__main__':
    app = QApplication([])
    widge = QMainWindow()
    widget = Options_Run_Button('super mega test')
    # widge.setLayout(QHBoxLayout())
    # button = Options_Run_Button('s;aiouf;lwkeja;slkjfasd;lje')
    # widge.layout().addWidget(button)
    widget.show()
    app.exec_()
