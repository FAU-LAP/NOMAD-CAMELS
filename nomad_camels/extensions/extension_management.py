import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from nomad_camels.gui.extension_manager import Ui_Form
from PySide6.QtWidgets import QWidget

class Extension_Manager(Ui_Form, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    widge = Extension_Manager()
    widge.show()
    app.exec()
