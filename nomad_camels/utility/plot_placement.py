import sys

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QCoreApplication

app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
screens = app.screens()

current_screen = 0
current_pos = [0, 0]
max_height_in_row = 0
iteration = 0

horizontal_margin = 5
vertical_margin = 5


def place_widget(widget:QWidget):
    global max_height_in_row, current_screen, current_pos, iteration
    widget.show()
    c = current_pos
    # print(c, current_screen)
    s = widget.size()
    screen_geometry = screens[current_screen].availableGeometry()
    if current_pos[0] + s.width() > screen_geometry.width():
        current_pos[1] += max_height_in_row + horizontal_margin
        current_pos[0] = 0
        max_height_in_row = 0
        if current_pos[1] + s.height() > screen_geometry.height():
            current_pos[1] = 0
            current_screen += 1
            if current_screen >= len(screens):
                current_screen = 0
                iteration += 1
            screen_geometry = screens[current_screen].availableGeometry()
            current_pos[1] += 5 * iteration * vertical_margin
    widget.move(current_pos[0] + screen_geometry.x(), current_pos[1] + screen_geometry.y())
    # print(current_pos[0] + screen_geometry.x(), current_pos[1] + screen_geometry.y())
    current_pos[0] += s.width() + vertical_margin
    max_height_in_row = s.height() if s.height() > max_height_in_row else max_height_in_row