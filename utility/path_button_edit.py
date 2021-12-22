from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QFileDialog, QStyle, QApplication
from PyQt5.QtGui import QIcon



class Path_Button_Edit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        self.button = QPushButton('...')
        self.button.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.line = QLineEdit()
        layout.addWidget(self.line, 0, 0)
        layout.addWidget(self.button, 0, 1)
        self.button.clicked.connect(self.choose_path)

    def get_path(self):
        return self.line.text()

    def choose_path(self):
        path = QFileDialog.getOpenFileName(self, 'Select File')[0]
        self.line.setText(path)
