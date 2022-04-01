"""
An example integration QtFigures into an "existing" Qt application. Run like:

python -m bluesky_widgets.examples.qt_app_integration
"""
from qtpy.QtWidgets import QApplication, QVBoxLayout, QLabel, QMainWindow, QWidget


def main():
    # First, some boilerplate to make a super-minimal Qt application that we want
    # to add some bluesky-widgets components into.
    app = QApplication(["Some App"])
    window = QMainWindow()
    central_widget = QWidget(window)
    window.setCentralWidget(central_widget)
    central_widget.setLayout(QVBoxLayout())
    central_widget.layout().addWidget(QLabel("This is part of the 'original' app."))
    window.show()

    # *** INTEGRATION WITH BLUESKY-WIDGETS STARTS HERE. ***

    # Ensure that any background workers started by bluesky-widgets stop
    # gracefully when the application closes.
    from bluesky_widgets.qt.threading import wait_for_workers_to_quit

    app.aboutToQuit.connect(wait_for_workers_to_quit)

    # Model a list of figures.
    # This will generate line plot automatically based on the structure (shape)
    # of the data and its hints. Other models could be used for more explicit
    # control of what gets plotted. See the examples in
    # http://blueskyproject.io/bluesky-widgets/reference.html#plot-builders
    from bluesky_widgets.models.auto_plot_builders import AutoLines

    model = AutoLines(max_runs=10)

    # Feed it data from the RunEngine. In actual practice, the RunEngine should
    # be in a separate process and we should be receiving these documents
    # over a network via publish--subscribe. See
    # bluesky_widgets.examples.advanced.qt_viewer_with_search for an example of
    # that. Here, we keep it simple.
    from bluesky_widgets.utils.streaming import stream_documents_into_runs
    from bluesky import RunEngine

    RE = RunEngine()
    RE.subscribe(stream_documents_into_runs(model.add_run))

    # Add a tabbed pane of figures to the app.
    from bluesky_widgets.qt.figures import QtFigures

    view = QtFigures(model.figures)  # view is a QWidget
    central_widget.layout().addWidget(view)

    # When the model receives data or is otherwise updated, any changes to
    # model.figures will be reflected in changes to the view.

    # Just for this example, generate some data before starting this app.
    # Again, in practice, this should happen in a separate process and send
    # the results over a network.

    from bluesky.plans import scan
    from ophyd.sim import motor, det
    import time
    from ophyd import EpicsMotor
    from ophyd import Device, EpicsSignal, EpicsSignalRO

    # m1 = EpicsMotor('IOCsim:m1', name='m1', labels=("motors",))
    # keithley6517 = EpicsSignal("EMILEL:test:rdCurE3", name="keithley", labels=("detectors"))
    motor.delay = 0
    def plan():
        for i in range(1, 5):
            yield from scan([det], motor, -1, 1, 1 + 2 * i)

        # yield from scan([keithley6517], m1, -1, 1, 2)

    RE(plan())


    # *** INTEGRATION WITH BLUESKY-WIDGETS ENDS HERE. ***

    # Run the app.
    app.exec_()


if __name__ == "__main__":
    main()
