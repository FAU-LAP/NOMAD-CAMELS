import sys

import matplotlib.pyplot as plt
from bluesky_widgets.qt.threading import wait_for_workers_to_quit
from bluesky_widgets.models import plot_builders
from bluesky_widgets.utils.streaming import stream_documents_into_runs
from bluesky_widgets.qt.figures import QtFigure

from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication

dark_mode = False
def activate_dark_mode():
    """Changes the plot-style to dark-mode."""
    global dark_mode
    dark_mode = True
    plt.style.use('dark_background')


class PlotWidget(QWidget):
    """Pop-up Widget containing a simple Plot."""
    def __init__(self, x_name='time', y_names=None, parent=None, max_runs=10,
                 run_engine=None, title=None, xlabel=None, ylabel=None,
                 streams=('primary',)):
        """

        Parameters
        ----------
        x_name : str, default "time"
            name of the x-axis signal used for the plot, if "time" the
            y-values are plotted against time
        y_names : list or str
            list of all values that should be plotted along the y-axis
        parent : QWidget
            parent-widget of the PlotWidget
        max_runs : int, default 10
            maximum number of runs that should be plotted at the same
            time, older runs are then removed
        run_engine : RunEngine
            the RunEngine, to which the plot should be subscribed
        title : str
            title of the matplotlib-plot and of the Window
        xlabel : str
            x-label of the plot
        ylabel : str
            y-label of the plot
        streams : iterable, default ("primary",)
            the streams that should be handled by this plot
        """
        super().__init__(parent)
        if isinstance(y_names, str):
            y_names = [y_names]
        elif y_names is None:
            y_names = ['']
        if x_name == "":
            x_name = 'time'
        self.plot_model = My_Lines(x_name, y_names, max_runs=max_runs, needs_streams=streams)
        layout = QGridLayout()
        self.setLayout(layout)
        plot = QtFigure(self.plot_model.figure, parent=parent)
        layout.addWidget(plot, 0, 1)
        if run_engine is not None:
            run_engine.subscribe(stream_documents_into_runs(self.plot_model.add_run))
        axes = self.plot_model.axes
        plot.figure.tight_layout()
        if title is not None and title != "":
            self.plot_model.title = title
            self.setWindowTitle(title)
        if xlabel is not None and xlabel != "":
            axes.x_label = xlabel
        if ylabel is not None and ylabel != "":
            self.plot_model.y_label = ylabel


class My_Lines(plot_builders.Lines):
    """Overwriting the plot_builders.Lines to not change the color for
    the current run."""
    def _add_lines(self, event):
        """Add a line."""
        if self._control_y_label:
            self.y_label = self._default_y_label()
        if self._control_title:
            self.title = self._default_title()

        run = event.run
        for y in self.ys:
            label = self._label_maker(run, y)
            color = next(self._color_cycle)
            style = {"color": color}

            # Style pinned runs differently.
            if run.metadata["start"]["uid"] in self.pinned:
                style.update(linestyle="dashed")
                label += " (pinned)"

            func = plot_builders.functools.partial(self._transform, x=self.x, y=y)
            line = plot_builders.Line.from_run(func, run, label, style)
            self._run_manager.track_artist(line, [run])
            self.axes.artists.append(line)
            self._ys_to_artists[y].append(line)



if __name__ == '__main__':
    from bluesky import RunEngine
    from bluesky.plans import scan
    from ophyd.sim import motor, det

    motor.delay = 0.1

    def plan():
        for i in range(1, 5):
            yield from scan([det], motor, -1, 1, 1 + 2 * i)

    RE = RunEngine()
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(wait_for_workers_to_quit)
    myapp = PlotWidget(run_engine=RE, x_name='motor', y_names=['det'], title='test', xlabel='aaaa', ylabel='bbbb')
    myapp.show()
    RE(plan())
    sys.exit(app.exec_())