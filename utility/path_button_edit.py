from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QFileDialog, QStyle, QApplication
from PyQt5.QtCore import pyqtSignal

import os



class Path_Button_Edit(QWidget):
    path_changed = pyqtSignal(str)

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
        self.line.textChanged.connect(self.changed)

    def get_path(self):
        return self.line.text()

    def set_path(self, path):
        self.line.setText(path)

    def choose_path(self):
        try:
            direc = os.path.dirname(self.get_path())
        except OSError:
            direc = ''
        path = QFileDialog.getOpenFileName(self, 'Select File', directory=direc)[0]
        if path:
            self.line.setText(path)

    def changed(self):
        self.path_changed.emit(self.get_path())
