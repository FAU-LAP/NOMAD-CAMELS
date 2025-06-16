from PySide6.QtWidgets import (
    QPushButton,
    QApplication,
    QMainWindow,
    QLabel,
    QStyle,
    QFrame,
    QMenu,
    QMessageBox,
)
from PySide6.QtGui import QPainter, QColor, QBrush, QAction, QDrag
from PySide6.QtCore import Qt, QSize, QMimeData, Signal, SIGNAL

from nomad_camels.utility.variables_handling import get_color


class SimpleWrapLabel(QLabel):
    """ """

    def __init__(self, text="", parent=None):
        if " " not in text:
            text = text.replace("_", " ")
            text = text.replace("-", " ")
        super().__init__(text=text, parent=parent)

    def setText(self, a0: str) -> None:
        """

        Parameters
        ----------
        a0: str :


        Returns
        -------

        """
        if " " not in a0:
            a0 = a0.replace("_", " ")
            a0 = a0.replace("-", " ")
        super().setText(a0)


class Dots_Button(QPushButton):
    """ """

    def __init__(self, parent=None, size=100):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.setIconSize(self.size())
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        # self.setStyleSheet("QPushButton {text-align: left; font-weight: bold; font-size: 10pt; padding-bottom: -60px; font-family: Calibri; }")

    def paintEvent(self, event):
        """

        Parameters
        ----------
        event :


        Returns
        -------

        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the brush and pen for the painter
        brush = QBrush(QColor(get_color("black")))
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        # Draw three dots using the painter
        size = self.size().width()
        painter.drawEllipse(size - 10, size - 20, 4, 4)
        painter.drawEllipse(size - 10, size - 13, 4, 4)
        painter.drawEllipse(size - 10, size - 6, 4, 4)
        super().paintEvent(event)

    def sizeHint(self):
        """ """
        return self.minimumSizeHint()


class Options_Run_Button(QFrame):
    """ """

    build_asked = Signal()
    external_asked = Signal()
    data_path_asked = Signal()
    del_asked = Signal()
    move_asked = Signal()
    duplicate_asked = Signal()

    def __init__(self, text="", size=120, small_text="run", protocol_options=True):
        super().__init__()
        self.label = SimpleWrapLabel(text, parent=self)
        self.label.setGeometry(5, 0, size - 20, size)
        self.label.setWordWrap(True)
        self.label.setStyleSheet(
            "QLabel {font-weight: bold; font-size: 11pt; font-family: Calibri;}"
        )
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.button = Dots_Button(parent=self, size=size)
        self.button.setGeometry(0, 0, size, size)
        self.small_button = QPushButton(small_text, parent=self)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        self.small_button.setIcon(icon)
        if protocol_options:
            self.small_button.setIconSize(QSize(int(size / 5), int(size / 5)))
            self.small_button.setGeometry(5, 5, size - 10, int(size / 4))
            self.queue_button = QPushButton("queue", parent=self)
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_CommandLink)
            self.queue_button.setIcon(icon)
            self.queue_button.setIconSize(QSize(int(size / 5), int(size / 5)))
            self.queue_button.setGeometry(5, 10 + size // 4, size - 10, int(size / 4))
            self.button.setToolTip(
                "open the protocol settings / measurement sequence\nright-click for more options"
            )
            self.small_button.setToolTip("run this protocol right away")
            self.queue_button.setToolTip(
                "queue this protocol\nyou can set the protocol's variables for this specific run"
            )
        else:
            self.small_button.setIconSize(QSize(int(size / 4), int(size / 4)))
            self.small_button.setGeometry(5, 5, size - 10, int(size / 3))
            self.queue_button = None
            self.button.setToolTip(
                "open the settings of the manual control\nright-click for more options"
            )
            self.small_button.setToolTip("start the manual control")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.options_menu)
        self.config_function = None
        self.run_function = None
        self.build_function = None
        self.external_function = None
        self.data_path_function = None
        self.del_function = None
        self.move_function = None
        self.queue_function = None
        self.duplicate_function = None

        self.setFixedSize(size, size)
        self.setFrameStyle(1)
        self.protocol_options = protocol_options

    def update_functions(self):
        """ """
        # check if build_asked has anything to disconnect
        if self.receivers(SIGNAL("build_asked()")) > 0:
            self.build_asked.disconnect()
        if self.receivers(SIGNAL("external_asked()")) > 0:
            self.external_asked.disconnect()
        if self.receivers(SIGNAL("data_path_asked()")) > 0:
            self.data_path_asked.disconnect()
        if self.receivers(SIGNAL("del_asked()")) > 0:
            self.del_asked.disconnect()
        if self.receivers(SIGNAL("move_asked()")) > 0:
            self.move_asked.disconnect()
        if self.receivers(SIGNAL("duplicate_asked()")) > 0:
            self.duplicate_asked.disconnect()
        if self.config_function is not None:
            self.button.clicked.connect(self.config_function)
        if self.run_function is not None:
            self.small_button.clicked.connect(self.run_function)
        if self.build_function is not None:
            self.build_asked.connect(self.build_function)
        if self.external_function is not None:
            self.external_asked.connect(self.external_function)
        if self.data_path_function is not None:
            self.data_path_asked.connect(self.data_path_function)
        if self.del_function is not None:
            self.del_asked.connect(self.del_function)
        if self.move_function is not None:
            self.move_asked.connect(self.move_function)
        if self.duplicate_function is not None:
            self.duplicate_asked.connect(self.duplicate_function)
        if self.queue_function is not None:
            self.queue_button.clicked.connect(self.queue_function)

    def options_menu(self, pos):
        """

        Parameters
        ----------
        pos :


        Returns
        -------

        """
        menu = QMenu()
        actions = []
        if self.protocol_options:
            action_export = QAction("Export Protocol")
            action_export.triggered.connect(self.build_asked.emit)
            action_open = QAction("Open Externally")
            action_open.triggered.connect(self.external_asked.emit)
            action_datapath = QAction("Open Data Path")
            action_datapath.triggered.connect(self.data_path_asked.emit)
            actions += [action_export, action_open, action_datapath]
        action_move = QAction("Move to other Tab")
        action_move.triggered.connect(self.move_button)
        action_duplicate = QAction("Duplicate")
        action_duplicate.triggered.connect(self.duplicate_asked.emit)
        action_delete = QAction("Delete")
        action_delete.triggered.connect(self.delete_button)
        menu.addActions(actions)
        menu.addSeparator()
        menu.addActions([action_duplicate, action_move, action_delete])
        menu.exec_(self.mapToGlobal(pos))

    def move_button(self):
        """ """
        self.move_asked.emit()

    def delete_button(self):
        """ """
        del_dialog = QMessageBox.question(
            self,
            f"Delete {self.label.text()}?",
            f"{self.label.text()} will be removed completely",
            QMessageBox.Yes | QMessageBox.No,
        )
        if del_dialog == QMessageBox.Yes:
            self.del_asked.emit()

    def mouseMoveEvent(self, event):
        """

        Parameters
        ----------
        event :


        Returns
        -------

        """
        if event.buttons() == Qt.LeftButton:
            mimeData = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(Qt.MoveAction)

    def rename(self, new_name):
        """

        Parameters
        ----------
        new_name :


        Returns
        -------

        """
        self.label.setText(new_name)
        if self.config_function is not None:
            self.button.clicked.disconnect(self.config_function)
        if self.run_function is not None:
            self.small_button.clicked.disconnect(self.run_function)
        if self.build_function is not None:
            self.build_asked.disconnect(self.build_function)
        if self.external_function is not None:
            self.external_asked.disconnect(self.external_function)
        if self.del_function is not None:
            self.del_asked.disconnect(self.del_function)
        if self.move_function is not None:
            self.move_asked.disconnect(self.move_function)
        if self.duplicate_function is not None:
            self.duplicate_asked.disconnect(self.duplicate_function)
        if self.data_path_function is not None:
            self.data_path_asked.disconnect(self.data_path_function)
        if self.queue_function is not None:
            self.queue_button.clicked.disconnect(self.queue_function)


if __name__ == "__main__":
    app = QApplication([])
    widge = QMainWindow()
    widget = Options_Run_Button("super mega test")
    # widge.setLayout(QHBoxLayout())
    # button = Options_Run_Button('s;aiouf;lwkeja;slkjfasd;lje')
    # widge.layout().addWidget(button)
    widget.show()
    app.exec()
