from unittest.mock import patch
import tempfile
from PySide6.QtWidgets import QApplication
import sys
from nomad_camels.MainApp_v2 import MainWindow
from nomad_camels.CAMELS_start import start_camels


def test_startup_of_mainapp(qtbot, capfd):
    """Simply try to start and run CAMELS.
    By default, the autosave is enabled, so if it works correctly and closes,
    the statement "current state saved!" should be printed"""
    # import sys
    from nomad_camels.utility import exception_hook

    class MockDialog:
        def __init__(self, *args, **kwargs):
            # Create a temporary directory for the test
            with tempfile.TemporaryDirectory() as temp_dir:
                self.path = temp_dir

        def exec(self):
            return True

    def close_save_message():
        """ """
        main_window.change_catalog_name()
        main_window.close()
        out, err = capfd.readouterr()
        print(out)
        assert "current state saved!" in out

    with patch(
        "nomad_camels.ui_widgets.path_button_edit.Path_Button_Dialog", new=MockDialog
    ):
        main_window = MainWindow()
        qtbot.waitUntil(close_save_message)


def test_start_camels(qtbot, capfd):
    """Test the startup of the CAMELS application."""

    class MockDialog:
        def __init__(self, *args, **kwargs):
            # Create a temporary directory for the test
            self.path = tempfile.mkdtemp()

        def exec(self):
            return True

    def close_save_message():
        """ """
        main_window.change_catalog_name()
        main_window.close()
        out, err = capfd.readouterr()
        print(out)
        assert "current state saved!" in out

    with patch(
        "nomad_camels.ui_widgets.path_button_edit.Path_Button_Dialog", new=MockDialog
    ):
        with patch("nomad_camels.CAMELS_start.QApplication.exec", return_value=None):
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)

            # Start the CAMELS application
            start_camels()

            # Check if the main window is displayed
            app.processEvents()
            main_window = app.activeWindow()
            assert main_window is not None
            assert (
                main_window.windowTitle()
                == "NOMAD CAMELS - Configurable Application for Measurements, Experiments and Laboratory-Systems"
            )
            qtbot.waitUntil(close_save_message)

            # Ensure the main window is closed properly
            main_window.close()
            qtbot.waitUntil(lambda: not main_window.isVisible())
