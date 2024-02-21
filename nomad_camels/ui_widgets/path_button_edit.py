from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QStyle,
    QApplication,
    QDialog,
    QLabel,
    QDialogButtonBox,
)
from PySide6.QtCore import Signal, Qt

import os


class Path_Button_Edit(QWidget):
    """This class provides QLineEdit with a QPushButton, used to select
    a file-path, that is then displayed in the LineEdit.

    Parameters
    ----------

    Returns
    -------

    """

    path_changed = Signal(str)

    def __init__(
        self,
        parent=None,
        path="",
        default_dir="",
        file_extension="",
        select_directory=False,
        save_file=False,
    ):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        self.button = QPushButton("...")
        self.button.setIcon(
            QApplication.style().standardIcon(QStyle.SP_DialogOpenButton)
        )
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
        self.save_file = save_file

    def get_path(self):
        """ """
        return self.line.text()

    def set_path(self, path):
        """

        Parameters
        ----------
        path :


        Returns
        -------

        """
        self.line.setText(path)

    def choose_path(self):
        """ """
        try:
            direc = os.path.dirname(self.get_path()) or self.default_dir
        except OSError:
            direc = self.default_dir
        if self.select_directory:
            path = QFileDialog.getExistingDirectory(self, "Select Directory", dir=direc)
        elif self.save_file:
            path = QFileDialog.getSaveFileName(
                self, "Choose Filename", dir=direc, filter=self.file_extension
            )[0]
        else:
            path = QFileDialog.getOpenFileName(
                self, "Select File", dir=direc, filter=self.file_extension
            )[0]
        if path:
            self.line.setText(path)

    def changed(self):
        """ """
        self.path_changed.emit(self.get_path())


class Path_Button_Dialog(QDialog):
    def __init__(
        self,
        parent=None,
        path="",
        default_dir="",
        file_extension="",
        select_directory=False,
        save_file=False,
        title="",
        text="",
    ):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)

        if text:
            label = QLabel(text)
            layout.addWidget(label, 0, 0)
        self.pathEdit = Path_Button_Edit(
            self, path, default_dir, file_extension, select_directory, save_file
        )
        layout.addWidget(self.pathEdit, 1, 0)
        if title:
            self.setWindowTitle(title)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        layout.addWidget(self.buttonBox, 2, 0)

        self.path = ""

    def accept(self) -> None:
        self.path = self.pathEdit.get_path()
        super().accept()
