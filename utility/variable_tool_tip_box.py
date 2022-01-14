from PyQt5.QtWidgets import QLineEdit

class Variable_Box(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setToolTip('test')
