from PySide6.QtWidgets import QApplication, QMainWindow, QStyleFactory
from PySide6.QtGui import QPalette, QColor
from qt_material import apply_stylesheet

dark_palette = QPalette(QColor(53, 53, 53), QColor(42, 42, 42))
light_palette = QPalette(QColor(225, 225, 225), QColor(238, 238, 238))

def change_theme(theme, main_app=None, material_theme=None, dark_mode=False):
    if main_app is None:
        main_app = QApplication.instance()
        if main_app is None:
            raise RuntimeError("MainApp not found.")
    if theme in QStyleFactory.keys():
        main_app.setStyleSheet('')
        palette = None
        if 'windowsvista' in QStyleFactory.keys():
            main_app.setStyle(QStyleFactory.create('windowsvista'))
            if dark_mode:
                palette = dark_palette
            else:
                palette = light_palette
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