from ophyd import Signal, SignalRO, Device
import inspect
import time


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
            # If the put_function requires the instance of the class, pass it as the first argument
            # The instance is the signal, while the parent is the Device class
            # For dynamically created signals often a call to self.parent is required
            if inspect.getfullargspec(self.put_function).args[0] == '_self_instance':
                retry_function(
                    self.put_function(self, value),
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    # self_instance is required if you want to force sequential reading
                    # self_instance is False if there is self.parent does not have a force_sequential attribute
                    # self_instance is None if self.parent.force_sequential is False
                    self_instance = self if getattr(self.parent, 'force_sequential', False) else None,
                )
            else:
                retry_function(
                    self.put_function,
                    self.retry_on_error,
                    value,
                    error_retry_function=self.error_retry_function,
                    # self_instance is required if you want to force sequential reading
                    # self_instance is False if there is self.parent does not have a force_sequential attribute
                    # self_instance is None if self.parent.force_sequential is False
                    self_instance = self if getattr(self.parent, 'force_sequential', False) else None,
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
            # If the read_function requires the instance of the class, pass it as the first argument
            # The instance is the signal, while the parent is the Device class
            # For dynamically created signals often a call to self.parent is required
            if inspect.getfullargspec(self.read_function).args[0] == '_self_instance':
                self._readback = retry_function(
                    self.read_function(self),
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    # self_instance is required if you want to force sequential reading
                    # self_instance is False if there is self.parent does not have a force_sequential attribute
                    # self_instance is None if self.parent.force_sequential is False
                    self_instance = self if getattr(self.parent, 'force_sequential', False) else None,
                )
            else:    
                self._readback = retry_function(
                    self.read_function,
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    # self_instance is required if you want to force sequential reading
                    # self_instance is False if there is self.parent does not have a force_sequential attribute
                    # self_instance is None if self.parent.force_sequential is False
                    self_instance = self if getattr(self.parent, 'force_sequential', False) else None,
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
    """
    This function attempts to execute a given function multiple times until it succeeds or the maximum number of retries is reached.

    Parameters:
    func (callable): The function to be executed.
    retries (int): The maximum number of times to retry executing the function.
    *args: Variable length argument list for the function to be executed.
    error_retry_function (callable, optional): A function to be called when an error occurs. Defaults to None.
    **kwargs: Arbitrary keyword arguments for the function to be executed. Special keyword arguments:
        - force_sequential (bool, optional): If True, the function execution will be forced to be sequential. Defaults to False.

    Returns:
    The return value of the function to be executed.

    Raises:
    Exception: If the function fails to execute after the specified number of retries, an exception is raised with details of the last exception encountered.
    """
    self_instance = kwargs.pop('self_instance', None)
    if self_instance:
        while self_instance.parent.currently_reading:
            time.sleep(0.001) # wait for 1 ms
        self_instance.parent.currently_reading = True
    excs = []
    for i in range(retries + 1):
        try:
            result = func(*args, **kwargs)
            if self_instance:
                self_instance.parent.currently_reading = False
            return result
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
        force_sequential=False,
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
            # If the read_function requires the instance of the class, pass it as the first argument
            # The instance is the signal, while the parent is the Device class
            # For dynamically created signals often a call to self.parent is required
            if inspect.getfullargspec(self.read_function).args[0] == '_self_instance':
                self._readback = retry_function(
                    self.read_function(self),
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    self_instance = self if getattr(self.parent, 'force_sequential', False) else None,
                )
            else:    
                self._readback = retry_function(
                    self.read_function,
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    self_instance = self if getattr(self.parent, 'force_sequential', False) else None,
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


class Sequential_Device(Device):
    def __init__(self, force_sequential=False, currently_reading=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.force_sequential = force_sequential
        self.currently_reading = currently_reading
