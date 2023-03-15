from PyQt5.QtWidgets import QApplication, QMainWindow
import qdarkstyle
from qt_material import apply_stylesheet

def change_theme(theme, main_app=None, main_window=None):
    if main_app is None:
        main_app = QApplication.instance()
        if main_app is None:
            raise RuntimeError("MainApp not found.")
    if theme == 'default':
        main_app.setStyleSheet('')
    elif theme == 'qdarkstyle':
        main_app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    else:
        apply_stylesheet(main_app, theme=theme+'.xml')
        # if 'light' in theme and main_window:
        #     main_window.setStyleSheet("QWidget#main_window > * { background-color: white; }")
        #     main_window.setObjectName("main_window")