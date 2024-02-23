from tqdm import tqdm


class ProgressBar:
    """Provides a progress bar for protocols run directly from the script.
    With the `emit` method, the bar can be updated the same way signals are
    used when running the protocol from the UI.

    Attributes
    ----------
    n_steps : int
        the number of total (expected) steps of the protocol
    bar : tqdm
        the actual progress bar
    """

    def __init__(self, n_steps):
        self.n_steps = n_steps
        self.bar = tqdm(total=n_steps)

    def emit(self, n):
        """
        Updates the progress bar to the next step. The parameter `n` is only so
        the function has the same shape as the `emit` function for the signal
        used with the main UI.

        Parameters
        ----------
        n : int
            has no function, only there to be able to give this method a value
        """
        self.bar.update()
