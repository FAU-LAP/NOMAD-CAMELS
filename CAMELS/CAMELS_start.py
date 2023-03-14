# Import the necessary PyQt5 modules
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QProgressBar, QGridLayout, QLabel
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPixmap

from pkg_resources import resource_filename
# Import your main application form
# from main_window import MainWindow

# Create a new form for the loading screen
class LoadingScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAMELS - Loading...")
        self.setCursor(Qt.WaitCursor)
        layout = QGridLayout()
        self.setLayout(layout)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        image = QPixmap()
        image.load(resource_filename('CAMELS','graphics/CAMELS_Logo.png'))
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
        app = QApplication(sys.argv)

    # Create the loading screen
    loading_screen = LoadingScreen()
    loading_screen.show()
    import os.path
    file_dir = os.path.dirname(__file__)
    with open(f'{file_dir}/packages.txt', 'r') as f:
        package_list = [x.rstrip() for x in f.readlines()]
    n = len(package_list) + 1

    from PyQt5.QtCore import QThread, pyqtSignal
    # Create a thread to import the packages

    class ImportThread(QThread):
        update_progress = pyqtSignal(int)
        update_text = pyqtSignal(str)

        def run(self):
            # Import your packages here
            for i, package in enumerate(package_list):
                self.update_progress.emit(int(i / n * 100))
                self.update_text.emit(f'loading {package}...')
                __import__(package)
            self.update_text.emit('starting CAMELS...')
            self.update_progress.emit(int((n-1)/n * 100))
            import MainApp_v2


    # Start the thread and connect the progress signal
    thread = ImportThread()
    thread.update_progress.connect(loading_screen.set_progress)
    thread.update_text.connect(loading_screen.set_text)
    # thread.finished.connect(start_main)
    thread.start()
    while thread.isRunning():
        app.processEvents()
    import MainApp_v2
    import sys
    from CAMELS.utility import exception_hook
    sys.excepthook = exception_hook.exception_hook
    main_window = MainApp_v2.MainWindow()
    loading_screen.hide()

    app.exec_()