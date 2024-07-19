# Import the necessary PySide6 modules
import sys
from PySide6.QtWidgets import QApplication, QDialog, QProgressBar, QGridLayout, QLabel
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QPixmap, QIcon
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from importlib import resources
from nomad_camels import graphics
# Add nomad_camels/gui folder to the python path
sys.path.append(os.path.join(os.path.dirname(__file__),r"gui"))

# Import your main application form
# from main_window import MainWindow


# Create a new form for the loading screen
class LoadingScreen(QDialog):
    """
    A loading screen that appears when the application is starting up.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("NOMAD CAMELS - Loading...")
        self.setCursor(Qt.WaitCursor)
        layout = QGridLayout()
        self.setLayout(layout)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setWindowIcon(QIcon(str(resources.files(graphics) / "camels_icon.png")))

        image = QPixmap()
        image.load(str(resources.files(graphics) / "CAMELS_vertical.png"))
        image = image.scaled(403, 308)
        image_label = QLabel()
        image_label.setPixmap(image)

        self.label = QLabel("loading...")

        self.progress_bar = QProgressBar(self)
        layout.addWidget(image_label, 0, 0)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.progress_bar, 2, 0)
        self.show()

    # A function to update the progress bar
    def set_progress(self, value):
        """
        Set the progress bar value
        """
        self.progress_bar.setValue(value)

    def set_text(self, text):
        """

        Parameters
        ----------
        text :


        Returns
        -------

        """
        self.label.setText(text)


# Show the loading screen and import your packages
def start_camels():
    import os

    app = QCoreApplication.instance()
    if app is None:
        # sys.argv += ['-platform', 'windows:darkmode=1']
        app = QApplication(sys.argv)

    # Create the loading screen
    loading_screen = LoadingScreen()
    loading_screen.show()
    import os.path

    file_dir = os.path.dirname(__file__)
    package_file = os.path.join(file_dir, "startup_packages.txt")
    if os.path.isfile(package_file):
        with open(package_file, "r", encoding="utf-8") as f:
            package_list = [x.rstrip() for x in f.readlines()]
    else:
        package_list = []
    n = len(package_list) + 1

    from PySide6.QtCore import QThread, Signal

    # Create a thread to import the packages

    class ImportThread(QThread):
        """This thread imports the necessary packages for the main application to run."""

        update_progress = Signal(int)
        update_text = Signal(str)

        def run(self):
            """ """
            # Import your packages here
            for i, package in enumerate(package_list):
                self.update_progress.emit(int(i / n * 96))
                self.update_text.emit(f"loading {package}...")
                try:
                    __import__(package)
                except ModuleNotFoundError:
                    pass
                except AttributeError:
                    pass
            self.update_text.emit("starting NOMAD CAMELS...")
            self.update_progress.emit(int((n - 1) / n * 96))
            from nomad_camels import MainApp_v2

    # Start the thread and connect the progress signal
    thread = ImportThread()
    thread.update_progress.connect(loading_screen.set_progress)
    thread.update_text.connect(loading_screen.set_text)
    thread.start()
    while thread.isRunning():
        app.processEvents()
    with open(package_file, "w", encoding="utf-8") as f:
        for i, (mod_name, mod) in enumerate(sys.modules.items()):
            if mod_name.startswith("_") or mod is None:
                continue
            f.write(f"{mod_name}\n")
    from nomad_camels import MainApp_v2
    from nomad_camels.utility import exception_hook

    sys.excepthook = exception_hook.exception_hook
    main_window = MainApp_v2.MainWindow()
    loading_screen.hide()
    main_window.show()

    app.exec()


if __name__ == "__main__":
    start_camels()
