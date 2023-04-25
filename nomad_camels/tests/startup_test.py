def test_startup():
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QCoreApplication
    import nomad_camels.MainApp_v2
    from nomad_camels.utility import exception_hook
    sys.excepthook = exception_hook.exception_hook
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    main_window = nomad_camels.MainApp_v2.MainWindow()
    main_window.close()
