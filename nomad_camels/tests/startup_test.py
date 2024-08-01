import pytest
from unittest.mock import patch, Mock
import tempfile
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication
import sys
import os
import subprocess
from nomad_camels.MainApp_v2 import MainWindow
from nomad_camels.CAMELS_start import start_camels, LoadingScreen


class MockDialog:
    def __init__(self, *args, **kwargs):
        # Create a temporary directory for the test
        self.path = tempfile.mkdtemp()

    def exec(self):
        return True


@pytest.mark.order(0)
def test_start_camels(qtbot, capfd):
    """Test the startup of the CAMELS application."""

    def close_save_message():
        """ """
        main_window.close()
        out, err = capfd.readouterr()
        app = QApplication.instance()
        app.processEvents()
        assert "current state saved!" in out

    with patch(
        "nomad_camels.ui_widgets.path_button_edit.Path_Button_Dialog", new=MockDialog
    ):
        with patch("nomad_camels.CAMELS_start.QApplication.exec", return_value=None):

            # Start the CAMELS application
            app = QCoreApplication.instance()
            if app is not None:
                app.quit()
                del app
            start_camels()
            app = QApplication.instance()

            # Check if the main window is displayed
            app.processEvents()
            main_window = None
            widgets = app.topLevelWidgets()
            for widget in widgets:
                if isinstance(widget, MainWindow):
                    main_window = widget
                    break
            assert main_window is not None
            assert (
                main_window.windowTitle()
                == "NOMAD CAMELS - Configurable Application for Measurements, Experiments and Laboratory-Systems"
            )
            try:
                qtbot.waitUntil(close_save_message)
            except TimeoutError:
                pass

            # Ensure the main window is closed properly
            main_window.close()
            app.processEvents()
            qtbot.waitUntil(lambda: not main_window.isVisible())


@pytest.mark.order(0)
def test_start_camels_again(qtbot, capfd):
    """Test the startup of the CAMELS application."""

    def close_save_message():
        """ """
        main_window.close()
        app = QApplication.instance()
        app.processEvents()
        out, err = capfd.readouterr()
        assert "current state saved!" in out

    with patch(
        "nomad_camels.ui_widgets.path_button_edit.Path_Button_Dialog", new=MockDialog
    ):
        with patch("nomad_camels.CAMELS_start.QApplication.exec", return_value=None):

            # Start the CAMELS application
            app = QCoreApplication.instance()
            if app is not None:
                app.quit()
                del app
            start_camels()
            app = QApplication.instance()

            # Check if the main window is displayed
            app.processEvents()
            main_window = None
            widgets = app.topLevelWidgets()
            for widget in widgets:
                if isinstance(widget, MainWindow):
                    main_window = widget
                    break
            assert main_window is not None
            assert (
                main_window.windowTitle()
                == "NOMAD CAMELS - Configurable Application for Measurements, Experiments and Laboratory-Systems"
            )
            try:
                qtbot.waitUntil(close_save_message, timeout=10000)
            except (TimeoutError, AssertionError):
                pass

            # Ensure the main window is closed properly
            main_window.close()
            app.processEvents()
            qtbot.waitUntil(lambda: not main_window.isVisible())


@pytest.fixture(scope="module")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    if app is not None:
        app.quit()


@pytest.fixture
def instance(app):
    return LoadingScreen()  # Replace with the actual class name


@pytest.mark.order(0)
def test_set_progress(instance):
    instance.set_progress(50)
    assert instance.progress_bar.value() == 50


@pytest.mark.order(0)
def test_set_text(instance):
    test_text = "Test text"
    instance.set_text(test_text)
    assert instance.label.text() == test_text


@pytest.mark.order(0)
def test_import_thread(qtbot):
    """Test the ImportThread class."""
    from CAMELS_start import ImportThread

    # Mock the package list and other dependencies
    package_list = ["os", "sys", "nonexistent_package", "sys.bad_test_attribute"]
    loading_screen = Mock()
    loading_screen.set_progress = Mock()
    loading_screen.set_text = Mock()

    # Create an instance of ImportThread
    thread = ImportThread(package_list=package_list)

    # Connect signals to slots
    thread.update_progress.connect(loading_screen.set_progress)
    thread.update_text.connect(loading_screen.set_text)

    # Start the thread
    thread.run()

    # Wait for the thread to finish
    qtbot.waitUntil(lambda: not thread.isRunning(), timeout=5000)

    # Check if the signals were emitted correctly
    loading_screen.set_progress.assert_called()
    loading_screen.set_text.assert_called()

    # Ensure the thread has finished
    assert not thread.isRunning()
