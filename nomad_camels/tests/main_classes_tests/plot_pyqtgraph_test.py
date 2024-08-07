import pytest
from PySide6.QtWidgets import QApplication, QMainWindow, QColorDialog
from PySide6.QtGui import QCloseEvent, QColor
from unittest.mock import patch
from unittest.mock import MagicMock
import pyqtgraph as pg


# Importing the necessary components for the test
from nomad_camels.main_classes.plot_pyqtgraph import PlotWidget, LivePlot, Plot_Options


@pytest.fixture(scope="module")
def qapp():
    """Fixture for creating a QApplication instance"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def plot_widget(qapp):
    """Fixture for creating an instance of PlotWidget."""
    return PlotWidget(
        x_name="time",
        y_names=["value1", "value2"],
        stream_name="primary",
        use_bluesky=False,  # Mocking bluesky usage for simplicity
    )


def test_initialization(plot_widget):
    """Test the initialization of PlotWidget."""
    assert plot_widget.x_name == "time"
    assert plot_widget.y_names == ["value1", "value2"]
    assert plot_widget.stream_name == "primary"
    assert plot_widget.plot_widget is not None
    assert plot_widget.livePlot is not None


def test_show_again(plot_widget):
    """Test the show_again method."""
    with patch.object(plot_widget, "show") as mock_show:
        plot_widget.show_again()
        mock_show.assert_not_called()
        plot_widget.close()
        plot_widget.show_again()
        mock_show.assert_called_once()


def test_auto_range(plot_widget):
    """Test the auto_range method."""
    with patch.object(plot_widget.livePlot.plotItem.vb, "autoRange") as mock_autoRange:
        plot_widget.auto_range()
        mock_autoRange.assert_called_once()
        if plot_widget.ax2_viewbox:
            with patch.object(
                plot_widget.ax2_viewbox, "autoRange"
            ) as mock_ax2_autoRange:
                plot_widget.auto_range()
                mock_ax2_autoRange.assert_called_once()


def test_change_maxlen(plot_widget):
    """Test the change_maxlen method."""
    plot_widget.lineEdit_n_data.setText("100")
    plot_widget.change_maxlen()
    assert plot_widget.livePlot.maxlen == 100

    plot_widget.lineEdit_n_data.setText("inf")
    plot_widget.change_maxlen()
    assert plot_widget.livePlot.maxlen == float("inf")

    plot_widget.lineEdit_n_data.setText("invalid")
    plot_widget.change_maxlen()
    # maxlen should not change due to invalid input
    assert plot_widget.livePlot.maxlen == float("inf")


def test_show_options(plot_widget):
    """Test the show_options method."""
    plot_widget.show_options()
    assert plot_widget.options_open
    assert plot_widget.pushButton_show_options.text() == "Hide Options"

    plot_widget.show_options()
    assert not plot_widget.options_open
    assert plot_widget.pushButton_show_options.text() == "Show Options"


def test_clear_plot(plot_widget):
    """Test the clear_plot method."""
    with patch.object(plot_widget.livePlot, "clear_plot") as mock_clear_plot:
        for fit_plot in plot_widget.liveFitPlots:
            with patch.object(fit_plot, "clear_plot") as mock_fit_clear_plot:
                plot_widget.clear_plot()
                mock_clear_plot.assert_called_once()
                mock_fit_clear_plot.assert_called_once()


def test_closeEvent(plot_widget):
    """Test the closeEvent method."""
    mock_slot = MagicMock()
    plot_widget.closing.connect(mock_slot)
    plot_widget.closeEvent(QCloseEvent())
    mock_slot.assert_called_once()


@pytest.fixture
def main_window(qapp):
    window = QMainWindow()
    return window


@pytest.fixture
def live_plot(main_window):
    plot_widget = pg.PlotWidget()
    plot_item = plot_widget.getPlotItem()
    plot_item.setLogMode = MagicMock()
    ax2_viewbox = pg.ViewBox()
    plot_item.scene().addItem(ax2_viewbox)
    live_plot = LivePlot("time", ["test"], plot_item=plot_item, ax2_viewbox=ax2_viewbox)
    return live_plot


@pytest.fixture
def plot_options(main_window, live_plot):
    plot_options = Plot_Options(parent=main_window, livePlot=live_plot)
    return plot_options
