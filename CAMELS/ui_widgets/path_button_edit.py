from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QFileDialog, QStyle, QApplication
from PySide6.QtCore import Signal

import os



class Path_Button_Edit(QWidget):
    """This class provides QLineEdit with a QPushButton, used to select
    a file-path, that is then displayed in the LineEdit."""
    path_changed = Signal(str)

    def __init__(self, parent=None, path='', default_dir='', file_extension='',
                 select_directory=False):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        self.button = QPushButton('...')
        self.button.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.line = QLineEdit()
        layout.addWidget(self.line, 0, 0)
        layout.addWidget(self.button, 0, 1)
        if path:
            self.set_path(path)
        self.default_dir = default_dir
        self.button.clicked.connect(self.choose_path)
        self.line.textChanged.connect(self.changed)
        self.file_extension = file_extension
        self.select_directory = select_directory

    def get_path(self):
        return self.line.text()

    def set_path(self, path):
        self.line.setText(path)

    def choose_path(self):
        try:
            direc = os.path.dirname(self.get_path()) or self.default_dir
        except OSError:
            direc = self.default_dir
        if self.select_directory:
            path = QFileDialog.getExistingDirectory(self, 'Select Directory',
                                                    dir=direc)
        else:
            path = QFileDialog.getOpenFileName(self, 'Select File',
                                               dir=direc,
                                               filter=self.file_extension)[0]
        if path:
            self.line.setText(path)

    def changed(self):
        self.path_changed.emit(self.get_path())
