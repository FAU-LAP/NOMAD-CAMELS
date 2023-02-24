from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # create central widget
        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.central_widget.updateLayout()


class CentralWidget(QWidget):

    def __init__(self):
        super().__init__()
        # create grid layout and add buttons
        self.layout = QGridLayout(self)
        self.buttons = []
        for i in range(5):
            button = QPushButton(f"Button {i+1}", self)
            button.setFixedSize(50, 50)
            self.buttons.append(button)
            self.layout.addWidget(button, i // 2, i % 2)

    def updateLayout(self):
        width = self.width()

        # calculate minimum column width based on button size
        button_width = self.buttons[0].width()
        min_column_width = button_width * 1.5

        # calculate number of columns based on current width
        columns = max(1, width // min_column_width)

        # calculate new positions of buttons based on columns
        positions = [(i // columns, i % columns) for i in range(5)]
        for button, position in zip(self.buttons, positions):
            self.layout.addWidget(button, *position)




if __name__ == '__main__':
    app = QApplication([])
    area = MainWindow()
    area.show()
    app.exec_()
