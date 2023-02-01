from PyQt5.QtWidgets import QWidget, QDesktopWidget

desktop = None
current_screen = 0
current_pos = [0, 0]
max_height_in_row = 0
iteration = 0

horizontal_margin = 5
vertical_margin = 5


def place_widget(widget:QWidget):
    global max_height_in_row, current_screen, desktop, current_pos, iteration
    if desktop is None:
        desktop = QDesktopWidget()
    widget.show()
    c = current_pos
    print(c, current_screen)
    s = widget.size()
    screen_geometry = desktop.screenGeometry(current_screen)
    if current_pos[0] + s.width() > screen_geometry.width():
        current_pos[1] += max_height_in_row + horizontal_margin
        current_pos[0] = 0
        max_height_in_row = 0
        if current_pos[1] + s.height() > screen_geometry.height():
            current_pos[1] = 0
            current_screen += 1
            if current_screen >= desktop.screenCount():
                current_screen = 0
                iteration += 1
            screen_geometry = desktop.screenGeometry(current_screen)
            current_pos[1] += 5 * iteration * vertical_margin
    widget.move(current_pos[0] + screen_geometry.x(), current_pos[1] + screen_geometry.y())
    print(current_pos[0] + screen_geometry.x(), current_pos[1] + screen_geometry.y())
    current_pos[0] += s.width() + vertical_margin
    max_height_in_row = s.height() if s.height() > max_height_in_row else max_height_in_row