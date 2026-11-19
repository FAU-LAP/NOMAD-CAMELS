"""Run info (protocol, times, state, parameters) attached to the plots of a run."""

from types import SimpleNamespace

import pytest

pytest.importorskip("pyqtgraph")

from nomad_camels.MainApp_v2 import MainWindow  # noqa: E402
from nomad_camels.main_classes.plot_pyqtgraph import PlotWidget  # noqa: E402
from nomad_camels.main_classes.remote_plot_cache import PlotCacheRegistry  # noqa: E402


def fake_main_window():
    window = SimpleNamespace(
        open_plots=[],
        open_windows=[],
        plot_caches=PlotCacheRegistry(),
        _current_run_info=None,
        _current_run_plots=[],
    )
    window.add_to_open_windows = lambda plot: window.open_windows.append(plot)
    return window


def test_plots_of_a_run_get_its_info_and_end_state(qtbot):
    window = fake_main_window()
    old = PlotWidget("time", ["value"], title="before")
    qtbot.addWidget(old)
    MainWindow.add_to_plots(window, old)
    # Plots opened outside a run get no run info.
    assert not hasattr(old, "run_info")

    window._current_run_info = {"protocol": "IV", "started": "2026-11-19T14:03:22+01:00",
                                "ended": None, "state": "running", "variables": {"n": 3}}
    plot = PlotWidget("time", ["value"], title="IV curve")
    qtbot.addWidget(plot)
    MainWindow.add_to_plots(window, plot)
    assert plot.run_info["protocol"] == "IV"
    assert window._current_run_plots == [plot]
    cache_id = str(id(plot))
    assert window.plot_caches.ids() == [str(id(old)), cache_id]

    # The run ends: its plots are marked, a following run is not affected.
    ended_plots, window._current_run_plots = window._current_run_plots, []
    MainWindow._end_run_info(window, "aborted", ended_plots)
    assert plot.run_info["state"] == "aborted" and plot.run_info["ended"]
    assert plot.livePlot.remote_plot_cache.info["state"] == "aborted"
    assert "Aborted" in plot.run_info_overlay.button.text()

    # Closing one plot by its cache id.
    plot.show()
    MainWindow.close_plot(window, cache_id)
    assert window.plot_caches.ids() == [str(id(old))]
