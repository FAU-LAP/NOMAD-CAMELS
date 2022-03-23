from ophyd import EpicsSignalRO
from ophyd.status import Status


class TriggerEpicsSignalRO(EpicsSignalRO):

    def __init__(self, read_pv, *, timeout=10, string=False, name=None, no_mdel=False, **kwargs):
        super().__init__(read_pv, string=string, name=name, timeout=timeout, auto_monitor=False, **kwargs)
        self.stat = None
        self.trigger_pv = self.cl.get_pv(f'{read_pv}:trig')
        self.subscribe(self.callback_method)
        self.last_time = self.timestamp
        self.no_mdel = no_mdel

    def callback_method(self, **kwargs):
        if self.stat is not None:
            self.stat.set_finished()
            self.stat = None

    def trigger(self):
        self.stat = Status(self, timeout=self.timeout)
        self.trigger_pv.put(1)
        if self.no_mdel:
            self.stat.set_finished()
        return self.stat






# def my_put(name):


# if __name__ == '__main__':
#     def testplan(dets, mot, start, stop, n, delay=0, md=None):
#         yield from bps.open_run()
#         yield from bps.trigger_and_read(dets, name='sec')
#         for i in np.linspace(start, stop, n):
#             yield from bps.abs_set(mot, i, wait=True)
#             yield from bps.sleep(delay)
#             yield from trigger_and_read_devices(dets)
#         yield from bps.close_run()
#     RE = RunEngine()
#     db = Broker.named('temp')
#     RE.subscribe(db.insert)
#     # # mesI = TriggerEpicsSignalRO('Hall:e5270:mesI1')
#     # mesV = TriggerEpicsSignalRO('Hall:e5270:mesV1')
#     # setV = EpicsSignal('Hall:e5270:setV1')
#     # setV.wait_for_connection()
#     # # mesI.wait_for_connection()
#     # mesV.wait_for_connection()
#     # # RE(scan([mesV], setV, 0, 1, 3))
#     # RE(testplan([mesV], setV, 0, 1, 3))
#     e5270 = Keysight_E5270B('Hall:e5270:', name='e5270')
#     e5270.wait_for_connection()
#     # e5270.apply_std_config()
#     RE(testplan([e5270], e5270.setV1, -0.1, 0.1, 5))
#     header = db[-1]
#     print(header.start)
#     print(e5270.read_configuration())
#     print(header.config_data('e5270'))
#     print(header.table())
#     db = header.table()
#     plt.plot(db['e5270_mesV1'], db['e5270_mesI1'], 'x')
#     plt.show()
#     # camonitor('Hall:e5270:mesV1', callback=mesV.callback_method)
#     # while True:
#     #     time.sleep(0.1)