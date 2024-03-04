from ophyd import Signal

import numpy as np

from epics import caput, caget


class EpicsFieldSignal(Signal):
    """A Signal used to address a single field of an EPICS PV."""

    def __init__(
        self,
        read_pv_name,
        name,
        value=0.0,
        timestamp=None,
        parent=None,
        labels=None,
        kind="hinted",
        tolerance=None,
        rtolerance=None,
        metadata=None,
        cl=None,
        attr_name="",
        conversion_function=None,
        set_conversion_function=None,
        putFunc=None,
    ):
        """
        Parameters
        ----------
        read_pv_name : str
            The name of the used PV.field
        name : string, keyword only
        value : any, optional
            The initial value
        timestamp : float, optional
            The timestamp associated with the initial value. Defaults to
            the current local time.
        parent : Device, optional
            The parent Device holding this signal
        kind : a member the Kind IntEnum (or equivalent integer), optional
            Default is Kind.normal. See Kind for options.
        tolerance : any, optional
            The absolute tolerance associated with the value
        rtolerance : any, optional
            The relative tolerance associated with the value, used in
            set_and_wait as follows
            .. math::
              |setpoint - readback| \\leq (tolerance + rtolerance * |readback|)
        cl : namespace, optional
            Control Layer.  Must provide 'get_pv' and 'thread_class'
        attr_name : str, optional
            The parent Device attribute name that corresponds to this
            Signal
        conversion_function : function, default lambda x: x
            This function is used to convert the given value for `put`
            to the actual value that the Signal should be set to
        set_conversion_function : function, default lambda x: x
            This function is used to convert the given value from `get`
            to the actual value that the User wants to see
        putFunc : function, default lambda x: x
            A function to be called when the value is put (e.g. to
            connect to other Signals)
        """
        super().__init__(
            name=name,
            value=value,
            timestamp=timestamp,
            parent=parent,
            labels=labels,
            kind=kind,
            tolerance=tolerance,
            rtolerance=rtolerance,
            metadata=metadata,
            cl=cl,
            attr_name=attr_name,
        )
        self.read_pv_name = read_pv_name
        if conversion_function is None:
            conversion_function = lambda x: x
        self.conversion_function = conversion_function
        if set_conversion_function is None:
            set_conversion_function = lambda x: x
        self.set_conversion_function = set_conversion_function
        self.put_values = None
        if putFunc is None:
            putFunc = lambda x: x
        self.putFunc = putFunc

    def just_readback(self):
        """Only returns the currently stored readback-value."""
        return self._readback

    def get(self):
        """Reads the Signals value. If there is a `conversion_function`,
        the value is transformed by it.

        Parameters
        ----------

        Returns
        -------

        """
        if self.read_pv_name is not None:
            getval = caget(self.read_pv_name)
            if (
                self.put_values is not None
                and type(getval) in [int, float, np.float64]
                and np.abs(getval - self.put_values[1]) <= 1e-3 * getval
            ):
                self._readback = self.put_values[0]
            else:
                self._readback = self.conversion_function(getval)
        return super().get()

    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        """Puts the Signals value. If there is a `set_conversion_function`,
        the value is transformed by it. Also calls `self.putFunc`.

        Parameters
        ----------
        value :

        * :

        timestamp :
             (Default value = None)
        force :
             (Default value = False)
        metadata :
             (Default value = None)
        **kwargs :


        Returns
        -------

        """
        self.putFunc(value)
        val = self.set_conversion_function(value)
        if self.read_pv_name is not None:
            caput(self.read_pv_name, val, wait=True)
            self.put_values = (value, val)
        super().put(val, timestamp=timestamp, force=force, metadata=metadata, **kwargs)


class EpicsFieldSignalRO(EpicsFieldSignal):
    """The read-only implementation of EpicsFieldSignal. The only
    difference is that it raises an error, when one tries to put a value.

    Parameters
    ----------

    Returns
    -------

    """

    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        """

        Parameters
        ----------
        value :

        * :

        timestamp :
             (Default value = None)
        force :
             (Default value = False)
        metadata :
             (Default value = None)
        **kwargs :


        Returns
        -------

        """
        raise Exception("EpicsFieldSignalRO does not support putting a value!")
