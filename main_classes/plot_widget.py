import sys

import matplotlib.pyplot as plt
from bluesky_widgets.qt.threading import wait_for_workers_to_quit
from bluesky_widgets.models.auto_plot_builders import AutoLines
from bluesky_widgets.models import plot_builders
from bluesky_widgets.utils.streaming import stream_documents_into_runs
from bluesky_widgets.qt.figures import QtFigures, QtFigure

from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication

dark_mode = False
def activate_dark_mode():
    global dark_mode
    dark_mode = True
    plt.style.use('dark_background')


class PlotWidget(QWidget):
    def __init__(self, x_name='time', y_names=None, parent=None, max_runs=10, run_engine=None, title=None, xlabel=None, ylabel=None):
        super().__init__(parent)
        if type(y_names) is str:
            y_names = [y_names]
        elif y_names is None:
            y_names = ['']
        self.plot_model = My_Lines(x_name, y_names, max_runs=max_runs)
        layout = QGridLayout()
        self.setLayout(layout)
        plot = QtFigure(self.plot_model.figure, parent=parent)
        layout.addWidget(plot, 0, 1)
        if run_engine is not None:
            run_engine.subscribe(stream_documents_into_runs(self.plot_model.add_run))
        axes = self.plot_model.axes
        plot.figure.tight_layout()
        if title is not None:
            self.plot_model.title = title
            self.setWindowTitle(title)
        if xlabel is not None:
            axes.x_label = xlabel
        if ylabel is not None:
            self.plot_model.y_label = ylabel


class My_Lines(plot_builders.Lines):
    pass

    def _add_lines(self, event):
        "Add a line."
        if self._control_y_label:
            self.y_label = self._default_y_label()
        if self._control_title:
            self.title = self._default_title()

        run = event.run
        for y in self.ys:
            label = self._label_maker(run, y)
            # If run is in progress, give it a special color so it stands out.
            # if plot_builders.run_is_live_and_not_completed(run):
            #     color = "black"
            #
            #     def restyle_line_when_complete(event):
            #         "When run is complete, update style."
            #         line.style.update({"color": next(self._color_cycle)})
            #
            #     run.events.completed.connect(restyle_line_when_complete)
            # else:
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