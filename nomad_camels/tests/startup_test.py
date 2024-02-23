from unittest.mock import patch
import tempfile


def test_startup(qtbot, capfd):
    """Simply try to start and run CAMELS.
    By default, the autosave is enabled, so if it works correctly and closes,
    the statement "current state saved!" should be printed"""
    # import sys
    import nomad_camels.MainApp_v2
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
        main_window = nomad_camels.MainApp_v2.MainWindow()
        qtbot.waitUntil(close_save_message)
