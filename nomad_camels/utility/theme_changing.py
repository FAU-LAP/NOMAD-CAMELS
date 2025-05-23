"""This module is used to change the UI-theme of CAMELS. It provides some
default color palettes `light_palette` and `dark_palette`."""

from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QPalette, QColor, QColorConstants

try:
    from qt_material import apply_stylesheet

    QT_MATERIAL = True
except ImportError:
    QT_MATERIAL = False


light_palette = QPalette(QColor(225, 225, 225), QColor(238, 238, 238))
light_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))

dark_palette = QPalette()
dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
dark_palette.setColor(QPalette.WindowText, QColorConstants.White)
dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
dark_palette.setColor(QPalette.ToolTipBase, QColorConstants.White)
dark_palette.setColor(QPalette.ToolTipText, QColorConstants.White)
dark_palette.setColor(QPalette.Text, QColorConstants.White)
dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
dark_palette.setColor(QPalette.ButtonText, QColorConstants.White)
dark_palette.setColor(QPalette.BrightText, QColorConstants.Red)
dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
dark_palette.setColor(QPalette.HighlightedText, QColorConstants.Black)


tooltip_dark = """
    QToolTip {
        background-color: #2a2a2a;
        color: white;
        border: 1px solid #3a3a3a;
        border-radius: 6px;
        padding: 3px;
        font: 12px;
    }
"""
tooltip_light = """
    QToolTip {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #c0c0c0;
        border-radius: 6px;
        padding: 3px;
        font: 12px;
    }
"""


splitter_style = """
    QSplitter::handle {
        border-radius: 3px;
    }
"""
splitter_style_light = (
    splitter_style
    + """
    QSplitter::handle {
        background: #aaaaaa;
        border: 1px solid #0a0a0a;
    }
    QSplitter::handle:hover {
        background-color: #3a3a3a;
        border: 1px dashed white;
    }
"""
)
splitter_style_dark = (
    splitter_style
    + """
    QSplitter::handle {
        background: gray;
        border: 1px solid #5a5a5a;
    }
    QSplitter::handle:hover {
        background-color: #bababa;
        border: 1px dashed black;
    }
"""
)


def change_theme(theme, main_app=None, material_theme=None, dark_mode=False):
    """

    Parameters
    ----------
    theme : str
        The name of the used theme. Possible values are the themes from
        QStyleFactory and "qt-material".
    main_app : QMainWindow
        (Default value = None)
        The main UI-window. If it is None, it is looked for with
        `QApplication.instance()`.
    material_theme : str
        (Default value = None)
        If `theme=="qt-material"`, the qt-material color palette is chosen with
        this theme name.
    dark_mode : bool
        (Default value = False)
        If True, the color palettes are switched to dark mode.
    """
    if main_app is None:
        main_app = QApplication.instance()
        if main_app is None:
            raise RuntimeError("MainApp not found for changing the color theme.")
    if theme in QStyleFactory.keys():
        main_app.setStyleSheet("")
        palette = None
        if dark_mode:
            palette = dark_palette
            main_app.setStyleSheet(tooltip_dark)
        else:
            palette = light_palette
            main_app.setStyleSheet(tooltip_light)
        if theme == "windowsvista":
            main_app.setStyle(QStyleFactory.create("windowsvista"))
        main_app.setPalette(palette)
        main_app.setStyle(QStyleFactory.create(theme))
        if palette:
            main_app.setPalette(palette)
    elif theme == "qt-material" and QT_MATERIAL:
        if not isinstance(material_theme, str):
            return
        if dark_mode:
            if material_theme.endswith("500"):
                material_theme = material_theme[:-4]
            xml = f"dark_{material_theme}.xml"
            main_app.setStyleSheet(tooltip_dark)
        else:
            xml = f"light_{material_theme}.xml"
            main_app.setStyleSheet(tooltip_light)
        apply_stylesheet(main_app, theme=xml)
    elif theme == "qt-material" and not QT_MATERIAL:
        # TODO: Add a message box to inform the user that qt-material is not installed, make optional
        raise ImportError("qt-material is not installed!")
    if dark_mode:
        main_app.setStyleSheet(main_app.styleSheet() + splitter_style_dark)
    else:
        main_app.setStyleSheet(main_app.styleSheet() + splitter_style_light)
