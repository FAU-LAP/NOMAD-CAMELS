"""Tests for the plot data copies that OASIS reads."""

import json

import numpy as np
import pytest

from nomad_camels.main_classes.remote_plot_cache import (
    PlotCacheRegistry,
    RemotePlotCache,
    plotly_style,
)


def make_cache(**kwargs):
    return RemotePlotCache(title="IV", x_label="V", y_label="I", y_names=["I"], **kwargs)


def cursor_of(snapshot):
    return {"since": snapshot["end"], "generation": snapshot["generation"], "version": snapshot["version"]}


def test_only_new_points_are_returned():
    cache = make_cache()
    for i in range(3):
        cache.append(np.float64(i), {"I": np.int64(i * 10)})
    first = cache.snapshot()
    assert first["reset"] is True
    assert (first["start"], first["end"], first["more"]) == (0, 3, False)
    assert first["x"] == [0.0, 1.0, 2.0] and first["traces"][0]["y"] == [0, 10, 20]
    json.dumps(first)  # numpy values were converted

    cache.append(3, {"I": 30})
    second = cache.snapshot(**cursor_of(first))
    assert second["reset"] is False
    assert second["x"] == [3] and second["traces"][0]["y"] == [30]
    # Fits and styles are unchanged, so they are not sent again.
    assert "fits" not in second

    nothing = cache.snapshot(**cursor_of(second))
    assert nothing["x"] == [] and nothing["start"] == nothing["end"] == 4


def test_clear_starts_a_new_generation():
    cache = make_cache()
    cache.append(0, {"I": 1})
    first = cache.snapshot()
    cache.clear()
    cache.append(5, {"I": 6})
    after = cache.snapshot(**cursor_of(first))
    assert after["reset"] is True and after["generation"] != first["generation"]
    assert after["x"] == [5]


def test_two_caches_never_share_a_generation():
    # A plot id can be reused after a plot was closed.
    assert make_cache().generation != make_cache().generation


def test_maxlen_drops_old_points_and_resets_lagging_clients():
    cache = make_cache(maxlen=3)
    for i in range(3):
        cache.append(i, {"I": i})
    first = cache.snapshot()
    for i in range(3, 8):
        cache.append(i, {"I": i})
    lagging = cache.snapshot(**cursor_of(first))
    # The client's next point (3) is gone, so it receives the kept points.
    assert lagging["reset"] is True
    assert lagging["x"] == [5, 6, 7] and lagging["start"] == 5


def test_large_plots_are_sent_in_chunks():
    cache = make_cache()
    for i in range(1000):
        cache.append(i, {"I": i})
    chunk = cache.snapshot(max_values=300)  # 2 values per point
    assert (chunk["start"], chunk["end"], chunk["more"]) == (0, 150, True)
    rest = cache.snapshot(**cursor_of(chunk), max_values=10000)
    assert (rest["start"], rest["end"], rest["more"]) == (150, 1000, False)


def test_new_curves_and_missing_values():
    cache = make_cache()
    cache.append(0, {"I": 1})
    cache.append(1, {"I": 2, "U": 5})
    cache.append(2, {"U": float("nan")})
    traces = {trace["name"]: trace["y"] for trace in cache.snapshot()["traces"]}
    assert traces == {"I": [1, 2, None], "U": [None, 5, None]}


def test_second_axis_style_and_fits():
    cache = RemotePlotCache(title="t", x_label="x", y_label="y", y_names=["a", "b"], y_axes={"b": 2})
    cache.append(0, {"a": 1, "b": 2})
    first = cache.snapshot()
    assert [trace["axis"] for trace in first["traces"]] == ["y", "y2"]

    style = plotly_style(line_color="#ff0000", pen_style="DashLine", symbol="s", symbol_color="#00ff00")
    cache.set_appearance({"a": style}, {"y_log": True, "ignored": 1})
    cache.set_fit("fit_a", np.array([0.0, 1.0]), np.array([1.0, 2.0]), plotly_style(pen_style="SolidLine"))
    second = cache.snapshot(**cursor_of(first))
    trace_a = second["traces"][0]
    assert trace_a["mode"] == "lines+markers"
    assert trace_a["line"]["dash"] == "dash" and trace_a["marker"]["symbol"] == "square"
    assert second["y_log"] is True and "ignored" not in second
    assert second["fits"][0]["name"] == "fit_a" and second["fits"][0]["x"] == [0.0, 1.0]

    cache.set_fit("fit_a", [], [], {})
    assert cache.snapshot(**cursor_of(second))["fits"] == []


@pytest.mark.parametrize(
    "kwargs, mode",
    [
        ({"pen_style": "NoPen", "symbol": "o"}, "markers"),
        ({"pen_style": "SolidLine", "symbol": None}, "lines"),
        ({"pen_style": "DotLine", "symbol": "t1"}, "lines+markers"),
        ({"pen_style": "NoPen", "symbol": None}, "markers"),  # never invisible
    ],
)
def test_plotly_mode(kwargs, mode):
    assert plotly_style(**kwargs)["mode"] == mode


def test_registry_splits_the_budget_between_plots():
    registry = PlotCacheRegistry()
    for name in ("p1", "p2"):
        cache = make_cache()
        for i in range(30000):
            cache.append(i, {"I": i})
        registry.register(name, cache)
    result = registry.snapshots()
    assert result["open_plot_count"] == 2
    total = sum(len(plot["x"]) * 2 for plot in result["plots"])
    assert total <= 20000 and all(plot["more"] for plot in result["plots"])
    assert len(json.dumps(result)) < 900 * 1024

    registry.unregister("p1")
    assert [plot["id"] for plot in registry.snapshots()["plots"]] == ["p2"]


def test_style_is_read_from_the_qt_plot(qtbot):
    pg = pytest.importorskip("pyqtgraph")
    from nomad_camels.main_classes.plot_pyqtgraph import LivePlot

    widget = pg.PlotWidget()
    qtbot.addWidget(widget)
    live = LivePlot("time", ["value1", "value2"], plot_item=widget.getPlotItem())
    live.add_plot("value1")
    live.add_plot("value2")
    live.update_caches(0.5, {"value1": 1.0, "value2": 2.0})
    live.update_plot()
    snapshot = live.remote_plot_cache.snapshot()
    trace = snapshot["traces"][0]
    assert snapshot["x"] == [0.5]
    assert trace["mode"] == "markers" and trace["marker"]["symbol"] == "circle"
    assert trace["marker"]["color"] == "#1f77b4"  # first CAMELS color
    assert snapshot["traces"][1]["marker"]["color"] == "#ff7f0e"
    assert snapshot["background"] == "#ffffff"

    # A change in Plot Options appears in the copy.
    item = live.current_plots["value1"]
    item.setSymbol("s")
    item.setPen(pg.mkPen(color="#123456", width=3, style=pg.QtCore.Qt.PenStyle.DashLine))
    live.publish_remote_appearance()
    trace = live.remote_plot_cache.snapshot()["traces"][0]
    assert trace["mode"] == "lines+markers"
    assert trace["marker"]["symbol"] == "square"
    assert trace["line"] == {"color": "#123456", "width": 3.0, "dash": "dash"}

    live.clear_plot()
    assert live.remote_plot_cache.snapshot()["x"] == []


def test_run_info_and_change_token():
    registry = PlotCacheRegistry()
    cache = RemotePlotCache(title="t", x_label="x", y_label="y", y_names=["a"])
    token = registry.change_token()
    registry.register("p", cache)
    assert registry.change_token() != token
    token = registry.change_token()
    cache.append(1, {"a": 2})
    assert registry.change_token() != token

    first = cache.snapshot()
    assert first["info"] == {}
    cache.set_info({"protocol": "IV", "state": "running", "variables": {"n": 3}})
    token = registry.change_token()
    # Unchanged info changes nothing.
    cache.set_info({"state": "running"})
    assert registry.change_token() == token
    current = cache.snapshot(since=first["end"], generation=first["generation"], version=first["version"])
    assert current["info"] == {"protocol": "IV", "state": "running", "variables": {"n": 3}}
    cache.set_info({"state": "finished"})
    later = cache.snapshot(since=current["end"], generation=current["generation"], version=current["version"])
    assert later["info"]["state"] == "finished" and later["info"]["protocol"] == "IV"
    # No change: the info is not sent again.
    assert "info" not in cache.snapshot(since=later["end"], generation=later["generation"], version=later["version"])
    registry.unregister("p")
    assert registry.ids() == []


def test_run_info_overlay_in_the_plot_window(qtbot):
    pytest.importorskip("pyqtgraph")
    from nomad_camels.main_classes.plot_pyqtgraph import PlotWidget

    plot = PlotWidget("time", ["value"], title="IV curve")
    qtbot.addWidget(plot)
    plot.show()
    overlay = plot.run_info_overlay
    assert not overlay.isVisible()
    plot.set_run_info({"protocol": "IV", "started": "2026-11-19T14:03:22+01:00", "state": "running",
                       "variables": {"n": 3}})
    assert overlay.isVisible() and not overlay.details.isVisible()
    assert overlay.button.text() == "IV · started 2026-11-19 14:03:22 · Running"
    overlay.button.click()
    assert overlay.details.isVisible() and "n = 3" in overlay.details.text()
    # Inside the plot area, in the top right corner.
    assert overlay.parent() is plot.plot_widget
    assert overlay.geometry().right() <= plot.plot_widget.width()
    plot.set_run_info({"state": "finished", "ended": "2026-11-19T14:05:00+01:00"})
    assert "Finished" in overlay.button.text() and "Ended" in overlay.details.text()
    assert plot.livePlot.remote_plot_cache.info["state"] == "finished"
    assert plot.livePlot.remote_plot_cache.info["protocol"] == "IV"
