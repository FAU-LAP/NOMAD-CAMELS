# Import the necessary PySide6 modules
import sys
from PySide6.QtWidgets import QApplication, QDialog, QProgressBar, QGridLayout, QLabel
from PySide6.QtCore import Qt, QCoreApplication, QThread, Signal
from PySide6.QtGui import QPixmap, QIcon
import os

# Extend the system path to include the parent directory of the current file.
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from importlib import resources, import_module
from nomad_camels import graphics

# Add nomad_camels/gui folder to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), r"gui"))

# Import your main application form
# from main_window import MainWindow


class LoadingScreen(QDialog):
    """
    A loading screen dialog that is displayed while the main application is starting up.

    This screen shows an image, a loading text label, and a progress bar that updates as packages
    are imported and the application loads.
    """

    def __init__(self):
        """
        Initialize the loading screen dialog.

        Sets up the dialog window properties, layout, image, label, and progress bar.
        """
        super().__init__()
        self.setWindowTitle("NOMAD CAMELS - Loading...")
        self.setCursor(Qt.WaitCursor)
        layout = QGridLayout()
        self.setLayout(layout)
        # Set custom window flags to disable some default decorations
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        # Set the window icon using a resource from the graphics package
        self.setWindowIcon(QIcon(str(resources.files(graphics) / "camels_icon.png")))

        # Load and set the image on the loading screen
        image = QPixmap()
        image.load(str(resources.files(graphics) / "CAMELS_vertical.png"))
        image = image.scaled(403, 308)
        image_label = QLabel()
        image_label.setPixmap(image)

        # Create a label to display loading text
        self.label = QLabel("loading...")

        # Create and configure the progress bar
        self.progress_bar = QProgressBar(self)
        # Add widgets to the layout in a grid formation
        layout.addWidget(image_label, 0, 0)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.progress_bar, 2, 0)
        self.show()

    def set_progress(self, value):
        """
        Update the progress bar with the given value.

        Args:
            value (int): The new value for the progress bar (typically 0 to 100).
        """
        self.progress_bar.setValue(value)

    def set_text(self, text):
        """
        Update the loading text displayed on the screen.

        Args:
            text (str): The new text to display in the label.
        """
        self.label.setText(text)


class ImportThread(QThread):
    """
    A thread dedicated to importing packages required by the main application.

    This thread emits progress updates and loading messages via signals while importing each package.
    """

    update_progress = Signal(int)
    update_text = Signal(str)

    def __init__(self, package_list=None):
        """
        Initialize the ImportThread with an optional list of packages to import.

        Args:
            package_list (list[str], optional): List of package names to import. Defaults to None.
        """
        super().__init__()
        self.package_list = package_list or []

    def run(self):
        """
        Execute the thread to import the specified packages.

        This method iterates over the package list, emitting progress updates and messages.
        If an import error occurs (ModuleNotFoundError or AttributeError), it is silently ignored.
        Finally, it imports the main application module.
        """
        # Calculate total number of steps for progress calculation
        package_list = self.package_list
        n = len(package_list) + 1
        for i, package in enumerate(package_list):
            # Emit progress update based on the current index
            self.update_progress.emit(int(i / n * 96))
            # Emit a message indicating which package is being loaded
            self.update_text.emit(f"loading {package}...")
            try:
                # Attempt to import the package
                import_module(package)
            except ModuleNotFoundError:
                # If the module is not found, continue without interruption
                pass
            except AttributeError:
                # If there is an attribute error during import, continue without interruption
                pass
        # Final update message before starting the main application
        self.update_text.emit("starting NOMAD CAMELS...")
        self.update_progress.emit(int((n - 1) / n * 96))
        # Import the main application module to proceed with launching the app
        from nomad_camels import MainApp_v2


def start_camels(start_proxy_bool=True):
    """
    Launch the NOMAD CAMELS application with a loading screen.

    This function performs the following steps:
      1. Checks if a QCoreApplication instance exists and creates one if needed.
      2. Displays the loading screen.
      3. Reads the list of startup packages from a file (if available).
      4. Starts a separate thread to import the packages with progress updates.
      5. Processes application events until the import thread completes.
      6. Saves the currently loaded modules to the startup package file.
      7. Sets up the main window and exception hook.
      8. Launches the main application event loop.
    """
    import os

    # Ensure there is an active QApplication or QCoreApplication instance
    app = QCoreApplication.instance()
    if app is None:
        # sys.argv += ['-platform', 'windows:darkmode=1']
        app = QApplication(sys.argv)

    # Create and display the loading screen
    loading_screen = LoadingScreen()
    loading_screen.show()

    import os.path

    # Determine the path to the startup packages file
    file_dir = os.path.dirname(__file__)
    package_file = os.path.join(file_dir, "startup_packages.txt")
    if os.path.isfile(package_file):
        # Read package names from the file, stripping newline characters
        with open(package_file, "r", encoding="utf-8") as f:
            package_list = [x.rstrip() for x in f.readlines()]
    else:
        package_list = []

    # Start the import thread and connect its signals to the loading screen updates
    thread = ImportThread(package_list)
    thread.update_progress.connect(loading_screen.set_progress)
    thread.update_text.connect(loading_screen.set_text)
    thread.start()

    # Process Qt events until the import thread has finished its execution
    while thread.isRunning():
        app.processEvents()

    # After the thread finishes, write the names of currently loaded modules to the startup packages file
    with open(package_file, "w", encoding="utf-8") as f:
        packages = {key: val for key, val in sys.modules.items()}
        for i, (mod_name, mod) in enumerate(packages.items()):
            # Skip private modules and any modules that are None
            if mod_name.startswith("_") or mod is None:
                continue
            f.write(f"{mod_name}\n")

    # Import the main application and utility modules
    from nomad_camels import MainApp_v2
    from nomad_camels.utility import exception_hook

    # Set the exception hook for handling uncaught exceptions
    sys.excepthook = exception_hook.exception_hook

    # Create and display the main application window, hiding the loading screen
    main_window = MainApp_v2.MainWindow(start_proxy_bool=start_proxy_bool)
    loading_screen.hide()
    main_window.show()
    thread.quit()
    thread.wait()
    thread.deleteLater()
    # Start the main Qt application event loop
    app.exec()


if __name__ == "__main__":
    start_camels()
