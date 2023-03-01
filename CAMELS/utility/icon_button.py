from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter, QPalette, QPen


class IconButton(QPushButton):
    def __init__(self, parent=None, icon=None, width=100, height=100):
        super().__init__(parent=parent)
        self.setStyleSheet('QPushButton {font-family: Arial; font-size: 16px;}')
    #     self.setFixedSize(width, height)
    #     self.color = None
    #     if icon:
    #         self.use_icon(icon)
    #     self.set_icon_color('default')
    #
    # def use_icon(self, icon):
    #     self.setIcon(icon)
    #     self.setIconSize(QSize(self.width(), self.height()))
    #
    # def resizeEvent(self, a0) -> None:
    #     self.setIconSize(QSize(self.width(), self.height()))
    #
    # def set_icon_color(self, color):
    #     self.color = color
    #     self.update()
    #
    # def paintEvent(self, event):
    #     super().paintEvent(event)
    #     if self.color is not None:
    #         painter = QPainter(self)
    #         painter.setRenderHint(QPainter.Antialiasing)
    #         icon = self.icon()
    #         pixmap = icon.pixmap(self.iconSize())
    #         color = self.color
    #         if color == 'default':
    #             palette = self.palette()
    #             color = palette.color(QPalette.ButtonText)
    #         painter.setPen(QPen(color))
    #         painter.drawPixmap(self.rect(), pixmap)
    #         painter.end()