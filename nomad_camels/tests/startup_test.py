def test_startup(qtbot, capfd):
    """Simply try to start and run CAMELS.
    By default, the autosave is enabled, so if it works correctly and closes,
    the statement should be printed

    Parameters
    ----------
    qtbot :
        
    capfd :
        

    Returns
    -------

    """
    import sys
    import nomad_camels.MainApp_v2
    from nomad_camels.utility import exception_hook
    # sys.excepthook = exception_hook.exception_hook
    main_window = nomad_camels.MainApp_v2.MainWindow()

    def close_save_message():
        """ """
        main_window.change_catalog_name()
        main_window.close()
        out, err = capfd.readouterr()
        print(out)
        assert 'current state saved!' in out

    qtbot.waitUntil(close_save_message)


