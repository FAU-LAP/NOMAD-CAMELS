from PySide6.QtWidgets import QApplication, QMainWindow, QStyleFactory
from PySide6.QtGui import QPalette, QColor, QColorConstants
from qt_material import apply_stylesheet


light_palette = QPalette(QColor(225, 225, 225), QColor(238, 238, 238))
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

def change_theme(theme, main_app=None, material_theme=None, dark_mode=False):
    if main_app is None:
        main_app = QApplication.instance()
        if main_app is None:
            raise RuntimeError("MainApp not found.")
    if theme in QStyleFactory.keys():
        main_app.setStyleSheet('')
        palette = None
        if dark_mode:
            palette = dark_palette
        else:
            palette = light_palette
        if theme == 'windowsvista':# in QStyleFactory.keys():
            main_app.setStyle(QStyleFactory.create('windowsvista'))
        main_app.setPalette(palette)
        main_app.setStyle(QStyleFactory.create(theme))
        if palette:
            main_app.setPalette(palette)
    elif theme == 'qt-material':
        if not isinstance(material_theme, str):
            return
        if dark_mode:
            if material_theme.endswith('500'):
                material_theme = material_theme[:-4]
            xml = f'dark_{material_theme}.xml'
        else:
            xml = f'light_{material_theme}.xml'
        apply_stylesheet(main_app, theme=xml)