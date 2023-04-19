# Import the necessary PySide6 modules
import sys
from PySide6.QtWidgets import QApplication, QDialog, QProgressBar, QGridLayout, QLabel
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QPixmap, QIcon
import os
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

from pkg_resources import resource_filename
# Import your main application form
# from main_window import MainWindow

# Create a new form for the loading screen
class LoadingScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NOMAD-CAMELS - Loading...")
        self.setCursor(Qt.WaitCursor)
        layout = QGridLayout()
        self.setLayout(layout)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setWindowIcon(QIcon(resource_filename('nomad_camels', 'graphics/camels_icon.png')))

        image = QPixmap()
        image.load(resource_filename('nomad_camels', 'graphics/CAMELS_vertical.png'))
        image = image.scaled(403, 308)
        image_label = QLabel()
        image_label.setPixmap(image)

        self.label = QLabel('loading...')

        self.progress_bar = QProgressBar(self)
        layout.addWidget(image_label, 0, 0)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.progress_bar, 2, 0)
        self.show()

    # A function to update the progress bar
    def set_progress(self, value):
        self.progress_bar.setValue(value)

    def set_text(self, text):
        self.label.setText(text)


# Show the loading screen and import your packages
if __name__ == '__main__':
    app = QCoreApplication.instance()
    if app is None:
        # sys.argv += ['-platform', 'windows:darkmode=1']
        app = QApplication(sys.argv)

    # Create the loading screen
    loading_screen = LoadingScreen()
    loading_screen.show()
    import os.path
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    file_dir = os.path.dirname(__file__)
    package_file = f'{file_dir}/packages.txt'
    if os.path.isfile(package_file):
        with open(f'{file_dir}/packages.txt', 'r') as f:
            package_list = [x.rstrip() for x in f.readlines()]
    else:
        package_list = []
    n = len(package_list) + 1

    from PySide6.QtCore import QThread, Signal
    # Create a thread to import the packages

    class ImportThread(QThread):
        update_progress = Signal(int)
        update_text = Signal(str)

        def run(self):
            # Import your packages here
            for i, package in enumerate(package_list):
                self.update_progress.emit(int(i / n * 100))
                self.update_text.emit(f'loading {package}...')
                try:
                    __import__(package)
                except ModuleNotFoundError:
                    pass
            self.update_text.emit('starting NOMAD-CAMELS...')
            self.update_progress.emit(int((n-1)/n * 100))
            from nomad_camels import MainApp_v2


    # Start the thread and connect the progress signal
    thread = ImportThread()
    thread.update_progress.connect(loading_screen.set_progress)
    thread.update_text.connect(loading_screen.set_text)
    # thread.finished.connect(start_main)
    thread.start()
    while thread.isRunning():
        app.processEvents()
    with open(package_file, 'w') as f:
        for i, (mod_name, mod) in enumerate(sys.modules.items()):
            if mod_name.startswith('_') or mod is None:
                continue
            f.write(f'{mod_name}\n')
    from nomad_camels import MainApp_v2
    from nomad_camels.utility import exception_hook
    sys.excepthook = exception_hook.exception_hook
    main_window = MainApp_v2.MainWindow()
    loading_screen.hide()

    app.exec()