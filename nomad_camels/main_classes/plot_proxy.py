import threading
from bluesky.callbacks.zmq import Proxy


class StoppableProxy(Proxy):
    """
    A subclass of Proxy that runs in a background thread and provides a stop() method
    to cleanly shut down the proxy.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._thread = None
        self._stopped = False

        # Set LINGER to 0 to avoid blocking on socket close.
        self._frontend.setsockopt(self.zmq.LINGER, 0)
        self._backend.setsockopt(self.zmq.LINGER, 0)

    def start(self):
        if self.closed:
            raise RuntimeError(
                "This Proxy has already been started and interrupted. "
                "Create a fresh instance with {}".format(repr(self))
            )
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        try:
            # This call blocks until the context is terminated.
            self.zmq.device(self.zmq.FORWARDER, self._frontend, self._backend)
        except Exception:
            # The device call will throw an exception when the context is terminated.
            pass
        finally:
            self.closed = True
            self._frontend.close()
            self._backend.close()
            # Only terminate the context here if stop() hasn't already done so.
            if not self._stopped:
                try:
                    self._context.term()
                except self.zmq.ZMQError as e:
                    # Ignore the "Resource temporarily unavailable" error.
                    if e.errno != self.zmq.EAGAIN:
                        raise

    def stop(self):
        """
        Stop the proxy by terminating the ZeroMQ context,
        which interrupts the blocking device call.
        """
        if self.closed:
            return
        self._stopped = True
        try:
            self._context.term()
        except self.zmq.ZMQError as e:
            if e.errno != self.zmq.EAGAIN:
                raise
        if self._thread is not None:
            self._thread.join()
