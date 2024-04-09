from ophyd import Signal, SignalRO
import inspect


class Custom_Function_Signal(Signal):
    """Overwrites ophyd's Signal to add a simple python function that's called
    when calling `put`, `trigger` or `get`.

    Attributes
    ----------
    put_function : callable
        Called when the Signal's `put` method is called.

    read_function : callable
        Called when the Signal's `get` method is called.

    trigger_function : callable
        Called when the Signal's `trigger` method is called.
    """

    def __init__(
        self,
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
        put_function=None,
        read_function=None,
        trigger_function=None,
        retry_on_error=0,
        error_retry_function=None,
    ):
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
        self.put_function = put_function
        self.read_function = read_function
        self.trigger_function = trigger_function
        self.retry_on_error = retry_on_error
        self.error_retry_function = error_retry_function

    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        """
        Overwrites Signal's `put` to add the defined `put_function`.
        For further information see ophyd's documentation.
        """
        if self.put_function:
            if inspect.getfullargspec(self.put_function).args[0] == '_self_instance':
                retry_function(
                    self.put_function(self, value),
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                )
            else:
                retry_function(
                    self.put_function,
                    self.retry_on_error,
                    value,
                    error_retry_function=self.error_retry_function,
                )
        super().put(
            value, timestamp=timestamp, force=force, metadata=metadata, **kwargs
        )

    def get(self):
        """
        Overwrites Signal's `get` to add the defined `read_function`.
        For further information see ophyd's documentation.
        """
        if self.read_function:
            if inspect.getfullargspec(self.read_function).args[0] == '_self_instance':
                self._readback = retry_function(
                    self.read_function(self),
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                )
            else:    
                self._readback = retry_function(
                    self.read_function,
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                )
        return super().get()

    def trigger(self):
        """
        Overwrites Signal's `trigger` to add the defined `trigger_function`.
        For further information see ophyd's documentation.
        """
        if self.trigger_function:
            retry_function(
                self.trigger_function,
                self.retry_on_error,
                error_retry_function=self.error_retry_function,
            )
        return super().trigger()

    def describe(self):
        """Overwrites describe to add 'Custom Function' as 'source'."""
        info = super().describe()
        info[self.name]["source"] = "Custom Function"
        return info

    def read_configuration(self):
        if self._readback is not None:
            value = self._readback
        else:
            value = self.get()
        return {self.name: {"value": value, "timestamp": self.timestamp}}


def retry_function(func, retries: int, *args, error_retry_function=None, **kwargs):
    excs = []
    for i in range(retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            excs.append(e)
            if error_retry_function:
                error_retry_function(e)
    raise Exception(
        f"Failed to execute function {func} after {retries} retries. Last exception: {excs[-1]}"
    )


class Custom_Function_SignalRO(SignalRO):
    """Overwrites ophyd's SignalRO to add a simple python function that's called
    when calling, `trigger` or `get`.

    Attributes
    ----------
    read_function : callable
        Called when the Signal's `get` method is called.

    trigger_function : callable
        Called when the Signal's `trigger` method is called.
    """

    def __init__(
        self,
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
        read_function=None,
        trigger_function=None,
        retry_on_error=0,
        error_retry_function=None,
    ):
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
        self.read_function = read_function
        self.trigger_function = trigger_function
        self.retry_on_error = retry_on_error
        self.error_retry_function = error_retry_function

    def get(self):
        """
        Overwrites SignalRO's `get` to add the defined `read_function`.
        For further information see ophyd's documentation.
        """
        if self.read_function:
            if inspect.getfullargspec(self.read_function).args[0] == '_self_instance':
                self._readback = retry_function(
                    self.read_function(self),
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                )
            else:    
                self._readback = retry_function(
                    self.read_function,
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                )
        return super().get()

    def trigger(self):
        """
        Overwrites SignalRO's `trigger` to add the defined `trigger_function`.
        For further information see ophyd's documentation.
        """
        if self.trigger_function:
            retry_function(
                self.trigger_function,
                self.retry_on_error,
                error_retry_function=self.error_retry_function,
            )
        return super().trigger()

    def describe(self):
        """Overwrites describe to add 'Custom Function' as 'source'."""
        info = super().describe()
        info[self.name]["source"] = "Custom Function"
        return info

    def read_configuration(self):
        if self._readback is not None:
            value = self._readback
        else:
            value = self.get()
        return {self.name: {"value": value, "timestamp": self.timestamp}}
