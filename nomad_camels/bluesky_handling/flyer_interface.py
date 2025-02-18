from PySide6.QtCore import QMutex, QMutexLocker, QThread, QTimer
from collections import deque
from ophyd import DeviceStatus
import time


class CAMELS_Flyer:
    def __init__(self, name, detectors, read_time, **kwargs):
        self.name = name
        self.detectors = detectors
        self.read_time = read_time
        self.mutex = QMutex()
        self._data = deque()
        self._completion_status = None
        self.flyer_thread = Flyer_Thread(
            detectors=detectors,
            read_time=read_time,
            flyer_name=name,
            data_object=self._data,
            mutex=self.mutex,
        )
        self.flyer_thread.finished.connect(self._thread_finished)

    def _thread_finished(self):
        self._completion_status.set_finished()

    def describe_collect(self):
        dd = {}
        for det in self.detectors:
            dd.update(det.describe())
        return {self.name: dd}

    def kickoff(self):
        if self._completion_status is not None and not self._completion_status.done:
            raise RuntimeError(f"Collection already in progress for flyer {self.name}!")
        self._completion_status = DeviceStatus(device=self)
        self.flyer_thread.start()
        kickoff_st = DeviceStatus(device=self)
        kickoff_st.set_finished()
        return kickoff_st

    def complete(self):
        if self._completion_status is None:
            raise RuntimeError(f"No collection in progress for flyer {self.name}!")
        self.flyer_thread.quit()
        return self._completion_status

    def collect(self):
        with QMutexLocker(self.mutex):
            data = list(self._data)
            self._data.clear()
        yield from data


class Flyer_Thread(QThread):
    def __init__(
        self,
        parent=None,
        detectors=None,
        read_time=0,
        flyer_name="camels_flyer",
        data_object=None,
        mutex=None,
    ):
        super().__init__(parent)
        self.detectors = detectors or []
        self.read_time = read_time
        self.flyer_name = flyer_name
        self.data_object = data_object
        self.timer = None
        self.keep_running = True
        self.mutex = mutex or QMutex()
        self._currently_reading = False

    def run(self):
        self.timer = QTimer(self)
        self.timer.setInterval(self.read_time * 1000)
        self.timer.timeout.connect(self._do_reading)
        self.timer.start()
        self.exec()
        self.timer.stop()
        while self._currently_reading:
            time.sleep(0.1)

    def _do_reading(self):
        self._currently_reading = True
        stats = []
        for det in self.detectors:
            stats.append(det.trigger())
        for stat in stats:
            stat.wait()
        event = {"time": time.time(), "data": {}, "timestamps": {}}
        for det in self.detectors:
            d = det.read()
            for k, v in d.items():
                event["data"][k] = v["value"]
                event["timestamps"][k] = v["timestamp"]
        with QMutexLocker(self.mutex):
            self.data_object.append(event)
        self._currently_reading = False
