from ophyd import Signal, SignalRO, Device, Kind
import inspect
import time


class Custom_Function_Signal(Signal):
    """
    A custom signal class that extends ophyd's Signal by allowing the user to specify
    custom functions that are executed when putting, reading, or triggering the signal.

    Attributes:
        put_function (callable): Function called when the signal's put() method is invoked.
        read_function (callable): Function called when the signal's get() method is invoked.
        trigger_function (callable): Function called when the signal's trigger() method is invoked.
        retry_on_error (int): Number of retry attempts in case of failure when calling custom functions.
        error_retry_function (callable): Optional function to be called if a custom function raises an error.
        force_sequential (bool): Flag to force sequential execution; if True, operations may wait for the parent.
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
        """
        Initialize a Custom_Function_Signal instance.

        Args:
            name (str): Name of the signal.
            value (optional): Initial value of the signal. Defaults to 0.0.
            timestamp (optional): Timestamp for the signal.
            parent (optional): Parent device of the signal.
            labels (optional): Labels for the signal.
            kind (str, optional): Kind of signal (e.g., 'hinted'). Defaults to "hinted".
            tolerance (optional): Tolerance for value changes.
            rtolerance (optional): Relative tolerance for value changes.
            metadata (optional): Additional metadata.
            cl (optional): Class information for the signal.
            attr_name (str, optional): Attribute name of the signal.
            put_function (callable, optional): Function to be called during put().
            read_function (callable, optional): Function to be called during get().
            trigger_function (callable, optional): Function to be called during trigger().
            retry_on_error (int, optional): Number of retries if custom functions fail. Defaults to 0.
            error_retry_function (callable, optional): Function to call when an error occurs.
            force_sequential (bool, optional): If True, operations force sequential execution with the parent.
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
        self.put_function = put_function
        self.read_function = read_function
        self.trigger_function = trigger_function
        self.retry_on_error = retry_on_error
        self.error_retry_function = error_retry_function
        self.force_sequential = force_sequential

    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        """
        Write a value to the signal. If a put_function is defined, it is called to process the value.
        The function is retried upon error based on the retry_on_error setting.

        This method first checks if a put_function is provided and if it needs the instance reference.
        If the put_function's first parameter is named "_self_instance", the instance (self) is passed.
        Otherwise, the function is executed without the instance.

        Args:
            value: The value to be written to the signal.
            timestamp (optional): Timestamp for the put operation.
            force (bool, optional): Force the put operation even if the value is the same. Defaults to False.
            metadata (optional): Additional metadata for the put operation.
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        if self.put_function:
            # Determine if sequential execution is forced via self.force_sequential or parent's attribute.
            parent = False
            if self.force_sequential is not None:
                parent = self.parent if self.force_sequential else False
            elif getattr(self.parent, "force_sequential", None):
                parent = self.parent

            # Check if the put_function expects the instance as the first argument.
            if (
                self.put_function
                and inspect.getfullargspec(self.put_function).args
                and inspect.getfullargspec(self.put_function).args[0] == "_self_instance"
            ):
                retry_function(
                    self.put_function(self, value),
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    parent=parent,  # Ensure sequential reading if required.
                )
            else:
                retry_function(
                    self.put_function,
                    self.retry_on_error,
                    value,
                    error_retry_function=self.error_retry_function,
                    parent=parent,  # Ensure sequential reading if required.
                )

        # Call the parent class put() method after processing.
        super().put(value, timestamp=timestamp, force=force, metadata=metadata, **kwargs)

    def get(self):
        """
        Read the value from the signal. If a read_function is defined, it is used to obtain the value.
        The function is retried upon error based on the retry_on_error setting.

        This method updates the internal _readback attribute and notifies subscribers of the change.

        Returns:
            The value obtained from the parent get() method.
        """
        old_value = self._readback
        if self.read_function:
            # Determine if sequential execution is forced via self.force_sequential or parent's attribute.
            parent = False
            if self.force_sequential is not None:
                parent = self.parent if self.force_sequential else False
            elif getattr(self.parent, "force_sequential", None):
                parent = self.parent

            # Check if the read_function expects the instance as the first argument.
            if (
                self.read_function
                and inspect.getfullargspec(self.read_function).args
                and inspect.getfullargspec(self.read_function).args[0] == "_self_instance"
            ):
                self._readback = retry_function(
                    self.read_function(self),
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    parent=parent,
                )
            else:
                self._readback = retry_function(
                    self.read_function,
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    parent=parent,
                )

        # Notify subscribers that the signal value has changed.
        self._run_subs(
            sub_type=self.SUB_VALUE,
            old_value=old_value,
            value=self._readback,
            timestamp=time.time(),
        )
        return super().get()

    def trigger(self):
        """
        Trigger the signal. If a trigger_function is defined, it is executed with retries upon failure.

        Returns:
            The result of the parent trigger() method.
        """
        if self.trigger_function:
            retry_function(
                self.trigger_function,
                self.retry_on_error,
                error_retry_function=self.error_retry_function,
            )
        return super().trigger()

    def describe(self):
        """
        Return a description of the signal with a custom source identifier.

        Returns:
            dict: A dictionary describing the signal, with the 'source' set to "Custom Function".
        """
        info = super().describe()
        info[self.name]["source"] = "Custom Function"
        return info

    def read_configuration(self):
        """
        Read the current configuration of the signal.

        If _readback is already set, that value is used; otherwise, get() is called.
        The returned configuration is a dictionary with the signal's name as the key and a dictionary
        containing the value and timestamp.

        Returns:
            dict: A dictionary in the format {signal_name: {"value": value, "timestamp": timestamp}}.
        """
        if self._readback is not None:
            value = self._readback
        else:
            value = self.get()
        return {self.name: {"value": value, "timestamp": self.timestamp}}


def retry_function(
    func, retries: int, *args, error_retry_function=None, parent=None, **kwargs
):
    """
    Attempt to execute a function multiple times until it succeeds or the maximum number of retries is reached.

    If a parent object is provided and it is currently reading (i.e., parent.currently_reading is True),
    the function waits until the parent is no longer reading before executing.

    Args:
        func (callable): The function to be executed.
        retries (int): Maximum number of retries upon failure.
        *args: Variable length argument list for the function.
        error_retry_function (callable, optional): Function to call when an error occurs. Defaults to None.
        parent (object, optional): An object (e.g., an instrument) that may enforce sequential access. Defaults to None.
        **kwargs: Arbitrary keyword arguments for the function.

    Returns:
        The result of the function call if successful.

    Raises:
        Exception: If the function fails after the specified number of retries, an exception is raised
                   with details of the last and first encountered exceptions.
    """
    if parent:
        # Wait until the parent is not in a reading state.
        while parent.currently_reading:
            time.sleep(0.001)  # Sleep for 1 ms before checking again.
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
    if parent:
        parent.currently_reading = False
    raise Exception(
        f"Failed to execute function {func} after {retries} retries.\n"
        f"Last exception: {excs[-1]}\nFirst exception: {excs[0]}"
    ) from excs[-1]


class Custom_Function_SignalRO(SignalRO):
    """
    A custom read-only signal class that extends ophyd's SignalRO by allowing the user to specify
    functions that are executed when reading or triggering the signal.

    Attributes:
        read_function (callable): Function called when the signal's get() method is invoked.
        trigger_function (callable): Function called when the signal's trigger() method is invoked.
        retry_on_error (int): Number of retry attempts in case of failure when calling custom functions.
        error_retry_function (callable): Optional function to be called if a custom function raises an error.
        force_sequential (bool): Flag to force sequential execution; if True, operations may wait for the parent.
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
        """
        Initialize a Custom_Function_SignalRO instance.

        Args:
            name (str): Name of the signal.
            value (optional): Initial value of the signal. Defaults to 0.0.
            timestamp (optional): Timestamp for the signal.
            parent (optional): Parent device of the signal.
            labels (optional): Labels for the signal.
            kind (str, optional): Kind of signal (e.g., 'hinted'). Defaults to "hinted".
            tolerance (optional): Tolerance for value changes.
            rtolerance (optional): Relative tolerance for value changes.
            metadata (optional): Additional metadata.
            cl (optional): Class information for the signal.
            attr_name (str, optional): Attribute name of the signal.
            read_function (callable, optional): Function to be called during get().
            trigger_function (callable, optional): Function to be called during trigger().
            retry_on_error (int, optional): Number of retries if custom functions fail. Defaults to 0.
            error_retry_function (callable, optional): Function to call when an error occurs.
            force_sequential (bool, optional): If True, operations force sequential execution with the parent.
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
        self.read_function = read_function
        self.trigger_function = trigger_function
        self.retry_on_error = retry_on_error
        self.error_retry_function = error_retry_function
        self.force_sequential = force_sequential

    def get(self):
        """
        Read the value from the read-only signal. If a read_function is defined, it is used to obtain the value.
        The function is retried upon error based on the retry_on_error setting.

        The internal _readback attribute is updated and subscribers are notified of the change.

        Returns:
            The value obtained from the parent get() method.
        """
        old_value = self._readback
        if self.read_function:
            # Determine if sequential execution is enforced.
            parent = False
            if self.force_sequential is not None:
                parent = self.parent if self.force_sequential else False
            elif getattr(self.parent, "force_sequential", None):
                parent = self.parent

            # Check if the read_function expects the instance as the first argument.
            if (
                self.read_function
                and inspect.getfullargspec(self.read_function).args
                and inspect.getfullargspec(self.read_function).args[0] == "_self_instance"
            ):
                self._readback = retry_function(
                    self.read_function(self),
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    parent=parent,
                )
            else:
                self._readback = retry_function(
                    self.read_function,
                    self.retry_on_error,
                    error_retry_function=self.error_retry_function,
                    parent=parent,
                )

        # Notify subscribers about the update.
        self._run_subs(
            sub_type=self.SUB_VALUE,
            old_value=old_value,
            value=self._readback,
            timestamp=time.time(),
        )
        return super().get()

    def trigger(self):
        """
        Trigger the read-only signal. If a trigger_function is defined, it is executed with retries upon failure.

        Returns:
            The result of the parent trigger() method.
        """
        if self.trigger_function:
            retry_function(
                self.trigger_function,
                self.retry_on_error,
                error_retry_function=self.error_retry_function,
            )
        return super().trigger()

    def describe(self):
        """
        Return a description of the read-only signal with a custom source identifier.

        Returns:
            dict: A dictionary describing the signal, with the 'source' set to "Custom Function".
        """
        info = super().describe()
        info[self.name]["source"] = "Custom Function"
        return info

    def read_configuration(self):
        """
        Read the current configuration of the read-only signal.

        If _readback is set and the signal is not a configuration signal with an associated read_function,
        the existing value is used; otherwise, get() is called to obtain the value.
        The returned configuration is a dictionary with the signal's name as the key and a dictionary
        containing the value and timestamp.

        Returns:
            dict: A dictionary in the format {signal_name: {"value": value, "timestamp": timestamp}}.
        """
        if self._readback is not None and not (self.kind in ['config', Kind.config] and self.read_function):
            value = self._readback
        else:
            value = self.get()
        return {self.name: {"value": value, "timestamp": self.timestamp}}


class Sequential_Device(Device):
    """
    A custom device class that supports sequential operations.
    It provides flags to force sequential execution and to indicate whether a reading operation is in progress.
    """

    def __init__(
        self, force_sequential=False, currently_reading=False, *args, **kwargs
    ):
        """
        Initialize a Sequential_Device instance.

        Args:
            force_sequential (bool, optional): If True, operations on this device are executed sequentially. Defaults to False.
            currently_reading (bool, optional): Indicates if the device is currently performing a read operation. Defaults to False.
            *args: Additional positional arguments passed to the Device base class.
            **kwargs: Additional keyword arguments passed to the Device base class.
        """
        super().__init__(*args, **kwargs)
        self.force_sequential = force_sequential
        self.currently_reading = currently_reading
