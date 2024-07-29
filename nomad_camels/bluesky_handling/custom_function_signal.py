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
        force_sequential=None,
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
        self.force_sequential = force_sequential

    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        """
        Overwrites Signal's `put` to add the defined `put_function`.
        For further information see ophyd's documentation.
        """
        if self.put_function:
            # If the put_function requires the instance of the class, pass it as the first argument
            # The instance is the signal, while the parent is the Device class
            # For dynamically created signals often a call to self.parent is required
            parent = False
            if self.force_sequential is not None:
                parent = self.parent if self.force_sequential else False
            elif getattr(self.parent, "force_sequential", None):
                parent = self.parent
            if (
                self.put_function
                and inspect.getfullargspec(self.put_function).args
                and inspect.getfullargspec(self.put_function).args[0]
                == "_self_instance"
            ):
                retry_function(
                    self.put_function(self, value),
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    # parent is required if you want to force sequential reading
                    # parent is False if self.parent.force_sequential is False
                    # or if self.parent does not have a force_sequential attribute
                    parent=parent,
                )
            else:
                retry_function(
                    self.put_function,
                    self.retry_on_error,
                    value,
                    error_retry_function=self.error_retry_function,
                    # parent is required if you want to force sequential reading
                    # parent is False if self.parent.force_sequential is False
                    # or if self.parent does not have a force_sequential attribute
                    parent=parent,
                )
        super().put(
            value, timestamp=timestamp, force=force, metadata=metadata, **kwargs
        )

    def get(self):
        """
        Overwrites Signal's `get` to add the defined `read_function`.
        For further information see ophyd's documentation.
        """
        old_value = self._readback
        if self.read_function:
            # If the read_function requires the instance of the class, pass it as the first argument
            # The instance is the signal, while the parent is the Device class
            # For dynamically created signals often a call to self.parent is required
            parent = False
            if self.force_sequential is not None:
                parent = self.parent if self.force_sequential else False
            elif getattr(self.parent, "force_sequential", None):
                parent = self.parent
            if (
                self.read_function
                and inspect.getfullargspec(self.read_function).args
                and inspect.getfullargspec(self.read_function).args[0]
                == "_self_instance"
            ):
                self._readback = retry_function(
                    self.read_function(self),
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    # parent is required if you want to force sequential reading
                    # parent is False if self.parent.force_sequential is False
                    # or if self.parent does not have a force_sequential attribute
                    parent=parent,
                )
            else:
                self._readback = retry_function(
                    self.read_function,
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    # parent is required if you want to force sequential reading
                    # parent is False if self.parent.force_sequential is False
                    # or if self.parent does not have a force_sequential attribute
                    parent=parent,
                )
        self._run_subs(
            sub_type=self.SUB_VALUE,
            old_value=old_value,
            value=self._readback,
            timestamp=time.time(),
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


def retry_function(
    func, retries: int, *args, error_retry_function=None, parent=None, **kwargs
):
    """
    This function attempts to execute a given function multiple times until it succeeds or the maximum number of retries is reached.
    If a parent object is provided and it is currently reading, the function waits until the parent is no longer reading before attempting to execute the function.

    Parameters:
    func (callable): The function to be executed.
    retries (int): The maximum number of times to retry executing the function.
    *args: Variable length argument list for the function to be executed.
    error_retry_function (callable, optional): A function to be called when an error occurs. Defaults to None.
    parent (object, optional): An object (the instrument class) that the function checks for a currently_reading attribute. If currently_reading is True, the function waits until it is False before executing. Defaults to None.
    **kwargs: Arbitrary keyword arguments for the function to be executed.

    Returns:
    The return value of the function to be executed.

    Raises:
    Exception: If the function fails to execute after the specified number of retries, an exception is raised with details of the last exception encountered.
    """
    if parent:
        while parent.currently_reading:
            time.sleep(0.001)  # wait for 1 ms
        parent.currently_reading = True
    excs = []
    for i in range(retries + 1):
        try:
            result = func(*args, **kwargs)
            if parent:
                parent.currently_reading = False
            return result
        except Exception as e:
            excs.append(e)
            if error_retry_function:
                error_retry_function(e)
    parent.currently_reading = False
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
        force_sequential=None,
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
        self.force_sequential = force_sequential

    def get(self):
        """
        Overwrites SignalRO's `get` to add the defined `read_function`.
        For further information see ophyd's documentation.
        """
        old_value = self._readback
        if self.read_function:
            # If the read_function requires the instance of the class, pass it as the first argument
            # The instance is the signal, while the parent is the Device class
            # For dynamically created signals often a call to self.parent is required
            parent = False
            if self.force_sequential is not None:
                parent = self.parent if self.force_sequential else False
            elif getattr(self.parent, "force_sequential", None):
                parent = self.parent
            if (
                self.read_function
                and inspect.getfullargspec(self.read_function).args
                and inspect.getfullargspec(self.read_function).args[0]
                == "_self_instance"
            ):
                self._readback = retry_function(
                    self.read_function(self),
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    # parent is required if you want to force sequential reading
                    # parent is False if self.parent.force_sequential is False
                    # or if self.parent does not have a force_sequential attribute
                    parent=parent,
                )
            else:
                self._readback = retry_function(
                    self.read_function,
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    # parent is required if you want to force sequential reading
                    # parent is False if self.parent.force_sequential is False
                    # or if self.parent does not have a force_sequential attribute
                    parent=parent,
                )
        self._run_subs(
            sub_type=self.SUB_VALUE,
            old_value=old_value,
            value=self._readback,
            timestamp=time.time(),
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
    def __init__(
        self, force_sequential=False, currently_reading=False, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.force_sequential = force_sequential
        self.currently_reading = currently_reading
