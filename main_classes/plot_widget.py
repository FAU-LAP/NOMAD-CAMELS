import sys

from bluesky_widgets.qt.threading import wait_for_workers_to_quit
from bluesky_widgets.models.auto_plot_builders import AutoLines
from bluesky_widgets.models import plot_builders
from bluesky_widgets.utils.streaming import stream_documents_into_runs
from bluesky_widgets.qt.figures import QtFigures, QtFigure

from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication

class PlotWidget(QWidget):
    def __init__(self, x_name='time', y_names=None, parent=None, max_runs=10, run_engine=None):
        super().__init__(parent)
        if type(y_names) is str:
            y_names = [y_names]
        elif y_names is None:
            y_names = ['']
        self.plot_model = plot_builders.Lines(x_name, y_names, max_runs=max_runs)
        layout = QGridLayout()
        self.setLayout(layout)
        plot = QtFigure(self.plot_model.figure, parent=parent)
        layout.addWidget(plot, 0, 1)
        if run_engine is not None:
            run_engine.subscribe(stream_documents_into_runs(self.plot_model.add_run))
        axes = plot.figure.get_axes()
        b = axes[0]



if __name__ == '__main__':
    from bluesky import RunEngine
    from bluesky.plans import scan
    from ophyd.sim import motor, det

    motor.delay = 0.2

    def plan():
        for i in range(1, 5):
            yield from scan([det], motor, -1, 1, 1 + 2 * i)

    RE = RunEngine()
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(wait_for_workers_to_quit)
    myapp = PlotWidget(run_engine=RE, x_name='motor', y_names=['det'])
    myapp.show()
    RE(plan())
    sys.exit(app.exec_())