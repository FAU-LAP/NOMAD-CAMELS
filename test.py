from PyQt5.QtWidgets import QApplication, QScrollArea, QWidget, QVBoxLayout, QPushButton, QAbstractButton
from PyQt5.QtCore import Qt, QMimeData, QByteArray, QDataStream, QIODevice
from PyQt5.QtGui import QDrag

class MyButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)
        self.setFlat(True)
        self.setFixedHeight(50)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return

        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        mime_data = QMimeData()
        byte_array = QByteArray()
        data_stream = QDataStream(byte_array, QIODevice.WriteOnly)
        data_stream.writeString(self.objectName().encode())
        mime_data.setData('application/x-dnditemdata', byte_array)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
        drop_action = drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-dnditemdata'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-dnditemdata'):
            byte_array = event.mimeData().data('application/x-dnditemdata')
            data_stream = QDataStream(byte_array, QIODevice.ReadOnly)
            button_name = data_stream.readString()

            button = self.parent().findChild(QAbstractButton, button_name.decode())

            if button is not self:
                self.move(button.pos())
                button.move(event.pos())
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

class Example(QWidget):
    def __init__(self):
        super().__init__()

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumSize(500, 500)
        widget = QWidget(scroll_area)
        scroll_area.setWidget(widget)
        layout = QVBoxLayout(widget)

        for i in range(10):
            button = MyButton('Button {}'.format(i), widget)
            button.setObjectName('Button{}'.format(i))
            layout.addWidget(button)

        # self.setGeometry(300, 300, 300, 400)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
