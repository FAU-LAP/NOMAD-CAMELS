from PySide6.QtWidgets import QApplication, QMainWindow, QStyleFactory
from PySide6.QtGui import QPalette, QColor
import qdarkstyle
from qt_material import apply_stylesheet

def change_theme(theme, main_app=None, main_window=None):
    if main_app is None:
        main_app = QApplication.instance()
        if main_app is None:
            raise RuntimeError("MainApp not found.")
    palette = None
    if 'windowsvista' in QStyleFactory.keys():
        main_app.setStyle(QStyleFactory.create('windowsvista'))
        dark_palette = QPalette(QColor(53), QColor(42, 42, 42))
        light_palette = QPalette(QColor(225, 225, 225), QColor(238, 238, 238))
        palette = light_palette
        # palette = QPalette(QColor(53, 53, 53), QColor(42, 42, 42))
        main_app.setPalette(palette)
    if theme == 'default':
        main_app.setStyleSheet('')
    # elif theme == 'qdarkstyle':
    #     main_app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))
    elif theme in QStyleFactory.keys():
        main_app.setStyle(QStyleFactory.create(theme))
        main_app.setStyle(QStyleFactory.create(theme))
        if palette:
            main_app.setPalette(palette)
        # palette = QPalette(QColor(53, 53, 53), QColor(42, 42, 42))
        # main_app.setPalette(palette)
        # palette = main_app.style().standardPalette()
        # main_app.setPalette(main_app.style().standardPalette())
    # else:
    #     apply_stylesheet(main_app, theme=theme+'.xml')
        # if 'light' in theme and main_window:
        #     main_window.setStyleSheet("QWidget#main_window > * { background-color: white; }")
        #     main_window.setObjectName("main_window")