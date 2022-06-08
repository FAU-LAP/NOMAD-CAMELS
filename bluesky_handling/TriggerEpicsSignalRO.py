from ophyd import EpicsSignalRO
from ophyd.status import Status


class TriggerEpicsSignalRO(EpicsSignalRO):
    """Subclass that implements a simple 'timed' reading when called via
    bluesky's 'trigger_and_read'.
    Note that each PV that shall be read via this class also needs a
    second PV with the same name+:trig. That PV should provide a FLNK to
    the original PV.

    Parameters
    ----------
    read_pv : str
        the name of the PV that shall be read
    name : str
        name of the Signal (usually the same as the variable-name)
    no_mdel : bool, default False
        set to True if the MDEL field of the corresponding record is not
        set to "-1". The status returned from the trigger function is
        then directly set to finished
    """
    def __init__(self, read_pv, *, timeout=10, string=False, name=None,
                 no_mdel=False, **kwargs):
        super().__init__(read_pv, string=string, name=name, timeout=timeout, auto_monitor=False, **kwargs)
        self.stat = None
        self.trigger_pv = self.cl.get_pv(f'{read_pv}:trig')
        self.subscribe(self.callback_method)
        self.last_time = self.timestamp
        self.no_mdel = no_mdel
        self.triggering = True

    def callback_method(self, **kwargs):
        """If there is a status object from the trigger-method, it will
        be set to finished."""
        if self.stat is not None and not self.no_mdel and self.triggering:
            self.stat.set_finished()
            # self.stat = None

    def trigger(self):
        """Returns a status object that will be set to finished, when
        the PV-value is updated. Sets the trigger-PV to 1, thus
        triggering the process of the original PV."""
        self.stat = Status(self, timeout=self.timeout)
        if self.triggering:
            self.trigger_pv.put(1)
        if self.no_mdel or not self.triggering:
            self.stat.set_finished()
        return self.stat
