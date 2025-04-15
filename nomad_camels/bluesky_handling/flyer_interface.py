""" Module for Asynchronous Data Acquisition from Detectors

This module provides classes for managing asynchronous data collection from multiple detectors using a threaded approach. The primary class is CAMELS_Flyer."""

from PySide6.QtCore import QMutex, QMutexLocker, QThread, QTimer, Signal
from collections import deque
from ophyd import DeviceStatus
import time

from nomad_camels.bluesky_handling.run_engine_overwrite import get_nan_value


class CAMELS_Flyer:
    """
    Class that provides asynchronous acquisition during the run of protocol.

    Parameters
    ----------
    name : str
        Name of the flyer and its data stream.
    detectors : list
        List of the detectors to be used for data collection.
    read_time : float
        Time interval (in seconds) between each reading.
    can_fail : list[bool]
        If true, a failed reading of the detector does not throw an error and a NaN value is used instead.
    **kwargs : dict
        Additional keyword arguments (not in use).

    Attributes
    ----------
    name : str
        Flyer name.
    detectors : list
        List of detectors.
    can_fail : list or bool
        Fail flag for each detector.
    read_time : float
        Read interval in seconds.
    mutex : QMutex
        Mutex for thread-safe operations.
    _data : deque
        Deque to store collected data events.
    _completion_status : DeviceStatus or None
        Status of the data collection process.
    flyer_thread : Flyer_Thread
        Thread that performs the periodic reading from detectors.
    """

    def __init__(self, name, detectors, read_time, can_fail, **kwargs):
        self.name = name
        self.detectors = detectors
        self.can_fail = can_fail
        self.read_time = read_time
        self.mutex = QMutex()
        self._data = deque()
        self._completion_status = None
        self.flyer_thread = Flyer_Thread(
            detectors=detectors,
            can_fail=can_fail,
            read_time=read_time,
            flyer_name=name,
            data_object=self._data,
            mutex=self.mutex,
        )
        self.flyer_thread.finished.connect(self._thread_finished)
        self.flyer_thread.exception_signal.connect(self.propagate_exceptions)
        self._raised_exceptions = []

    def _thread_finished(self):
        """
        Callback invoked when the flyer thread has finished execution.
        Marks the data collection as finished.
        """
        self._completion_status.set_finished()

    def propagate_exceptions(self, ex):
        """Raise an exception from the flyer thread in the main thread."""
        if not ex.args in self._raised_exceptions:
            self._raised_exceptions.append(ex.args)
            raise ex

    def describe_collect(self):
        """
        Generate a description of the detectors for data collection.

        Returns
        -------
        dict
            Dictionary with flyer name as key and aggregated detector descriptions as value.
        """
        dd = {}
        for det in self.detectors:
            dd.update(det.describe())
        return {self.name: dd}

    def kickoff(self):
        """
        Start the data collection process.

        Raises
        ------
        RuntimeError
            If a collection is already in progress.

        Returns
        -------
        DeviceStatus
            Status object indicating that the kickoff is complete.
        """
        if self._completion_status is not None and not self._completion_status.done:
            raise RuntimeError(f"Collection already in progress for flyer {self.name}!")
        self._completion_status = DeviceStatus(device=self)
        self.flyer_thread.start()
        kickoff_st = DeviceStatus(device=self)
        kickoff_st.set_finished()
        return kickoff_st

    def complete(self):
        """
        Stop the data collection process.

        Raises
        ------
        RuntimeError
            If no collection is currently in progress.

        Returns
        -------
        DeviceStatus
            Status object indicating the completion status of the data collection.
        """
        if self._completion_status is None:
            raise RuntimeError(f"No collection in progress for flyer {self.name}!")
        self.flyer_thread.quit()
        return self._completion_status

    def collect(self):
        """
        Retrieve the collected data events in a thread-safe manner. Clears the data deque.

        Yields
        ------
        list
            List of collected data events.
        """
        with QMutexLocker(self.mutex):
            data = list(self._data)
            self._data.clear()
        yield from data


class Flyer_Thread(QThread):
    """
    Thread class for periodically reading data asynchronously during a protocol.

    Parameters
    ----------
    parent : QObject, optional
        Parent object (default is None).
    detectors : list, optional
        List of detectors to trigger and read from (default is None, giving an empty list).
    can_fail : list[bool], optional
        Flag for each detector indicating if a failed reading should be ignored (default None defaults to all False).
    read_time : float, optional
        Time interval (in seconds) between each read (default is 1).
    flyer_name : str, optional
        Name identifier for the flyer, which also names the resulting data stream (default is "camels_flyer").
    data_object : deque, optional
        Deque to store the collected events (default is None).
    mutex : QMutex, optional
        Mutex for ensuring thread-safe operations (default is None).

    Attributes
    ----------
    timer : QTimer or None
        Timer to schedule periodic readings.
    keep_running : bool
        Flag to control the continuous operation of the thread.
    mutex : QMutex
        Mutex for synchronizing access to shared data.
    _currently_reading : bool
        Flag indicating if a read operation is currently in progress.
    """

    exception_signal = Signal(Exception)

    def __init__(
        self,
        parent=None,
        detectors=None,
        can_fail=None,
        read_time=1,
        flyer_name="camels_flyer",
        data_object=None,
        mutex=None,
    ):
        super().__init__(parent)
        self.detectors = detectors or []
        self.can_fail = can_fail or [False] * len(self.detectors)
        self.read_time = read_time
        self.flyer_name = flyer_name
        self.data_object = data_object
        self.timer = None
        self.keep_running = True
        self.mutex = mutex or QMutex()
        self._currently_reading = False

    def run(self):
        """
        Run the thread event loop with a timer that periodically triggers data reading.
        """
        self.timer = QTimer(self)
        # Convert read_time from seconds to milliseconds
        self.timer.setInterval(self.read_time * 1000)
        self.timer.timeout.connect(self._do_reading)
        self.timer.start()
        # Enter the thread's event loop
        self.exec()
        self.timer.stop()
        # Wait until any ongoing reading is finished before completely exiting the thread
        while self._currently_reading:
            time.sleep(0.1)

    def _do_reading(self):
        """
        Perform a single reading cycle from all detectors.

        Triggers all detectors, waits for their operations to complete,
        and then constructs an event dictionary with the collected data.
        The event is appended to the shared data object in a thread-safe manner.
        """
        try:
            self._currently_reading = True
            stats = []
            # Trigger all detectors and collect their statuses
            for det in self.detectors:
                stats.append(det.trigger())
            # Wait for all detectors to complete triggering
            for stat in stats:
                stat.wait()
            # Create an event with the current time and empty data containers
            event = {"time": time.time(), "data": {}, "timestamps": {}}
            for i, det in enumerate(self.detectors):
                if self.can_fail[i]:
                    try:
                        det.trigger()
                        d = det.read()
                    except Exception as e:
                        # If the detector fails, use a NaN value for the detector reading
                        d = {
                            det.name: {
                                "value": get_nan_value(det.value),
                                "timestamp": time.time(),
                            }
                        }
                else:
                    det.trigger()
                    d = det.read()
                # Populate the event with detector data and corresponding timestamps
                for k, v in d.items():
                    event["data"][k] = v["value"]
                    event["timestamps"][k] = event["time"]
            # Safely append the event to the shared data object
            with QMutexLocker(self.mutex):
                self.data_object.append(event)
        except Exception as ex:
            self.exception_signal.emit(ex)
        finally:
            self._currently_reading = False
