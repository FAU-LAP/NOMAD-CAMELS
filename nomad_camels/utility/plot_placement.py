"""This module helps to place the plots on the screen without too much
overlap between the plots. The positions are saved into the global variables,
since this module may be imported by several other modules.

Attributes
----------
    current_screen : int
        the number of the currently used screen to place plots
    current_pos : list[int, int]
        the x and y coordinates of the current placement
    max_height_in_row : int
        the maximum height a plot window has within the currently populated row
    iteration : int
        if the screens were full once, it is increased and the next plots are
        slightly shifted
    horizontal_margin : int
        the horizontal distance between the plot windows
    vertical_margin : int
        the vertical distance between the plot windows
"""

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


def reset_variables():
    global current_screen, current_pos, max_height_in_row, iteration, screens
    screens = app.screens()
    current_screen = 0
    current_pos = [0, 0]
    max_height_in_row = 0
    iteration = 0
    screen_geometry = screens[current_screen].availableGeometry()


def place_widget(
    widget: QWidget,
    top_left_x: int = None,
    top_left_y: int = None,
    plot_width: int = None,
    plot_height: int = None,
):
    """
    This function places the given `widget` on the next free spot on the screen.
    First all widgets are placed next to each other in a row, until one would be
    outside the screen, then the next row is started. If it would "flow out" the
    bottom of the screen, a second screen (if available) is used. If all
    available screens are full, it restarts on the first screen, slightly
    shifting the widgets in comparison to the first ones.

    Parameters
    ----------
    widget : QWidget
        the widget that should be placed
    """
    global max_height_in_row, current_screen, current_pos, iteration, screens
    widget.show()

    # If specific coordinates and dimensions are provided, use them
    if (
        top_left_x is not None
        and top_left_y is not None
        and top_left_x != ""
        and top_left_y != ""
    ):
        widget.move(int(top_left_x), int(top_left_y))

        if plot_width not in (None, "") and plot_height not in (None, ""):
            widget.resize(int(plot_width), int(plot_height))

        return

    s = widget.size()
    try:
        screen_geometry = screens[current_screen].availableGeometry()
    except:
        reset_variables()
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
            current_pos[1] += 5 * iteration * vertical_margin
    widget.move(
        current_pos[0] + screen_geometry.x(), current_pos[1] + screen_geometry.y()
    )
    current_pos[0] += s.width() + vertical_margin
    max_height_in_row = (
        s.height() if s.height() > max_height_in_row else max_height_in_row
    )
