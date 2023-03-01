from PyQt5.QtWidgets import QPushButton, QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap
from PyQt5.QtCore import Qt




class ThreeDotsButton(QPushButton):
    def __init__(self, parent=None):
        super(ThreeDotsButton, self).__init__(parent)
        self.setFixedSize(100, 100)
        self.setIconSize(self.size())
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setText('test blubb aaa;ejk;saj')
        self.setStyleSheet("QPushButton {text-align: left; font-weight: bold; font-size: 10pt; padding-bottom: -60px; font-family: Calibri; }")



    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the brush and pen for the painter
        brush = QBrush(QColor(50, 50, 50))
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        # Draw three dots using the painter
        painter.drawEllipse(90, 73, 4.5, 4.5)
        painter.drawEllipse(90, 84, 4.5, 4.5)
        painter.drawEllipse(90, 93, 4.5, 4.5)
        super().paintEvent(event)

    def sizeHint(self):
        return self.minimumSizeHint()


if __name__ == '__main__':
    app = QApplication([])
    widge = QMainWindow()
    widge.setLayout(QHBoxLayout())
    button = ThreeDotsButton()
    button.clicked.connect(lambda x: print('hi'))
    widge.layout().addWidget(button)
    small_button = QPushButton('aaaa')
    widge.layout().addWidget(small_button)
    small_button.setGeometry(10, 10, 50, 50)
    widge.showMaximized()
    app.exec_()
