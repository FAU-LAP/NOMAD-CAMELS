import pytest
from unittest.mock import MagicMock, patch
import numpy as np

from PySide6.QtWidgets import QApplication

# Importing your classes (adjust the module paths accordingly)
from nomad_camels.main_classes.plot_2D import PlotWidget_2D, LivePlot_2D


# Ensure a QApplication instance exists for QWidget tests


@pytest.fixture(scope="module")
def app():
    """Fixture for creating a QApplication instance"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


# Mock for Evaluator since it might depend on other parts of your application
@pytest.fixture
def evaluator_mock():
    return MagicMock()


def test_plotwidget_2d_init(app, evaluator_mock):
    widget = PlotWidget_2D(
        x_name="x", y_name="y", z_name="z", title="Test Plot", namespace=None
    )

    assert widget.windowTitle() == "Test Plot"
    assert widget.x_name == "x"
    assert widget.y_name == "y"
    assert widget.z_name == "z"
    assert widget.livePlot is not None
    assert widget.toolbar is not None
    assert widget.pushButton_autoscale is not None


def test_plotwidget_2d_autoscale(app, evaluator_mock):
    widget = PlotWidget_2D(
        x_name="x", y_name="y", z_name="z", title="Test Plot", namespace=None
    )

    widget.ax.set_xlim(0, 1)
    widget.ax.set_ylim(0, 1)

    widget.autoscale()

    assert widget.ax.get_xlim() != (0, 1)
    assert widget.ax.get_ylim() != (0, 1)


def test_plotwidget_2d_close_event(app, evaluator_mock):
    widget = PlotWidget_2D(
        x_name="x", y_name="y", z_name="z", title="Test Plot", namespace=None
    )

    with patch.object(widget, "closeEvent") as mock_close_event:
        widget.close()
        mock_close_event.assert_called_once()


def test_liveplot_2d_init(evaluator_mock):
    live_plot = LivePlot_2D(x="x", y="y", z="z", evaluator=evaluator_mock)
    live_plot.start({})

    assert live_plot.x == "x"
    assert live_plot.y == "y"
    assert live_plot.I == "z"
    assert live_plot.eva == evaluator_mock


def test_liveplot_2d_update(evaluator_mock):
    live_plot = LivePlot_2D(x="x", y="y", z="z", evaluator=evaluator_mock)
    live_plot.start({})

    x_data = np.array([1, 2, 3])
    y_data = np.array([4, 5, 6])
    z_data = np.array([7, 8, 9])

    live_plot.update(x_data, y_data, z_data)

    assert len(live_plot._xdata) == 3
    assert len(live_plot._ydata) == 3
    assert len(live_plot._Idata) == 3
    assert live_plot._xdata == [1, 2, 3]
    assert live_plot._ydata == [4, 5, 6]
    assert live_plot._Idata == [7, 8, 9]


def test_liveplot_2d_make_colormesh(evaluator_mock):
    live_plot = LivePlot_2D(x="x", y="y", z="z", evaluator=evaluator_mock)

    live_plot._xdata = [1, 2, 3]
    live_plot._ydata = [4, 5, 6]
    live_plot._Idata = [7, 8, 9]

    mesh = live_plot.make_colormesh(x_shape=1, y_shape=3)

    assert mesh is not None
    x, y, c = mesh
    assert x.shape == (1, 3)
    assert y.shape == (1, 3)
    assert c.shape == (1, 3)


def test_liveplot_2d_clear_plot(evaluator_mock):
    live_plot = LivePlot_2D(x="x", y="y", z="z", evaluator=evaluator_mock)

    live_plot._xdata = [1, 2, 3]
    live_plot._ydata = [4, 5, 6]
    live_plot._Idata = [7, 8, 9]

    live_plot.clear_plot()

    assert len(live_plot._xdata) == 0
    assert len(live_plot._ydata) == 0
    assert len(live_plot._Idata) == 0
